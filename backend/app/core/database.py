import logging
from typing import Generator
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.exc import OperationalError, SQLAlchemyError

from app.core.config import settings

logger = logging.getLogger(__name__)

# Create SQLAlchemy engine
# pool_pre_ping=True helps detect stale/dropped connections
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a transactional database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_database_connection() -> dict:
    """
    Checks if the MySQL database connection is alive.
    Returns status dictionary.
    """
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"connected": True, "message": "Database connection healthy"}
    except OperationalError as e:
        logger.warning(f"Database connection not available: {str(e)}")
        return {"connected": False, "message": f"Database not connected: {str(e)}"}
    except Exception as e:
        logger.warning(f"Unexpected database error: {str(e)}")
        return {"connected": False, "message": f"Database error: {str(e)}"}


def init_db() -> bool:
    """
    Creates database tables if MySQL database exists and is reachable.
    Does not crash the application if MySQL is temporarily unreachable.
    """
    try:
        import app.models  # noqa: F401 - Register all models with Base.metadata
        Base.metadata.create_all(bind=engine)
        
        # Backward-compatible column check for recommendations table
        try:
            with engine.connect() as conn:
                cols = [r[0] for r in conn.execute(text("DESCRIBE recommendations")).fetchall()]
                new_cols = [
                    ("recommendation_score", "FLOAT NULL"),
                    ("concept_gap", "FLOAT NULL"),
                    ("difficulty_fit", "FLOAT NULL"),
                    ("primary_weak_concept", "VARCHAR(100) NULL")
                ]
                for col_name, col_type in new_cols:
                    if col_name not in cols:
                        conn.execute(text(f"ALTER TABLE recommendations ADD COLUMN {col_name} {col_type}"))
                conn.commit()
        except Exception as col_err:
            logger.debug(f"Recommendation column verification note: {col_err}")

        # Non-destructive Phase 1 RBAC check for users.role column
        try:
            with engine.connect() as conn:
                user_cols = [r[0] for r in conn.execute(text("DESCRIBE users")).fetchall()]
                if "role" not in user_cols:
                    conn.execute(text("ALTER TABLE users ADD COLUMN role VARCHAR(20) NOT NULL DEFAULT 'STUDENT'"))
                    conn.execute(text("UPDATE users SET role = 'STUDENT' WHERE role IS NULL OR role = ''"))
                    conn.commit()
                    logger.info("Phase 1 RBAC: Added 'role' column to users table with default 'STUDENT'.")
        except Exception as role_col_err:
            logger.debug(f"User role column verification note: {role_col_err}")

        # Non-destructive Phase 2 Diagnostic Enforcement check for users diagnostic columns
        try:
            with engine.connect() as conn:
                user_cols = [r[0] for r in conn.execute(text("DESCRIBE users")).fetchall()]
                diag_cols = [
                    ("diagnostic_completed", "TINYINT(1) NOT NULL DEFAULT 0"),
                    ("diagnostic_exempt", "TINYINT(1) NOT NULL DEFAULT 0"),
                    ("diagnostic_score", "INT NULL"),
                    ("diagnostic_total", "INT NULL"),
                    ("diagnostic_completed_at", "DATETIME NULL")
                ]
                for col_name, col_type in diag_cols:
                    if col_name not in user_cols:
                        conn.execute(text(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}"))
                        if col_name == "diagnostic_exempt":
                            # Safe migration strategy: Existing baseline users (created before Phase 2) are marked exempt
                            conn.execute(text("UPDATE users SET diagnostic_exempt = 1 WHERE id <= 297"))
                conn.commit()
                logger.info("Phase 2 Diagnostic: Verified diagnostic columns on users table.")
        except Exception as diag_col_err:
            logger.debug(f"User diagnostic columns verification note: {diag_col_err}")

        # Non-destructive Phase 3 Multi-Language check for submissions and problems tables
        try:
            with engine.connect() as conn:
                sub_cols = [r[0] for r in conn.execute(text("DESCRIBE submissions")).fetchall()]
                if "language" not in sub_cols:
                    conn.execute(text("ALTER TABLE submissions ADD COLUMN language VARCHAR(20) NOT NULL DEFAULT 'python'"))
                    conn.execute(text("UPDATE submissions SET language = 'python' WHERE language IS NULL OR language = ''"))
                    logger.info("Phase 3 Multi-Language: Added 'language' column to submissions table.")

                prob_cols = [r[0] for r in conn.execute(text("DESCRIBE problems")).fetchall()]
                new_prob_cols = [
                    ("starter_code_java", "TEXT NULL"),
                    ("reference_solution_java", "TEXT NULL"),
                    ("starter_code_cpp", "TEXT NULL"),
                    ("reference_solution_cpp", "TEXT NULL"),
                    ("starter_code_javascript", "TEXT NULL"),
                    ("reference_solution_javascript", "TEXT NULL")
                ]
                for col_name, col_type in new_prob_cols:
                    if col_name not in prob_cols:
                        conn.execute(text(f"ALTER TABLE problems ADD COLUMN {col_name} {col_type}"))
                da_cols = [r[0] for r in conn.execute(text("DESCRIBE diagnostic_attempts")).fetchall()]
                if "language" not in da_cols:
                    conn.execute(text("ALTER TABLE diagnostic_attempts ADD COLUMN language VARCHAR(20) NOT NULL DEFAULT 'python'"))
                    conn.execute(text("UPDATE diagnostic_attempts SET language = 'python' WHERE language IS NULL OR language = ''"))
                    logger.info("Phase 3 Multi-Language: Added 'language' column to diagnostic_attempts table.")

                conn.commit()
                logger.info("Phase 3 Multi-Language: Verified multi-language columns on submissions, problems, and diagnostic attempts.")
        except Exception as phase3_col_err:
            logger.debug(f"Phase 3 column verification note: {phase3_col_err}")

        # Non-destructive Phase 4: Synchronize diagnostic completion for users with full historical attempts
        try:
            with engine.connect() as conn:
                conn.execute(text("""
                    UPDATE users u
                    JOIN (
                        SELECT da.user_id,
                               SUM(CASE WHEN da.is_solved = 1 THEN 1 ELSE 0 END) AS solved_count,
                               COUNT(DISTINCT da.problem_id) AS total_attempted,
                               MAX(da.created_at) AS last_attempt_at
                        FROM diagnostic_attempts da
                        JOIN problems p ON da.problem_id = p.id AND p.is_diagnostic = 1
                        GROUP BY da.user_id
                        HAVING COUNT(DISTINCT da.problem_id) >= (SELECT COUNT(*) FROM problems WHERE is_diagnostic = 1)
                    ) diag ON u.id = diag.user_id
                    SET u.diagnostic_completed = 1,
                        u.diagnostic_score = COALESCE(u.diagnostic_score, diag.solved_count),
                        u.diagnostic_total = COALESCE(u.diagnostic_total, diag.total_attempted),
                        u.diagnostic_completed_at = COALESCE(u.diagnostic_completed_at, diag.last_attempt_at)
                    WHERE u.diagnostic_completed = 0
                """))
                conn.commit()
        except Exception as phase4_err:
            logger.debug(f"Phase 4 diagnostic sync note: {phase4_err}")

        # Phase 5: Environment-based initial Admin Account Initialization
        # Creates an initial admin only if ADMIN_EMAIL & ADMIN_PASSWORD are provided via environment variables.
        # Never uses a hardcoded fallback or seeds an admin without explicit environment configuration.
        if settings.ADMIN_EMAIL and settings.ADMIN_PASSWORD:
            try:
                from app.core.security import get_password_hash
                from app.models.user import User, UserRole
                admin_email = settings.ADMIN_EMAIL.strip().lower()
                with SessionLocal() as db_session:
                    existing_admin = db_session.query(User).filter(User.email == admin_email).first()
                    if not existing_admin:
                        admin_count = db_session.query(User).filter(User.role == UserRole.ADMIN).count()
                        if admin_count == 0:
                            hashed_pw = get_password_hash(settings.ADMIN_PASSWORD)
                            new_admin = User(
                                name=settings.ADMIN_NAME or "Platform Administrator",
                                email=admin_email,
                                password_hash=hashed_pw,
                                role=UserRole.ADMIN,
                                diagnostic_completed=True,
                                diagnostic_exempt=True,
                            )
                            db_session.add(new_admin)
                            db_session.commit()
                            logger.info(f"Phase 5: Initialized administrative account '{admin_email}' from environment.")
            except Exception as admin_init_err:
                logger.warning(f"Phase 5 admin initialization note: {admin_init_err}")

        logger.info("Database tables verified/created successfully.")
        return True
    except (OperationalError, SQLAlchemyError) as e:
        logger.warning(
            f"Could not automatically initialize database tables. "
            f"Please ensure MySQL is running and the database specified in DATABASE_URL exists. Error: {str(e)}"
        )
        return False

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload

from app.core.database import get_db
from app.models.problem import Problem
from app.models.topic import Topic
from app.schemas.problem import ProblemSummary, ProblemDetail, TopicResponse, TestCaseResponse

router = APIRouter()


@router.get(
    "/topics",
    response_model=List[TopicResponse],
    status_code=status.HTTP_200_OK,
    summary="List all DSA topics"
)
def list_topics(db: Session = Depends(get_db)):
    """Return all 10 DSA curriculum topics ordered by index."""
    topics = db.query(Topic).order_by(Topic.order_index).all()
    return topics


@router.get(
    "",
    response_model=List[ProblemSummary],
    status_code=status.HTTP_200_OK,
    summary="List problems with optional filters"
)
def list_problems(
    topic: Optional[str] = Query(None, description="Filter by topic slug"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty: Easy, Medium, Hard"),
    is_diagnostic: Optional[bool] = Query(None, description="Filter to only diagnostic problems"),
    skip: int = Query(0, ge=0),
    limit: Optional[int] = Query(None, ge=1, le=2000),
    curated_only: bool = Query(False, description="Filter to curated benchmark problems (ID <= 40)"),
    db: Session = Depends(get_db)
):
    """
    List DSA problems with optional filters for topic, difficulty, diagnostic flag, and curated scope.
    """
    query = (
        db.query(Problem)
        .options(joinedload(Problem.topic))
        .join(Topic, Problem.topic_id == Topic.id)
    )

    if curated_only:
        query = query.filter(Problem.id <= 40)

    if topic:
        query = query.filter(Topic.slug == topic.lower())

    if difficulty:
        allowed = {"easy": "Easy", "medium": "Medium", "hard": "Hard"}
        normalized = allowed.get(difficulty.lower())
        if normalized is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid difficulty '{difficulty}'. Must be one of: Easy, Medium, Hard"
            )
        query = query.filter(Problem.difficulty == normalized)

    if is_diagnostic is not None:
        query = query.filter(Problem.is_diagnostic == is_diagnostic)

    query = query.order_by(Problem.order_index.asc()).offset(skip)
    if limit is not None:
        query = query.limit(limit)

    return query.all()


@router.get(
    "/{slug}",
    response_model=ProblemDetail,
    status_code=status.HTTP_200_OK,
    summary="Get full problem details by slug"
)
def get_problem(slug: str, db: Session = Depends(get_db)):
    """
    Retrieve a problem's full detail including description, starter code,
    and all visible (non-hidden) test cases.
    """
    problem = (
        db.query(Problem)
        .options(joinedload(Problem.topic), joinedload(Problem.test_cases))
        .filter(Problem.slug == slug.lower())
        .first()
    )

    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Problem with slug '{slug}' not found."
        )

    visible_tcs = sorted(
        [tc for tc in problem.test_cases if not tc.is_hidden],
        key=lambda t: t.order_index
    )

    return ProblemDetail(
        id=problem.id,
        title=problem.title,
        slug=problem.slug,
        difficulty=problem.difficulty,
        is_diagnostic=problem.is_diagnostic,
        order_index=problem.order_index,
        description_markdown=problem.description_markdown,
        constraints_markdown=problem.constraints_markdown,
        starter_code_python=problem.starter_code_python,
        starter_code_java=problem.starter_code_java,
        starter_code_cpp=problem.starter_code_cpp,
        starter_code_javascript=problem.starter_code_javascript,
        supported_languages=problem.supported_languages,
        topic=TopicResponse(
            id=problem.topic.id,
            name=problem.topic.name,
            slug=problem.topic.slug,
            order_index=problem.topic.order_index,
        ),
        visible_test_cases=[
            TestCaseResponse(
                id=tc.id,
                input_data=tc.input_data,
                expected_output=tc.expected_output,
                is_hidden=tc.is_hidden,
                order_index=tc.order_index
            )
            for tc in visible_tcs
        ]
    )

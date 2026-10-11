# Backend — LeetCode Adaptive Learning Platform

FastAPI REST API, SQLAlchemy ORM with MySQL, and modular ML knowledge-tracing foundation.

## Setup Instructions

1. **Create and activate a virtual environment (recommended)**:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```
   Update `DATABASE_URL` with your MySQL user, password, and port.

4. **Initialize MySQL Database**:
   ```sql
   CREATE DATABASE IF NOT EXISTS adaptive_learning CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

5. **Start FastAPI Backend Server**:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

6. **Verify Server**:
   - Health check: `http://localhost:8000/api/health`
   - Interactive Docs (Swagger): `http://localhost:8000/docs`

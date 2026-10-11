# LeetCode: An AI-Driven Adaptive Learning and Problem Recommendation Framework

A self-contained AI-driven adaptive coding learning platform designed to demonstrate personalized Data Structures and Algorithms (DSA) problem recommendation using diagnostic assessment, knowledge tracing, and explainable recommendations.

## Project Structure
```
Adaptive_Learning_platform/
├── backend/          # FastAPI Python backend + SQLAlchemy ORM + ML Engine
│   ├── app/
│   │   ├── api/      # REST API route handlers
│   │   ├── core/     # App config, database connections, security
│   │   ├── models/   # SQLAlchemy database models
│   │   ├── schemas/  # Pydantic validation models
│   │   ├── services/ # Business logic layer
│   │   ├── engine/   # Code evaluation & recommendation algorithms
│   │   ├── ml/       # LSTM Knowledge Tracing architecture (Milestone 5)
│   │   └── seeds/    # Curriculum & problem dataset seeders (Milestone 3)
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
├── frontend/         # React + Vite single-page application
│   ├── src/
│   │   ├── components/ # Reusable UI components
│   │   ├── pages/      # Route pages & views
│   │   ├── services/   # Axios / API clients
│   │   ├── context/    # React context providers
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   └── README.md
├── README.md
└── .gitignore
```

## Milestone 1: Foundation Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- MySQL 8.0+

### Database Setup
1. Open MySQL CLI or MySQL Workbench:
   ```sql
   CREATE DATABASE IF NOT EXISTS adaptive_learning CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
2. Copy `backend/.env.example` to `backend/.env` and configure your credentials:
   ```env
   DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/adaptive_learning
   SECRET_KEY=your_secret_key_here
   ```

### Running Backend
```bash
cd backend
python -m pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Backend API will be available at: `http://localhost:8000`
Health check: `http://localhost:8000/api/health`
Interactive Swagger API Docs: `http://localhost:8000/docs`

### Running Frontend
```bash
cd frontend
npm install
npm run dev
```
Frontend UI will be available at: `http://localhost:5173`

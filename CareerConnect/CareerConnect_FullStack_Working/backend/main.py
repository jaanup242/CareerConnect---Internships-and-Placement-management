from fastapi import FastAPI
from sqlalchemy import inspect, text
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models
from routers import auth_routes, jobs, applications, profiles

Base.metadata.create_all(bind=engine)

# Keep the existing CareerConnect database compatible with the expanded
# employer hiring workflow. This is intentionally lightweight so existing
# MySQL/SQLite databases do not need to be recreated.
def ensure_schema_columns():
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    if "jobs" in tables:
        job_existing = {c["name"] for c in inspector.get_columns("jobs")}
        if "salary" not in job_existing:
            with engine.begin() as conn:
                conn.execute(text("ALTER TABLE jobs ADD COLUMN salary VARCHAR(100)"))

    if "applications" not in tables:
        return

    existing = {c["name"] for c in inspector.get_columns("applications")}
    columns = {
        "shortlisted": "BOOLEAN DEFAULT 0",
        "employer_notes": "TEXT",
        "interview_date": "VARCHAR(30)",
        "interview_time": "VARCHAR(20)",
        "interview_mode": "VARCHAR(20)",
        "interview_link": "VARCHAR(500)",
        "interviewer": "VARCHAR(150)",
        "interview_round": "VARCHAR(100)",
        "interview_instructions": "TEXT",
        "interview_feedback": "TEXT",
        "interview_technical": "VARCHAR(20)",
        "interview_communication": "VARCHAR(20)",
        "interview_problem_solving": "VARCHAR(20)",
        "interview_strengths": "TEXT",
        "interview_improvements": "TEXT",
        "interview_result": "VARCHAR(30)",
        "offer_position": "VARCHAR(150)",
        "offer_salary": "VARCHAR(100)",
        "offer_joining_date": "VARCHAR(30)",
        "offer_work_location": "VARCHAR(150)",
        "offer_employment_type": "VARCHAR(60)",
        "offer_expiry_date": "VARCHAR(30)",
        "offer_status": "VARCHAR(30) DEFAULT 'not_created'",
    }
    with engine.begin() as conn:
        for name, definition in columns.items():
            if name not in existing:
                conn.execute(text(f"ALTER TABLE applications ADD COLUMN {name} {definition}"))

ensure_schema_columns()

app = FastAPI(title="CareerConnect API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(jobs.router)
app.include_router(applications.router)
app.include_router(profiles.router)

@app.get("/")
def root():
    return {"message": "CareerConnect API is running", "version": "2.0.0"}

# CareerConnect — Full Stack

This version combines the new pastel CareerConnect frontend with a FastAPI + SQLAlchemy backend.

## Features
- Candidate and Company account registration/login
- JWT authentication and role protection
- Candidate profile stored in the database
- Company profile stored in the database
- Job posting and employer job management
- Candidate job search/filtering
- Real applications stored in the database
- Candidate application tracking
- Employer application review
- Accept/reject application status
- Bell-style application notifications
- MySQL support through DATABASE_URL
- SQLite default for zero-setup testing

## Run backend on Windows PowerShell

```powershell
cd backend
py -m venv venv
.env\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn main:app --reload
```

Backend:
http://127.0.0.1:8000

Swagger:
http://127.0.0.1:8000/docs

## Use your MySQL database

Open `backend/.env` and set:

```env
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/careerconnect
SECRET_KEY=replace-with-a-long-secret
```

If your MySQL password contains `@`, URL-encode it as `%40`.

Make sure the MySQL database `careerconnect` exists before starting FastAPI.

## Run frontend

Open the `frontend` folder in VS Code and use Live Server on:

`frontend/index.html`

The frontend talks to `http://127.0.0.1:8000`.

## Important
The old separate Employer Profile page is intentionally not included. Employers use Company Profile.

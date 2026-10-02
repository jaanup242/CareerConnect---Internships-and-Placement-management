from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from auth import require_role, get_current_user

router = APIRouter(prefix="/applications", tags=["Applications"])

VALID_STATUSES = {"pending", "review", "shortlisted", "interview", "selected", "rejected", "accepted"}
INTERVIEW_MODES = {"Online", "Offline"}
OFFER_STATUSES = {"not_created", "sent", "accepted", "declined", "expired"}

def get_employer_application(application_id: int, db: Session, current_user):
    app = db.query(models.Application).filter(models.Application.id == application_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    job = db.query(models.Job).filter(models.Job.id == app.job_id).first()
    if not job or job.employer_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only manage applications for your jobs")
    return app, job

def application_payload(app, job, candidate, profile):
    return {
        "application_id": app.id,
        "candidate_id": candidate.id,
        "candidate_name": candidate.name,
        "candidate_email": candidate.email,
        "candidate_phone": profile.phone if profile else None,
        "candidate_location": profile.location if profile else None,
        "candidate_about": profile.about if profile else None,
        "candidate_college": profile.college if profile else None,
        "candidate_degree": profile.degree if profile else None,
        "candidate_branch": profile.branch if profile else None,
        "candidate_current_year": profile.current_year if profile else None,
        "candidate_graduation_year": profile.graduation_year if profile else None,
        "candidate_cgpa": profile.cgpa if profile else None,
        "candidate_qualifications": profile.qualifications if profile else None,
        "candidate_skills": profile.skills if profile else None,
        "candidate_projects": profile.projects if profile else None,
        "candidate_experience": profile.experience if profile else None,
        "candidate_achievements": profile.achievements if profile else None,
        "candidate_certifications": profile.certifications if profile else None,
        "candidate_resume_url": profile.resume_url if profile else None,
        "candidate_github": profile.github if profile else None,
        "candidate_linkedin": profile.linkedin if profile else None,
        "candidate_portfolio": profile.portfolio if profile else None,
        "job_id": job.id,
        "job_title": job.title,
        "job_description": job.description,
        "job_location": job.location,
        "job_type": job.job_type,
        "work_mode": job.work_mode,
        "salary": job.salary,
        "status": "selected" if app.status == "accepted" else app.status,
        "applied_at": app.applied_at,
        "shortlisted": bool(app.shortlisted),
        "employer_notes": app.employer_notes,
        "interview": {
            "date": app.interview_date,
            "time": app.interview_time,
            "mode": app.interview_mode,
            "link": app.interview_link,
            "interviewer": app.interviewer,
            "round": app.interview_round,
            "instructions": app.interview_instructions,
            "feedback": app.interview_feedback,
            "technical": app.interview_technical,
            "communication": app.interview_communication,
            "problem_solving": app.interview_problem_solving,
            "strengths": app.interview_strengths,
            "improvements": app.interview_improvements,
            "result": app.interview_result,
        },
        "offer": {
            "position": app.offer_position,
            "salary": app.offer_salary,
            "joining_date": app.offer_joining_date,
            "work_location": app.offer_work_location,
            "employment_type": app.offer_employment_type,
            "expiry_date": app.offer_expiry_date,
            "status": app.offer_status or "not_created",
        }
    }

@router.post("/", response_model=schemas.ApplicationOut)
def apply_to_job(application: schemas.ApplicationCreate, db: Session = Depends(get_db), current_user=Depends(require_role("candidate"))):
    job = db.query(models.Job).filter(models.Job.id == application.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    row = models.Application(
        job_id=application.job_id,
        candidate_id=current_user.id,
        status="pending",
        offer_status="not_created"
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row

@router.get("/mine")
def my_applications(db: Session = Depends(get_db), current_user=Depends(require_role("candidate"))):
    rows = db.query(models.Application, models.Job, models.User, models.CompanyProfile).join(
        models.Job, models.Application.job_id == models.Job.id
    ).join(
        models.User, models.Job.employer_id == models.User.id
    ).outerjoin(
        models.CompanyProfile, models.CompanyProfile.user_id == models.User.id
    ).filter(
        models.Application.candidate_id == current_user.id
    ).order_by(models.Application.applied_at.desc()).all()

    return [{
        "application_id": app.id,
        "job_id": job.id,
        "job_title": job.title,
        "job_description": job.description,
        "job_location": job.location,
        "job_type": job.job_type,
        "work_mode": job.work_mode,
        "salary": job.salary,
        "company_name": (company.company_name if company and company.company_name else employer.name),
        "company_about": company.about if company else None,
        "company_industry": company.industry if company else None,
        "company_type": company.company_type if company else None,
        "company_size": company.company_size if company else None,
        "company_headquarters": company.headquarters if company else None,
        "company_website": company.website if company else None,
        "company_work_mode": company.work_mode if company else None,
        "company_preferred_skills": company.preferred_skills if company else None,
        "company_minimum_qualification": company.minimum_qualification if company else None,
        "company_hiring_process": company.hiring_process if company else None,
        "status": "selected" if app.status == "accepted" else app.status,
        "applied_at": app.applied_at,
        "shortlisted": bool(app.shortlisted),
        "interview": {
            "date": app.interview_date, "time": app.interview_time, "mode": app.interview_mode,
            "link": app.interview_link, "interviewer": app.interviewer, "round": app.interview_round,
            "instructions": app.interview_instructions, "feedback": app.interview_feedback,
            "technical": app.interview_technical, "communication": app.interview_communication,
            "problem_solving": app.interview_problem_solving, "strengths": app.interview_strengths,
            "improvements": app.interview_improvements, "result": app.interview_result,
        },
        "offer": {
            "position": app.offer_position, "salary": app.offer_salary, "joining_date": app.offer_joining_date,
            "work_location": app.offer_work_location, "employment_type": app.offer_employment_type,
            "expiry_date": app.offer_expiry_date, "status": app.offer_status or "not_created",
        }
    } for app, job, employer, company in rows]

@router.get("/employer")
def employer_applications(db: Session = Depends(get_db), current_user=Depends(require_role("employer"))):
    rows = db.query(models.Application, models.Job, models.User).join(
        models.Job, models.Application.job_id == models.Job.id
    ).join(
        models.User, models.Application.candidate_id == models.User.id
    ).filter(
        models.Job.employer_id == current_user.id
    ).order_by(models.Application.applied_at.desc()).all()

    result = []
    for app, job, candidate in rows:
        profile = db.query(models.CandidateProfile).filter(models.CandidateProfile.user_id == candidate.id).first()
        result.append(application_payload(app, job, candidate, profile))
    return result

@router.patch("/{application_id}/status")
def update_status(application_id: int, status: str, db: Session = Depends(get_db), current_user=Depends(require_role("employer"))):
    status = status.lower().strip()
    if status not in VALID_STATUSES:
        raise HTTPException(status_code=400, detail="Invalid application status")
    app, _ = get_employer_application(application_id, db, current_user)
    if status == "shortlisted":
        app.shortlisted = True
    if status == "selected":
        app.shortlisted = True
    app.status = status
    db.commit()
    return {"message": "Application status updated", "application_id": app.id, "status": status}

@router.patch("/{application_id}/shortlist")
def toggle_shortlist(application_id: int, shortlisted: bool = True, db: Session = Depends(get_db), current_user=Depends(require_role("employer"))):
    app, _ = get_employer_application(application_id, db, current_user)
    app.shortlisted = shortlisted
    if shortlisted and app.status in {"pending", "review"}:
        app.status = "shortlisted"
    elif not shortlisted and app.status == "shortlisted":
        app.status = "review"
    db.commit()
    return {"shortlisted": app.shortlisted, "status": app.status}

@router.patch("/{application_id}/notes")
def save_notes(application_id: int, payload: schemas.EmployerNotesUpdate, db: Session = Depends(get_db), current_user=Depends(require_role("employer"))):
    app, _ = get_employer_application(application_id, db, current_user)
    app.employer_notes = payload.notes
    db.commit()
    return {"message": "Employer notes saved"}

@router.post("/{application_id}/interview")
def schedule_interview(application_id: int, payload: schemas.InterviewSchedule, db: Session = Depends(get_db), current_user=Depends(require_role("employer"))):
    app, _ = get_employer_application(application_id, db, current_user)
    if not app.shortlisted and app.status != "shortlisted":
        raise HTTPException(status_code=400, detail="Shortlist the candidate before scheduling an interview")
    if payload.mode not in INTERVIEW_MODES:
        raise HTTPException(status_code=400, detail="Interview mode must be Online or Offline")
    if payload.mode == "Online" and not payload.meeting_link:
        raise HTTPException(status_code=400, detail="Meeting link is required for an online interview")

    app.interview_date = payload.date
    app.interview_time = payload.time
    app.interview_mode = payload.mode
    app.interview_link = payload.meeting_link
    app.interviewer = payload.interviewer
    app.interview_round = payload.round
    app.interview_instructions = payload.instructions
    app.status = "interview"
    db.commit()
    return {"message": "Interview scheduled", "status": app.status}

@router.patch("/{application_id}/interview-feedback")
def save_interview_feedback(application_id: int, payload: schemas.InterviewFeedback, db: Session = Depends(get_db), current_user=Depends(require_role("employer"))):
    app, _ = get_employer_application(application_id, db, current_user)
    if not app.interview_date:
        raise HTTPException(status_code=400, detail="Schedule an interview first")
    if payload.result not in {"passed", "failed", "next_round"}:
        raise HTTPException(status_code=400, detail="Result must be passed, failed or next_round")

    app.interview_feedback = payload.remarks
    app.interview_technical = payload.technical
    app.interview_communication = payload.communication
    app.interview_problem_solving = payload.problem_solving
    app.interview_strengths = payload.strengths
    app.interview_improvements = payload.improvements
    app.interview_result = payload.result
    if payload.result == "passed":
        app.status = "selected"
    elif payload.result == "failed":
        app.status = "rejected"
    else:
        app.status = "interview"
    db.commit()
    return {"message": "Interview feedback saved", "status": app.status}

@router.post("/{application_id}/offer")
def create_offer(application_id: int, payload: schemas.OfferCreate, db: Session = Depends(get_db), current_user=Depends(require_role("employer"))):
    app, _ = get_employer_application(application_id, db, current_user)
    if app.status not in {"selected", "accepted"}:
        raise HTTPException(status_code=400, detail="Select the candidate before creating an offer")

    app.offer_position = payload.position
    app.offer_salary = payload.salary
    app.offer_joining_date = payload.joining_date
    app.offer_work_location = payload.work_location
    app.offer_employment_type = payload.employment_type
    app.offer_expiry_date = payload.expiry_date
    app.offer_status = "sent"
    db.commit()
    return {"message": "Offer created and sent", "offer_status": app.offer_status}

@router.patch("/{application_id}/offer-response")
def offer_response(application_id: int, response: str, db: Session = Depends(get_db), current_user=Depends(require_role("candidate"))):
    response = response.lower().strip()
    if response not in {"accepted", "declined"}:
        raise HTTPException(status_code=400, detail="Offer response must be accepted or declined")
    app = db.query(models.Application).filter(
        models.Application.id == application_id,
        models.Application.candidate_id == current_user.id
    ).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    if app.offer_status != "sent":
        raise HTTPException(status_code=400, detail="No active offer is available")
    app.offer_status = response
    db.commit()
    return {"message": f"Offer {response}", "offer_status": response}

@router.get("/notifications")
def notifications(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role == "employer":
        rows = db.query(models.Application, models.Job, models.User).join(
            models.Job, models.Application.job_id == models.Job.id
        ).join(
            models.User, models.Application.candidate_id == models.User.id
        ).filter(models.Job.employer_id == current_user.id).order_by(models.Application.applied_at.desc()).limit(10).all()
        items = []
        for app, job, candidate in rows:
            items.append({
                "type": "application",
                "message": f"{candidate.name} applied for {job.title}",
                "job_title": job.title,
                "candidate_name": candidate.name,
                "status": app.status,
                "created_at": app.applied_at
            })
            if app.offer_status == "accepted":
                items.append({"type":"offer","message":f"{candidate.name} accepted the offer for {job.title}","created_at":app.applied_at})
            elif app.offer_status == "declined":
                items.append({"type":"offer","message":f"{candidate.name} declined the offer for {job.title}","created_at":app.applied_at})
        return items[:10]

    rows = db.query(models.Application, models.Job).join(
        models.Job, models.Application.job_id == models.Job.id
    ).filter(models.Application.candidate_id == current_user.id).order_by(models.Application.applied_at.desc()).limit(10).all()
    items = []
    for app, job in rows:
        items.append({
            "type": "application_update",
            "message": f"Your application for {job.title} is {'selected' if app.status == 'accepted' else app.status}",
            "job_title": job.title,
            "status": "selected" if app.status == "accepted" else app.status,
            "created_at": app.applied_at
        })
        if app.interview_date:
            items.append({"type":"interview","message":f"Interview scheduled for {job.title} on {app.interview_date} at {app.interview_time or 'the scheduled time'}","created_at":app.applied_at})
        if app.offer_status == "sent":
            items.append({"type":"offer","message":f"You have a new offer for {job.title}","created_at":app.applied_at})
    return items[:10]

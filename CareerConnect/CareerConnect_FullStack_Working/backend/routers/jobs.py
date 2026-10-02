from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from auth import require_role

router = APIRouter(prefix="/jobs", tags=["Jobs"])

def job_payload(job, company=None):
    return {
        "id": job.id,
        "title": job.title,
        "description": job.description,
        "location": job.location,
        "job_type": job.job_type,
        "work_mode": job.work_mode,
        "skills": job.skills,
        "salary": job.salary,
        "employer_id": job.employer_id,
        "created_at": job.created_at,
        "company_name": (company.company_name if company and company.company_name else None),
        "company_industry": company.industry if company else None,
        "company_type": company.company_type if company else None,
        "company_size": company.company_size if company else None,
        "company_headquarters": company.headquarters if company else None,
        "company_website": company.website if company else None,
        "company_about": company.about if company else None,
        "company_work_mode": company.work_mode if company else None,
        "company_preferred_skills": company.preferred_skills if company else None,
        "company_minimum_qualification": company.minimum_qualification if company else None,
        "company_hiring_process": company.hiring_process if company else None,
    }

def get_job_with_company(db, job_id):
    row = db.query(models.Job, models.CompanyProfile).outerjoin(
        models.CompanyProfile, models.CompanyProfile.user_id == models.Job.employer_id
    ).filter(models.Job.id == job_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Job not found")
    return row

@router.get("/", response_model=list[schemas.JobOut])
def list_jobs(db: Session = Depends(get_db)):
    rows = db.query(models.Job, models.CompanyProfile).outerjoin(
        models.CompanyProfile, models.CompanyProfile.user_id == models.Job.employer_id
    ).order_by(models.Job.created_at.desc()).all()
    return [job_payload(job, company) for job, company in rows]

@router.get("/mine", response_model=list[schemas.JobOut])
def my_jobs(db: Session = Depends(get_db), current_user=Depends(require_role("employer"))):
    rows = db.query(models.Job, models.CompanyProfile).outerjoin(
        models.CompanyProfile, models.CompanyProfile.user_id == models.Job.employer_id
    ).filter(models.Job.employer_id == current_user.id).order_by(models.Job.created_at.desc()).all()
    return [job_payload(job, company) for job, company in rows]

@router.post("/", response_model=schemas.JobOut)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db), current_user=Depends(require_role("employer"))):
    new_job = models.Job(**job.model_dump(), employer_id=current_user.id)
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    company = db.query(models.CompanyProfile).filter(models.CompanyProfile.user_id == current_user.id).first()
    return job_payload(new_job, company)

@router.get("/{job_id}", response_model=schemas.JobOut)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job, company = get_job_with_company(db, job_id)
    return job_payload(job, company)

@router.patch("/{job_id}", response_model=schemas.JobOut)
def update_job(job_id: int, data: schemas.JobUpdate, db: Session = Depends(get_db), current_user=Depends(require_role("employer"))):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.employer_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only edit your own jobs")
    for key, value in data.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(job, key, value)
    db.commit()
    db.refresh(job)
    company = db.query(models.CompanyProfile).filter(models.CompanyProfile.user_id == current_user.id).first()
    return job_payload(job, company)

@router.delete("/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db), current_user=Depends(require_role("employer"))):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.employer_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own jobs")
    db.delete(job)
    db.commit()
    return {"message": "Job deleted"}

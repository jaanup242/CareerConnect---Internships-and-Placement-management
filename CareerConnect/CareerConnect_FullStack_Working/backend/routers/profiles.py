from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from auth import require_role

router = APIRouter(tags=["Profiles"])

@router.get("/candidate-profile/me", response_model=schemas.CandidateProfileOut)
def get_candidate_profile(db: Session = Depends(get_db), current_user=Depends(require_role("candidate"))):
    profile = db.query(models.CandidateProfile).filter(models.CandidateProfile.user_id == current_user.id).first()
    if not profile:
        profile = models.CandidateProfile(user_id=current_user.id)
        db.add(profile); db.commit(); db.refresh(profile)
    return profile

@router.put("/candidate-profile/me", response_model=schemas.CandidateProfileOut)
def update_candidate_profile(data: schemas.CandidateProfileBase, db: Session = Depends(get_db), current_user=Depends(require_role("candidate"))):
    profile = db.query(models.CandidateProfile).filter(models.CandidateProfile.user_id == current_user.id).first()
    if not profile:
        profile = models.CandidateProfile(user_id=current_user.id)
        db.add(profile)
    for key, value in data.model_dump().items():
        setattr(profile, key, value)
    db.commit(); db.refresh(profile)
    return profile

@router.get("/company-profile/me", response_model=schemas.CompanyProfileOut)
def get_company_profile(db: Session = Depends(get_db), current_user=Depends(require_role("employer"))):
    profile = db.query(models.CompanyProfile).filter(models.CompanyProfile.user_id == current_user.id).first()
    if not profile:
        profile = models.CompanyProfile(user_id=current_user.id, company_name=current_user.name)
        db.add(profile); db.commit(); db.refresh(profile)
    return profile

@router.put("/company-profile/me", response_model=schemas.CompanyProfileOut)
def update_company_profile(data: schemas.CompanyProfileBase, db: Session = Depends(get_db), current_user=Depends(require_role("employer"))):
    profile = db.query(models.CompanyProfile).filter(models.CompanyProfile.user_id == current_user.id).first()
    if not profile:
        profile = models.CompanyProfile(user_id=current_user.id)
        db.add(profile)
    for key, value in data.model_dump().items():
        setattr(profile, key, value)
    db.commit(); db.refresh(profile)
    return profile


@router.get("/candidate-profile/{user_id}")
def get_candidate_profile_for_employer(user_id: int, db: Session = Depends(get_db), current_user=Depends(require_role("employer"))):
    candidate = db.query(models.User).filter(models.User.id == user_id, models.User.role == "candidate").first()
    if not candidate:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Candidate not found")
    # Employers may view candidates who have applied to one of their jobs.
    allowed = db.query(models.Application).join(
        models.Job, models.Application.job_id == models.Job.id
    ).filter(
        models.Application.candidate_id == user_id,
        models.Job.employer_id == current_user.id
    ).first()
    if not allowed:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="You can only view profiles of your applicants")
    profile = db.query(models.CandidateProfile).filter(models.CandidateProfile.user_id == user_id).first()
    if not profile:
        profile = models.CandidateProfile(user_id=user_id)
        db.add(profile); db.commit(); db.refresh(profile)
    data = {k: getattr(profile, k) for k in schemas.CandidateProfileBase.model_fields.keys()}
    data.update({"id": profile.id, "user_id": profile.user_id, "name": candidate.name, "email": candidate.email})
    return data

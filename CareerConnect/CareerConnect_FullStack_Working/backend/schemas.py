from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=6)
    role: str

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class JobCreate(BaseModel):
    title: str
    description: str
    location: Optional[str] = None
    job_type: str = "Internship"
    work_mode: str = "Remote"
    skills: Optional[str] = None
    salary: Optional[str] = None

class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    work_mode: Optional[str] = None
    skills: Optional[str] = None
    salary: Optional[str] = None

class JobOut(BaseModel):
    id: int
    title: str
    description: str
    location: Optional[str]
    job_type: str
    work_mode: str
    skills: Optional[str]
    salary: Optional[str]
    employer_id: int
    created_at: datetime
    # Company profile information returned with every job so the
    # candidate Browse Jobs / job-details page can display it.
    company_name: Optional[str] = None
    company_industry: Optional[str] = None
    company_type: Optional[str] = None
    company_size: Optional[str] = None
    company_headquarters: Optional[str] = None
    company_website: Optional[str] = None
    company_about: Optional[str] = None
    company_work_mode: Optional[str] = None
    company_preferred_skills: Optional[str] = None
    company_minimum_qualification: Optional[str] = None
    company_hiring_process: Optional[str] = None
    class Config:
        from_attributes = True

class ApplicationCreate(BaseModel):
    job_id: int

class ApplicationOut(BaseModel):
    id: int
    job_id: int
    candidate_id: int
    status: str
    applied_at: datetime
    class Config:
        from_attributes = True


class EmployerNotesUpdate(BaseModel):
    notes: Optional[str] = None

class InterviewSchedule(BaseModel):
    date: str
    time: str
    mode: str
    meeting_link: Optional[str] = None
    interviewer: Optional[str] = None
    round: Optional[str] = None
    instructions: Optional[str] = None

class InterviewFeedback(BaseModel):
    technical: Optional[str] = None
    communication: Optional[str] = None
    problem_solving: Optional[str] = None
    strengths: Optional[str] = None
    improvements: Optional[str] = None
    remarks: Optional[str] = None
    result: str

class OfferCreate(BaseModel):
    position: str
    salary: str
    joining_date: str
    work_location: str
    employment_type: str
    expiry_date: str

class CandidateProfileBase(BaseModel):
    phone: Optional[str] = None
    location: Optional[str] = None
    about: Optional[str] = None
    date_of_birth: Optional[str] = None
    college: Optional[str] = None
    degree: Optional[str] = None
    branch: Optional[str] = None
    current_year: Optional[str] = None
    graduation_year: Optional[str] = None
    cgpa: Optional[str] = None
    qualifications: Optional[str] = None
    skills: Optional[str] = None
    projects: Optional[str] = None
    experience: Optional[str] = None
    achievements: Optional[str] = None
    certifications: Optional[str] = None
    resume_url: Optional[str] = None
    github: Optional[str] = None
    linkedin: Optional[str] = None
    portfolio: Optional[str] = None

class CandidateProfileOut(CandidateProfileBase):
    id: int
    user_id: int
    class Config:
        from_attributes = True

class CompanyProfileBase(BaseModel):
    company_name: Optional[str] = None
    industry: Optional[str] = None
    company_type: Optional[str] = None
    founded_year: Optional[str] = None
    company_size: Optional[str] = None
    headquarters: Optional[str] = None
    website: Optional[str] = None
    about: Optional[str] = None
    hiring_positions: Optional[str] = None
    departments: Optional[str] = None
    internships: Optional[str] = None
    full_time: Optional[str] = None
    work_mode: Optional[str] = None
    preferred_skills: Optional[str] = None
    minimum_qualification: Optional[str] = None
    hiring_process: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None

class CompanyProfileOut(CompanyProfileBase):
    id: int
    user_id: int
    class Config:
        from_attributes = True

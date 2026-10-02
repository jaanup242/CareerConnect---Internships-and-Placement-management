from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean, func
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)  # candidate / employer
    created_at = Column(DateTime, server_default=func.now())

    jobs_posted = relationship("Job", back_populates="employer", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="candidate", cascade="all, delete-orphan")
    candidate_profile = relationship("CandidateProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    company_profile = relationship("CompanyProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String(150))
    job_type = Column(String(40), default="Internship", nullable=False)
    work_mode = Column(String(40), default="Remote", nullable=False)
    skills = Column(String(500))
    salary = Column(String(100))
    employer_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    employer = relationship("User", back_populates="jobs_posted")
    applications = relationship("Application", back_populates="job", cascade="all, delete-orphan")


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    candidate_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(30), default="pending", nullable=False)
    applied_at = Column(DateTime, server_default=func.now())

    # Employer-side hiring workflow
    shortlisted = Column(Boolean, default=False, nullable=False)
    employer_notes = Column(Text)

    # Interview
    interview_date = Column(String(30))
    interview_time = Column(String(20))
    interview_mode = Column(String(20))
    interview_link = Column(String(500))
    interviewer = Column(String(150))
    interview_round = Column(String(100))
    interview_instructions = Column(Text)
    interview_feedback = Column(Text)
    interview_technical = Column(String(20))
    interview_communication = Column(String(20))
    interview_problem_solving = Column(String(20))
    interview_strengths = Column(Text)
    interview_improvements = Column(Text)
    interview_result = Column(String(30))

    # Offer
    offer_position = Column(String(150))
    offer_salary = Column(String(100))
    offer_joining_date = Column(String(30))
    offer_work_location = Column(String(150))
    offer_employment_type = Column(String(60))
    offer_expiry_date = Column(String(30))
    offer_status = Column(String(30), default="not_created", nullable=False)

    job = relationship("Job", back_populates="applications")
    candidate = relationship("User", back_populates="applications")


class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    phone = Column(String(30))
    location = Column(String(150))
    about = Column(Text)
    date_of_birth = Column(String(20))
    college = Column(String(200))
    degree = Column(String(150))
    branch = Column(String(150))
    current_year = Column(String(50))
    graduation_year = Column(String(20))
    cgpa = Column(String(30))
    qualifications = Column(Text)
    skills = Column(Text)
    projects = Column(Text)
    experience = Column(Text)
    achievements = Column(Text)
    certifications = Column(Text)
    resume_url = Column(String(500))
    github = Column(String(300))
    linkedin = Column(String(300))
    portfolio = Column(String(300))

    user = relationship("User", back_populates="candidate_profile")


class CompanyProfile(Base):
    __tablename__ = "company_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    company_name = Column(String(200))
    industry = Column(String(150))
    company_type = Column(String(100))
    founded_year = Column(String(20))
    company_size = Column(String(50))
    headquarters = Column(String(150))
    website = Column(String(300))
    about = Column(Text)
    hiring_positions = Column(Text)
    departments = Column(Text)
    internships = Column(String(20))
    full_time = Column(String(20))
    work_mode = Column(String(50))
    preferred_skills = Column(Text)
    minimum_qualification = Column(String(250))
    hiring_process = Column(Text)
    linkedin = Column(String(300))
    github = Column(String(300))

    user = relationship("User", back_populates="company_profile")

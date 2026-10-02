-- Run this in MySQL Workbench if you are connecting to your EXISTING careerconnect database.
USE careerconnect;

ALTER TABLE users MODIFY COLUMN hashed_password VARCHAR(255) NOT NULL;

ALTER TABLE jobs
  ADD COLUMN job_type VARCHAR(40) NOT NULL DEFAULT 'Internship',
  ADD COLUMN work_mode VARCHAR(40) NOT NULL DEFAULT 'Remote',
  ADD COLUMN skills VARCHAR(500) NULL,
  ADD COLUMN salary VARCHAR(100) NULL;

CREATE TABLE IF NOT EXISTS candidate_profiles (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL UNIQUE,
  phone VARCHAR(30),
  location VARCHAR(150),
  about TEXT,
  date_of_birth VARCHAR(20),
  college VARCHAR(200),
  degree VARCHAR(150),
  branch VARCHAR(150),
  current_year VARCHAR(50),
  graduation_year VARCHAR(20),
  cgpa VARCHAR(30),
  qualifications TEXT,
  skills TEXT,
  projects TEXT,
  experience TEXT,
  achievements TEXT,
  certifications TEXT,
  resume_url VARCHAR(500),
  github VARCHAR(300),
  linkedin VARCHAR(300),
  portfolio VARCHAR(300),
  CONSTRAINT fk_candidate_profile_user
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS company_profiles (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL UNIQUE,
  company_name VARCHAR(200),
  industry VARCHAR(150),
  company_type VARCHAR(100),
  founded_year VARCHAR(20),
  company_size VARCHAR(50),
  headquarters VARCHAR(150),
  website VARCHAR(300),
  about TEXT,
  hiring_positions TEXT,
  departments TEXT,
  internships VARCHAR(20),
  full_time VARCHAR(20),
  work_mode VARCHAR(50),
  preferred_skills TEXT,
  minimum_qualification VARCHAR(250),
  hiring_process TEXT,
  linkedin VARCHAR(300),
  github VARCHAR(300),
  CONSTRAINT fk_company_profile_user
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);


-- The application startup code also auto-adds the employer hiring workflow
-- columns to an existing database (interview, notes, shortlist and offer).
-- Restart Uvicorn after updating the code; no database recreation is needed.

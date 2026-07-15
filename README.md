# AI-Powered Multi-Agent Career Intelligence System with Predictive Analytics

## Project Type

**Final Year B.Tech Major Project**

**Duration:** 2 Semesters

- **Semester 7:** Research, Backend Development, Authentication, Resume Intelligence, ATS Analysis
- **Semester 8:** AI Mock Interview, Multi-Agent AI, Predictive Analytics, Deployment

---

# Overview

The **AI-Powered Multi-Agent Career Intelligence System with Predictive Analytics** is an intelligent web platform designed to enhance students' placement readiness using **Artificial Intelligence (AI)**, **Natural Language Processing (NLP)**, **Machine Learning (ML)**, **Predictive Analytics**, and **Computer Vision**.

The platform provides an end-to-end career preparation ecosystem by automatically analyzing resumes, evaluating ATS compatibility, identifying skill gaps, recommending learning paths, conducting AI-powered mock interviews, predicting placement readiness, and providing multilingual career assistance.

The current implementation includes:

- JWT-based Authentication
- User Profile Management
- Resume Upload & Validation
- Resume Parsing (PDF & DOCX)
- Resume Text Extraction
- ATS Score Analysis
- Resume Improvement Suggestions
- Resume History
- Resume Details
- Career Recommendation Engine
- Skill Extraction
- Career Match Score Calculation
- Missing Skill Detection
- AI Career Summary Generation
- Recommendation History
- Career Details API
- Secure REST APIs
- PostgreSQL Database Integration

Future phases will extend the platform with AI-powered interviews, resume-to-job matching, predictive analytics, multilingual assistance, and multi-agent AI collaboration.

---

# Project Objectives

The primary objectives of this project are:

- Build an intelligent AI-powered career guidance platform.
- Analyze resumes using Natural Language Processing.
- Calculate ATS compatibility scores.
- Detect technical and non-technical skill gaps.
- Recommend personalized learning paths.
- Conduct AI-powered mock interviews.
- Perform AI-based proctored interviews.
- Predict placement readiness using Machine Learning.
- Support multilingual career guidance.
- Provide an analytics dashboard for tracking overall progress.
- Recommend suitable careers based on extracted resume skills.
- Calculate career match scores.
- Detect missing skills required for recommended careers.
- Generate AI-powered career summaries.
- Store recommendation history for future reference.

---

# Key Features

## ✅ Implemented Features

### Authentication
- User Registration
- User Login (JWT Authentication)
- Protected APIs
- User Profile Management

### Resume Intelligence
- Resume Upload
- PDF & DOCX Validation
- File Size Validation (5 MB)
- Resume Parsing
- Resume Text Extraction
- ATS Score Analysis
- Resume Improvement Suggestions
- Resume History
- Resume Details
- Resume Deletion

### Security
- JWT Authentication
- User-specific Resume Access
- Protected Resume APIs
- Protected User APIs

### Career Recommendation

- Skill Extraction
- Career Recommendation Engine
- Career Match Score Calculation
- Missing Skill Detection
- AI Career Summary Generation
- Recommendation History
- Career Details

### AI Features
- Recommendation Engine

---

## 🚧 Planned Features

### Career Intelligence
- Skill Gap Detection
- Resume-to-Job Matching
- Personalized Career Roadmap
- AI Career Assistant

### Interview Intelligence
- AI Mock Interview
- Adaptive Interview System
- Voice-Based Interview Assessment
- AI Proctored Interview

### Predictive Analytics
- Placement Readiness Prediction
- Performance Forecasting
- Learning Progress Analysis
- Analytics Dashboard

### AI Features
- Multi-Agent AI
- Multilingual AI Assistant
- GitHub Portfolio Analyzer

---

# Technology Stack

## Frontend
- Next.js
- Tailwind CSS
- TypeScript

## Backend
- FastAPI
- Python

## Database
- PostgreSQL
- SQLAlchemy
- Alembic

## Authentication
- JWT
- Passlib
- bcrypt

## Resume Processing
- pdfplumber
- python-docx
- python-multipart

## AI / NLP

### Currently Used
- pdfplumber
- python-docx

### Planned
- spaCy
- Hugging Face Transformers
- Google Gemini API
- LangChain
- CrewAI

## Machine Learning

### Planned
- Scikit-learn
- XGBoost
- Pandas
- NumPy

## Computer Vision *(Planned)*
- OpenCV
- MediaPipe

## Speech Processing *(Planned)*
- Whisper

## Visualization *(Planned)*
- Plotly
- Matplotlib

---

# Project Structure

```text
Career-Intelligence-System/
│
├── backend/
│   ├── alembic/
│   │   ├── versions/
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── README
│   │
│   ├── app/
│   │   ├── config/
│   │   │   └── settings.py
│   │   │
│   │   ├── core/
│   │   │   └── security.py
│   │   │
│   │   ├── database/
│   │   │   ├── base.py
│   │   │   └── database.py
│   │   │
│   │   ├── dependencies/
│   │   │   └── auth_dependencies.py
│   │   │
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── resume.py
│   │   │   ├── career.py
│   │   │   ├── recommendation.py
│   │   │   ├── skill.py
│   │   │   ├── career_skill.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── resume.py
│   │   │   └── recommendation_router.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── user.py
│   │   │   ├── resume.py
│   │   │   ├── recommendation.py
│   │   │   └── token.py
│   │   │
│   │   ├── services/
│   │   │   ├── recommendation_service.py
│   │   │   └── career_summary_service.py
│   │   │
│   │   ├── utils/
│   │   │   ├── ats_analyzer.py
│   │   │   ├── resume_parser.py
│   │   │   ├── skill_extractor.py
│   │   │   └── suggestion_generator.py
│   │   │
│   │   └── main.py
│   │
│   ├── uploads/
│   ├── tests/
│   ├── logs/
│   ├── .env
│   ├── alembic.ini
│   ├── requirements.txt
│   └── main.py
│
├── datasets/
│   ├── careers.csv
│   ├── skills.json
│   └── learning_resources.json
│
├── docs/
├── notebooks/
├── scripts/
│   ├── import_careers.py
│   ├── import_skills.py
│   ├── seed_database.py
│   └── test_save_recommendation.py
│
├── frontend/
├── assets/
├── README.md
└── .gitignore
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/<your-username>/Career-Intelligence-System.git
```

---

## Navigate to Backend

```bash
cd Career-Intelligence-System/backend
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

---

## Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file inside the backend directory.

```env
DATABASE_URL=postgresql://postgres:password@localhost/career_intelligence_db

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## Database Migration

Apply all migrations

```bash
alembic upgrade head
```

Create a new migration

```bash
alembic revision --autogenerate -m "migration_name"
```

---

## Run the Backend

```bash
uvicorn main:app --reload
```

---

## Swagger Documentation

```
http://127.0.0.1:8000/docs
```

---

# Resume Workflow

```text
User Registration
        │
        ▼
User Login
        │
        ▼
Upload Resume
        │
        ▼
Resume Validation
        │
        ▼
Resume Parsing
        │
        ▼
Extract Resume Text
        │
        ▼
Calculate ATS Score
        │
        ▼
Generate Resume Suggestions
        │
        ▼
Extract Skills
        │
        ▼
Generate Career Recommendation
        │
        ▼
Calculate Match Score
        │
        ▼
Detect Missing Skills
        │
        ▼
Generate AI Career Summary
        │
        ▼
Save Recommendation
        │
        ▼
Recommendation History
        │
        ▼
Career Details
        │
        ▼
Resume History
        │
        ▼
Resume Details
        │
        ▼
Delete Resume
```

---

# REST APIs

## Authentication APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | User login |

---

## User APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/users/profile` | Get profile |
| PUT | `/users/profile` | Update profile |
| DELETE | `/users/profile` | Deactivate account |

---

## Resume APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/resume/upload` | Upload resume |
| GET | `/resume/parse/{resume_id}` | Parse resume |
| GET | `/resume/ats/{resume_id}` | Calculate ATS score |
| GET | `/resume/suggestions/{resume_id}` | Generate suggestions |
| GET | `/resume/history` | Resume history |
| GET | `/resume/{resume_id}` | Resume details |
| DELETE | `/resume/{resume_id}` | Delete resume |

---

## Career Recommendation APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/career/recommend` | Generate career recommendation |
| GET | `/api/career/history` | View recommendation history |
| GET | `/api/career/{career_id}` | View career details |

# Career Recommendation Algorithm

The recommendation engine performs the following steps:

1. Parse the uploaded resume.
2. Extract technical skills.
3. Compare extracted skills with the required skills of every career.
4. Calculate a match score.
5. Detect missing skills.
6. Select the highest matching career.
7. Generate an AI-powered summary.
8. Save the recommendation in PostgreSQL.

# AI Summary Generation

The recommendation engine automatically generates:

- Recommended Career
- Match Score
- Strengths
- Missing Skills
- Learning Resources
- Career Summary

Each recommendation is stored in the database and can be retrieved through the Recommendation History API.

# ATS Analysis

The ATS engine evaluates resumes using multiple criteria, including:

- Contact Information
- Education
- Technical Skills
- Work Experience
- Projects
- Certifications
- Achievements

The system:

- Extracts resume text
- Calculates an ATS score
- Stores ATS results
- Generates personalized improvement suggestions

---

# Current Backend Features

## Authentication

- JWT Authentication

## Resume Intelligence

- Resume Upload
- Resume Parsing
- ATS Score
- Resume Suggestions
- Resume History

## Career Recommendation

- Skill Extraction
- Career Matching
- Match Score Calculation
- Missing Skill Detection
- AI Summary Generation
- Recommendation History
- Career Details API

## Database

- PostgreSQL
- SQLAlchemy
- Alembic

---

# Development Phases

- ✅ Phase 1 – Project Planning & Environment Setup
- ✅ Phase 2 – Backend Foundation & FastAPI Setup
- ✅ Phase 3 – Database Design & User Authentication
- ✅ Phase 4 – Resume Management Module
- ✅ Phase 5 – Career Recommendation Engine
- ⏳ Phase 6 – AI Career Assistant
- ⏳ Phase 7 – Recommendation Engine
- ⏳ Phase 8 – AI Mock Interview
- ⏳ Phase 9 – Voice-Based Interview Analysis
- ⏳ Phase 10 – AI Proctored Interview
- ⏳ Phase 11 – Placement Readiness Prediction
- ⏳ Phase 12 – Analytics Dashboard
- ⏳ Phase 13 – GitHub Portfolio Analyzer
- ⏳ Phase 14 – Multi-Agent AI Integration
- ⏳ Phase 15 – Deployment & Production

---

# Testing

## Career Recommendation

- ✅ Skill Extraction
- ✅ Career Recommendation
- ✅ Match Score Calculation
- ✅ Missing Skill Detection
- ✅ Recommendation History
- ✅ Career Details
- ✅ Authentication
- ✅ Error Handling

The backend has been tested using **Swagger UI**.

## Authentication

- ✅ User Registration
- ✅ User Login
- ✅ JWT Authorization

## Resume Module

- ✅ Upload PDF
- ✅ Upload DOCX
- ✅ Invalid File Validation
- ✅ File Size Validation
- ✅ Resume Parsing
- ✅ ATS Score Analysis
- ✅ Resume Suggestions
- ✅ Resume History
- ✅ Resume Details
- ✅ Resume Deletion

## Security

- ✅ Unauthorized Access (401)
- ✅ Cross-user Access Protection
- ✅ Protected APIs

---

# Current Status

## Completed

- ✅ Authentication & Authorization Module
- ✅ User Profile Management Module
- ✅ Resume Management Module
- ✅ ATS Analysis Module
- ✅ Career Recommendation Engine

## Upcoming

- AI Career Assistant
- Resume-to-Job Matching
- AI Mock Interview
- Placement Readiness Prediction
- Multi-Agent AI

---

# Future Scope

Potential future enhancements include:

- AI Resume Builder
- Company Recruitment Portal
- LinkedIn Integration
- AI Avatar-Based Interviewer
- Mobile Application (Android & iOS)
- Cloud Deployment
- Real-Time Placement Analytics
- Industry Skill Trend Prediction
- AI Mentor Recommendation System

---

# Repository Status

🚧 **Under Active Development**

This repository is actively being developed as part of a **Final Year B.Tech Major Project**.

The backend currently includes:

- ✅ JWT Authentication
- ✅ User Profile Management
- ✅ Resume Intelligence
- ✅ ATS Analysis
- ✅ Career Recommendation Engine

Future development will focus on AI Career Assistant, AI Mock Interview, Placement Readiness Prediction, Multi-Agent AI, and deployment.

---

# Author

**Subin Paul**

Bachelor of Technology (B.Tech)

Final Year Major Project

---

# License

This project is developed for **academic, educational, and research purposes**.

All rights reserved by the author.
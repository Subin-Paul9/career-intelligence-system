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
- Recommendation Engine

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
│   ├── app/
│   │   ├── core/
│   │   ├── database/
│   │   ├── dependencies/
│   │   ├── models/
│   │   ├── routers/
│   │   ├── schemas/
│   │   ├── utils/
│   │   └── main.py
│   │
│   ├── uploads/
│   ├── tests/
│   ├── logs/
│   ├── .env
│   ├── alembic.ini
│   └── requirements.txt
│
├── frontend/
├── datasets/
├── docs/
├── notebooks/
├── scripts/
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
Generate Suggestions
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

- JWT Authentication
- User Profile APIs
- Resume Upload
- Resume Validation
- Resume Parsing
- Resume Text Extraction
- ATS Score Calculation
- Resume Suggestions
- Resume History
- Resume Details
- Resume Delete
- PostgreSQL Integration
- Alembic Database Migrations
- Swagger API Documentation

---

# Development Phases

- ✅ Phase 1 – Project Planning & Environment Setup
- ✅ Phase 2 – Backend Foundation & FastAPI Setup
- ✅ Phase 3 – Database Design & User Authentication
- ✅ Phase 4 – Resume Management Module
- 🚧 Phase 5 – Job Description Matching
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

- ✅ Authentication Module
- ✅ User Profile Module
- ✅ Resume Management Module

## In Progress

- 🚧 Job Description Matching Module

## Upcoming

- AI Career Assistant
- Resume-to-Job Matching
- Recommendation Engine
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

The backend authentication and resume management modules are complete, and additional AI-powered features will be implemented in future development phases.

---

# Author

**Subin Paul**

Bachelor of Technology (B.Tech)

Final Year Major Project

---

# License

This project is developed for **academic, educational, and research purposes**.

All rights reserved by the author.
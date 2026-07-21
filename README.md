# AI-Powered Multi-Agent Career Intelligence System with Predictive Analytics

## Project Type

**Final Year B.Tech Major Project**

**Duration:** 2 Semesters

- **Semester 7:** Research, Backend Development, Authentication, Resume Intelligence, Career Intelligence, AI Career Assistant
- **Semester 8:** AI Mock Interview, Multi-Agent AI, Predictive Analytics, Analytics Dashboard, Deployment

---

# Overview

The **AI-Powered Multi-Agent Career Intelligence System with Predictive Analytics** is a full-stack AI-powered platform designed to improve students' placement readiness through intelligent resume analysis, personalized career guidance, and predictive career analytics.

The platform combines **Artificial Intelligence (AI)**, **Natural Language Processing (NLP)**, **Large Language Models (LLMs)**, **Machine Learning (ML)**, and **Predictive Analytics** to provide an end-to-end career preparation ecosystem.

The system assists students throughout their placement journey by:

- Analyzing resumes
- Calculating ATS compatibility scores
- Identifying skill gaps
- Recommending suitable career paths
- Suggesting learning resources
- Generating personalized career roadmaps
- Providing AI-powered career guidance using Google Gemini
- Maintaining AI conversation history
- Recommending projects and certifications
- Predicting placement readiness (upcoming)
- Conducting AI-powered mock interviews (upcoming)

---

## Current Backend Implementation

### Authentication

- JWT Authentication
- User Registration & Login
- User Profile Management
- Protected APIs

### Resume Intelligence

- Resume Upload & Validation
- PDF & DOCX Parsing
- Resume Text Extraction
- ATS Score Analysis
- Resume Improvement Suggestions
- Resume History
- Resume Details

### Career Intelligence

- Skill Extraction
- Career Recommendation Engine
- Career Match Score Calculation
- Missing Skill Detection
- AI Career Summary Generation
- Recommendation History
- Career Details

### AI Career Assistant

- Google Gemini Integration
- Personalized AI Career Assistant
- Conversation Management
- Conversation History
- Career Comparison
- Career Roadmap Generator
- Project Recommendations
- Certification Recommendations
- Learning Resource Recommendations
- AI Feedback System

### Security

- JWT Authentication
- User-specific Data Isolation
- Prompt Injection Filtering
- API Key Protection
- Input Validation
- Rate Limiting
- Output Sanitization

---

Future phases will extend the platform with:

- Resume-to-Job Matching
- AI Mock Interview
- Voice-Based Interview Analysis
- AI Proctored Interview
- Placement Readiness Prediction
- Analytics Dashboard
- GitHub Portfolio Analyzer
- LinkedIn Portfolio Analyzer
- Multi-Agent AI Collaboration
- Cloud Deployment

---

# Project Objectives

The primary objectives of this project are:

- Build an intelligent AI-powered career guidance platform.
- Analyze resumes using NLP techniques.
- Calculate ATS compatibility scores.
- Recommend suitable career paths based on resume skills.
- Detect technical and non-technical skill gaps.
- Recommend personalized learning resources.
- Generate AI-powered career summaries.
- Provide an intelligent conversational AI Career Assistant.
- Generate personalized career roadmaps.
- Recommend projects and professional certifications.
- Conduct AI-powered mock interviews.
- Predict placement readiness using Machine Learning.
- Provide analytics dashboards for career progress.
- Support future Multi-Agent AI collaboration.

# Key Features

## ✅ Implemented Features

### 🔐 Authentication & User Management

- User Registration
- User Login (JWT Authentication)
- Secure Password Hashing (bcrypt)
- JWT Token-Based Authorization
- Protected REST APIs
- User Profile Management
- User-specific Data Access

---

### 📄 Resume Intelligence

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

---

### 🎯 Career Recommendation Engine

- Technical Skill Extraction
- Career Recommendation Engine
- Career Match Score Calculation
- Missing Skill Detection
- AI Career Summary Generation
- Recommendation History
- Career Details API
- Learning Resource Recommendations

---

### 🤖 AI Career Assistant (Google Gemini)

- Google Gemini 2.5 Flash Integration
- Personalized AI Career Guidance
- Resume-Aware Conversations
- Context-Aware Responses
- Career Comparison
- Career Roadmap Generator
- Project Recommendations
- Certification Recommendations
- Learning Resource Recommendations
- AI Feedback System

---

### 💬 Conversation Management

- Create New Conversations
- Retrieve Conversation History
- Conversation Persistence
- User-specific Conversation Access
- Delete Conversations

---

### 🛡️ Security

- JWT Authentication
- User-specific Resource Authorization
- Prompt Injection Filtering
- API Key Protection
- Input Validation
- Output Sanitization
- Rate Limiting
- Secure Environment Variables

---

### ⚡ REST API

- FastAPI-based REST Architecture
- OpenAPI / Swagger Documentation
- Pydantic Request Validation
- Structured JSON Responses
- Standard HTTP Status Codes

---

### 🗄️ Database

- PostgreSQL Database
- SQLAlchemy ORM
- Alembic Database Migrations
- Resume Storage
- Recommendation History
- Conversation History
- Feedback Storage

---

## 🚧 Planned Features

### 🎤 AI Interview Intelligence

- AI Mock Interview
- Adaptive Interview System
- Voice-Based Interview Assessment
- AI Proctored Interview
- Behavioral Interview Analysis

---

### 📊 Predictive Analytics

- Placement Readiness Prediction
- Performance Forecasting
- Learning Progress Analysis
- Analytics Dashboard
- Personalized Career Insights

---

### 🤖 Advanced AI Features

- Resume-to-Job Matching
- Multi-Agent AI Collaboration
- RAG-based Knowledge Retrieval
- GitHub Portfolio Analyzer
- LinkedIn Profile Analyzer
- AI Resume Builder
- Multilingual AI Career Assistant

---

### ☁️ Deployment & Scalability

- Docker Containerization
- Cloud Deployment
- CI/CD Pipeline
- Production Monitoring
- Logging & Performance Analytics

# Technology Stack

## 🎨 Frontend

- Next.js
- TypeScript
- Tailwind CSS
- React
- Axios

---

## ⚙️ Backend

- Python 3.12+
- FastAPI
- Uvicorn
- SQLAlchemy
- Alembic
- Pydantic

---

## 🗄️ Database

- PostgreSQL
- SQLAlchemy ORM
- Alembic Migrations

---

## 🔐 Authentication & Security

- JWT (JSON Web Tokens)
- OAuth2 Password Bearer
- Passlib
- bcrypt
- SlowAPI (Rate Limiting)
- Prompt Injection Protection
- Input Validation
- Output Sanitization

---

## 📄 Resume Processing

- pdfplumber
- python-docx
- python-multipart

Features:

- PDF Resume Parsing
- DOCX Resume Parsing
- Resume Text Extraction
- Resume Validation

---

## 🤖 Artificial Intelligence & NLP

### Currently Implemented

- Google Gemini 2.5 Flash
- Prompt Engineering
- Rule-Based NLP
- Resume Skill Extraction
- ATS Score Analysis
- AI Career Summary Generation
- AI Career Assistant
- Career Recommendation Engine
- Career Match Score Calculation
- Missing Skill Detection
- Career Roadmap Generation
- Career Comparison
- Learning Resource Recommendation
- Project Recommendation
- Certification Recommendation

---

### Planned

- spaCy
- Hugging Face Transformers
- LangChain
- CrewAI
- Retrieval-Augmented Generation (RAG)

---

## 📊 Machine Learning

### Planned

- Scikit-learn
- XGBoost
- Pandas
- NumPy

Future ML Features:

- Placement Readiness Prediction
- Career Success Prediction
- Resume Ranking
- Performance Forecasting

---

## 👁️ Computer Vision *(Planned)*

- OpenCV
- MediaPipe

Future Features:

- AI Proctored Interview
- Face Detection
- Eye Movement Tracking
- Suspicious Activity Detection

---

## 🎙️ Speech Processing *(Planned)*

- OpenAI Whisper

Future Features:

- Speech-to-Text
- Voice-Based Mock Interview
- Pronunciation Analysis
- Communication Skill Assessment

---

## 📈 Data Visualization *(Planned)*

- Plotly
- Matplotlib

Future Features:

- Placement Dashboard
- Analytics Dashboard
- Career Progress Tracking
- Skill Growth Visualization

---

## 🛠️ Development Tools

- Git
- GitHub
- VS Code
- Swagger UI
- Postman
- pgAdmin
- Virtual Environment (venv)

---

## ☁️ Deployment *(Planned)*

- Docker
- Nginx
- GitHub Actions
- AWS / Azure / GCP
- CI/CD Pipeline

# Project Structure

```text
Career-Intelligence-System/
│
├── backend/
│   │
│   ├── alembic/
│   │   ├── versions/
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── README
│   │
│   ├── app/
│   │   │
│   │   ├── config/
│   │   │   └── settings.py
│   │   │
│   │   ├── core/
│   │   │   ├── security.py
│   │   │   ├── gemini.py
│   │   │   └── rate_limiter.py
│   │   │
│   │   ├── data/
│   │   │   └── question_catalog.py
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
│   │   │   ├── conversation.py
│   │   │   ├── chat_history.py
│   │   │   ├── assistant_feedback.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── resume.py
│   │   │   ├── recommendation_router.py
│   │   │   └── ai_assistant_router.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── user.py
│   │   │   ├── token.py
│   │   │   ├── resume.py
│   │   │   ├── recommendation.py
│   │   │   ├── assistant.py
│   │   │   └── ai_assistant.py
│   │   │
│   │   ├── services/
│   │   │   ├── recommendation_service.py
│   │   │   ├── career_summary_service.py
│   │   │   ├── ai_assistant_service.py
│   │   │   ├── context_builder.py
│   │   │   ├── prompt_builder.py
│   │   │   ├── prompt_injection_filter.py
│   │   │   ├── response_formatter.py
│   │   │   ├── roadmap_generator_service.py
│   │   │   └── career_comparison_service.py
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
│
├── scripts/
│   ├── import_careers.py
│   ├── import_skills.py
│   ├── seed_database.py
│   └── test_save_recommendation.py
│
├── frontend/
│
├── assets/
│
├── README.md
│
└── .gitignore
```

# Installation & Setup

## Clone the Repository

```bash
git clone https://github.com/<your-username>/Career-Intelligence-System.git
```

---

## Navigate to the Backend

```bash
cd Career-Intelligence-System/backend
```

---

## Create a Virtual Environment

```bash
python -m venv venv
```

---

## Activate the Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Configure Environment Variables

Create a `.env` file inside the **backend** directory.

```env
# ==========================
# Database
# ==========================

DATABASE_URL=postgresql://postgres:password@localhost/career_intelligence_db

# ==========================
# Authentication
# ==========================

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60

# ==========================
# Google Gemini
# ==========================

GEMINI_API_KEY=your_gemini_api_key

GEMINI_MODEL=gemini-2.5-flash

GEMINI_TEMPERATURE=0.3

GEMINI_MAX_OUTPUT_TOKENS=2048

# ==========================
# AI Assistant
# ==========================

AI_CHAT_RATE_LIMIT=20/minute
```

---

# Database Migration

### Apply all migrations

```bash
alembic upgrade head
```

---

### Create a new migration

```bash
alembic revision --autogenerate -m "migration_name"
```

---

# Run the Backend Server

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

# API Documentation

FastAPI automatically generates interactive API documentation.

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

---

# Google Gemini Configuration

The AI Career Assistant uses **Google Gemini 2.5 Flash** for generating personalized career guidance.

Before starting the backend:

1. Generate a Gemini API key.
2. Add the key to the `.env` file.
3. Restart the FastAPI server.

The Gemini client is initialized through:

```text
backend/app/core/gemini.py
```

---

# Verify the Installation

After starting the server:

✅ Open Swagger UI

```
http://127.0.0.1:8000/docs
```

Verify the following modules:

- Authentication APIs
- Resume APIs
- Career Recommendation APIs
- AI Career Assistant APIs

If all endpoints are visible and accessible, the backend has been configured successfully.

# System Workflows

## 📄 Resume Intelligence Workflow

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
PDF / DOCX Parsing
        │
        ▼
Extract Resume Text
        │
        ▼
ATS Score Analysis
        │
        ▼
Generate Resume Suggestions
        │
        ▼
Extract Skills
        │
        ▼
Career Recommendation Engine
        │
        ▼
Calculate Career Match Score
        │
        ▼
Detect Missing Skills
        │
        ▼
Generate AI Career Summary
        │
        ▼
Recommend Learning Resources
        │
        ▼
Save Recommendation
        │
        ▼
Recommendation History
        │
        ▼
Career Details
```

---

# 🤖 AI Career Assistant Workflow

```text
User Login
      │
      ▼
JWT Authentication
      │
      ▼
Create / Select Conversation
      │
      ▼
Send Chat Message
      │
      ▼
Input Validation
      │
      ▼
Prompt Injection Filter
      │
      ▼
Retrieve User Context
      │
      ▼
 ┌─────────────────────────────┐
 │ Resume Information          │
 │ ATS Score                   │
 │ Resume Suggestions          │
 │ Extracted Skills            │
 │ Career Recommendation       │
 │ Match Score                 │
 │ Missing Skills              │
 │ Learning Resources          │
 │ User Profile                │
 └─────────────────────────────┘
      │
      ▼
Career Comparison Service
      │
      ▼
Roadmap Generator
      │
      ▼
Project Recommendations
      │
      ▼
Certification Recommendations
      │
      ▼
Prompt Builder
      │
      ▼
Google Gemini API
      │
      ▼
AI Response Generation
      │
      ▼
Response Formatter
      │
      ▼
Save Chat History
      │
      ▼
Return AI Response
```

---

# 🧠 AI Career Assistant Workflow Overview

The AI Career Assistant follows the workflow below:

1. Authenticate the user using JWT.
2. Validate the incoming request.
3. Check for prompt injection attempts.
4. Retrieve the user's career context from the database.
5. Build a personalized AI prompt.
6. Send the prompt to Google Gemini.
7. Format the generated response.
8. Store the conversation in PostgreSQL.
9. Return the response to the user.

---

# 💡 Personalized AI Context

Every AI response is generated using the authenticated user's data, including:

- Resume Information
- ATS Score
- Resume Improvement Suggestions
- Extracted Skills
- Recommended Career
- Career Match Score
- Missing Skills
- Learning Resources
- User Profile
- Previous Conversation History

This enables the AI Career Assistant to provide personalized career guidance instead of generic responses.

---

# 🔒 AI Security Workflow

Every chat request passes through multiple security layers before reaching the AI model.

```text
User Message
      │
      ▼
JWT Authentication
      │
      ▼
Request Validation
      │
      ▼
Prompt Injection Filter
      │
      ▼
Conversation Ownership Validation
      │
      ▼
Rate Limiting
      │
      ▼
Prompt Builder
      │
      ▼
Google Gemini API
      │
      ▼
Response Formatting
      │
      ▼
Return Response
```

# REST API Documentation

The backend exposes RESTful APIs built using **FastAPI**. All protected endpoints require JWT authentication unless otherwise specified.

---

# 🔐 Authentication APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Authenticate user and generate JWT token |

---

# 👤 User Management APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/users/profile` | Retrieve logged-in user's profile |
| PUT | `/users/profile` | Update user profile |
| DELETE | `/users/profile` | Deactivate user account |

---

# 📄 Resume Intelligence APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/resume/upload` | Upload resume |
| GET | `/resume/parse/{resume_id}` | Parse uploaded resume |
| GET | `/resume/ats/{resume_id}` | Calculate ATS score |
| GET | `/resume/suggestions/{resume_id}` | Generate resume improvement suggestions |
| GET | `/resume/history` | Retrieve uploaded resume history |
| GET | `/resume/{resume_id}` | Retrieve resume details |
| DELETE | `/resume/{resume_id}` | Delete uploaded resume |

---

# 🎯 Career Recommendation APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/career/recommend` | Generate career recommendation |
| GET | `/api/career/history` | View recommendation history |
| GET | `/api/career/{career_id}` | View career details |

---

# 🤖 AI Career Assistant APIs

## Conversation Management

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/assistant/conversations` | Create a new conversation |
| GET | `/api/assistant/conversations` | Retrieve all conversations |
| DELETE | `/api/assistant/conversations/{conversation_id}` | Delete a conversation |

---

## Chat APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/assistant/chat` | Send a message to the AI Career Assistant |
| GET | `/api/assistant/history/{conversation_id}` | Retrieve conversation history |

---

## AI Assistant Features

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/assistant/questions` | Retrieve common career questions |
| GET | `/api/assistant/projects` | Get personalized project recommendations |
| GET | `/api/assistant/resources` | Get learning resource recommendations |
| GET | `/api/assistant/certifications` | Get certification recommendations |
| GET | `/api/assistant/roadmap` | Generate personalized career roadmap |
| GET | `/api/assistant/compare-careers` | Compare two career paths |

---

## AI Feedback

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/assistant/feedback` | Submit AI response feedback |

---

# 🔒 Authentication

The following endpoints require a valid JWT access token:

- User Profile APIs
- Resume APIs
- Career Recommendation APIs
- AI Career Assistant APIs

JWT tokens must be included in the request header.

```http
Authorization: Bearer <access_token>
```

---

# 📖 Interactive API Documentation

FastAPI automatically generates interactive API documentation.

## Swagger UI

```text
http://127.0.0.1:8000/docs
```

---

## ReDoc

```text
http://127.0.0.1:8000/redoc
```

---

# 📦 API Response Format

Successful responses follow a structured JSON format.

Example:

```json
{
    "success": true,
    "message": "Operation completed successfully.",
    "data": {
        ...
    }
}
```

Validation and application errors return appropriate HTTP status codes with descriptive error messages.

---

# 🌐 HTTP Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | OK |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 409 | Conflict |
| 422 | Validation Error |
| 429 | Too Many Requests |
| 500 | Internal Server Error |

# System Intelligence

## 🎯 Career Recommendation Engine

The Career Recommendation Engine analyzes an uploaded resume and recommends the most suitable career path based on the user's technical skills and profile.

The recommendation process consists of the following stages:

1. Upload and validate the resume.
2. Parse PDF or DOCX files.
3. Extract resume text.
4. Identify technical skills.
5. Compare extracted skills with the career database.
6. Calculate career match scores.
7. Detect missing skills.
8. Recommend the best matching career.
9. Generate an AI-powered career summary.
10. Recommend learning resources.
11. Store recommendation history.

---

## 📄 ATS Analysis

The ATS (Applicant Tracking System) Analyzer evaluates resumes using multiple criteria commonly used by recruitment systems.

The analysis includes:

- Contact Information
- Professional Summary
- Education
- Technical Skills
- Work Experience
- Projects
- Certifications
- Achievements
- Resume Formatting

The ATS engine automatically:

- Extracts resume text
- Calculates an ATS compatibility score
- Identifies weak sections
- Generates personalized resume improvement suggestions

---

## 🤖 AI Career Assistant

The AI Career Assistant provides personalized career guidance using **Google Gemini 2.5 Flash**.

Unlike a general chatbot, the assistant generates responses using the authenticated user's career data, making every response personalized.

The assistant can help users with:

- Career Guidance
- Resume Improvement
- ATS Score Explanation
- Skill Gap Analysis
- Career Comparison
- Learning Recommendations
- Project Recommendations
- Certification Recommendations
- Career Roadmap Generation

---

## 🧠 Personalized Context Generation

Before generating an AI response, the system retrieves information from multiple modules.

The personalized context includes:

- User Profile
- Resume Information
- ATS Score
- Resume Suggestions
- Extracted Skills
- Recommended Career
- Career Match Score
- Missing Skills
- Learning Resources
- Previous Conversation History

This context enables the AI Career Assistant to provide accurate and personalized responses instead of generic advice.

---

## ✨ Google Gemini Integration

The AI Career Assistant uses **Google Gemini 2.5 Flash** as its Large Language Model (LLM).

Gemini is responsible for:

- Understanding user questions
- Generating natural language responses
- Explaining career recommendations
- Suggesting projects
- Recommending certifications
- Building career roadmaps
- Answering resume-related questions

The backend securely communicates with Gemini using an API key stored in environment variables.

---

## 💬 Conversation Management

Every interaction with the AI Career Assistant is stored in PostgreSQL.

The conversation system supports:

- Conversation Creation
- Conversation History
- Persistent Chat Storage
- User-specific Conversations
- Conversation Deletion
- AI Feedback Collection

This allows users to continue previous discussions without losing context.

---

## 🛣️ Career Roadmap Generator

The Career Roadmap Generator creates a personalized roadmap based on the user's current skills and recommended career.

The roadmap considers:

- Existing Skills
- Missing Skills
- Career Recommendation
- Learning Resources
- Recommended Certifications
- Suggested Projects

The generated roadmap helps users progress from their current skill level to their target career.

---

## 💡 Project Recommendation Engine

The system recommends projects that align with the user's target career and current skill set.

Recommendations are generated using:

- Recommended Career
- Existing Skills
- Missing Skills
- Skill Gap Analysis

These projects help users build practical experience and strengthen their portfolio.

---

## 🎓 Certification Recommendation Engine

The Certification Recommendation Engine suggests certifications relevant to the user's career goals.

Recommendations are based on:

- Recommended Career
- Missing Skills
- Current Skill Level

Examples include certifications from platforms such as:

- AWS
- Google
- Microsoft
- Coursera
- Udemy

---

## 🛡️ AI Security

Multiple security mechanisms protect the AI Career Assistant.

### Authentication

- JWT Authentication
- User-specific Data Access

### AI Security

- Prompt Injection Filtering
- Input Validation
- Output Sanitization
- Rate Limiting

### Data Security

- Protected API Keys
- Secure Environment Variables
- Conversation Ownership Validation

These measures ensure secure, reliable, and personalized AI interactions.

---

## ⚙️ AI Response Generation Pipeline

Every AI response follows the pipeline below:

```text
User Message
      │
      ▼
JWT Authentication
      │
      ▼
Conversation Validation
      │
      ▼
Prompt Injection Filter
      │
      ▼
Retrieve User Context
      │
      ▼
Career Comparison
      │
      ▼
Roadmap Generator
      │
      ▼
Prompt Builder
      │
      ▼
Google Gemini API
      │
      ▼
AI Response Generation
      │
      ▼
Response Formatter
      │
      ▼
Save Conversation
      │
      ▼
Return Response
```

# Current Backend Features

## 🔐 Authentication & User Management

- JWT Authentication
- User Registration
- User Login
- User Profile Management
- Protected REST APIs

---

## 📄 Resume Intelligence

- Resume Upload
- Resume Validation
- Resume Parsing
- Resume Text Extraction
- ATS Score Analysis
- Resume Improvement Suggestions
- Resume History
- Resume Details
- Resume Deletion

---

## 🎯 Career Intelligence

- Skill Extraction
- Career Recommendation Engine
- Career Match Score Calculation
- Missing Skill Detection
- AI Career Summary Generation
- Recommendation History
- Career Details API
- Learning Resource Recommendations

---

## 🤖 AI Career Assistant

- Google Gemini Integration
- Personalized AI Career Assistant
- Resume-aware AI Responses
- Conversation Management
- Conversation History
- Career Comparison
- Career Roadmap Generation
- Project Recommendations
- Certification Recommendations
- Learning Resource Recommendations
- AI Feedback System

---

## 🛡️ Security

- JWT Authentication
- Prompt Injection Filtering
- API Key Protection
- Input Validation
- Rate Limiting
- Output Sanitization
- User-specific Data Isolation

---

## 🗄️ Database

- PostgreSQL
- SQLAlchemy ORM
- Alembic Database Migrations
- Resume Storage
- Recommendation History
- Conversation History
- Feedback Storage

---

# Development Roadmap

## ✅ Completed Phases

- ✅ Phase 1 – Project Planning & Environment Setup
- ✅ Phase 2 – Backend Foundation & FastAPI Setup
- ✅ Phase 3 – Database Design & User Authentication
- ✅ Phase 4 – Resume Intelligence & ATS Analysis
- ✅ Phase 5 – Career Recommendation Engine
- ✅ Phase 6 – AI Career Assistant

---

## 🚧 Upcoming Phases

- ⏳ Phase 7 – Resume-to-Job Matching
- ⏳ Phase 8 – AI Mock Interview
- ⏳ Phase 9 – Voice-Based Interview Analysis
- ⏳ Phase 10 – AI Proctored Interview
- ⏳ Phase 11 – Placement Readiness Prediction
- ⏳ Phase 12 – Analytics Dashboard
- ⏳ Phase 13 – GitHub Portfolio Analyzer
- ⏳ Phase 14 – Multi-Agent AI Collaboration
- ⏳ Phase 15 – Deployment & Production

---

# Testing

The backend has been thoroughly tested using **Swagger UI**, **Postman**, and manual integration testing.

## Authentication

- ✅ User Registration
- ✅ User Login
- ✅ JWT Authorization
- ✅ Protected API Access

---

## Resume Intelligence

- ✅ PDF Upload
- ✅ DOCX Upload
- ✅ Invalid File Validation
- ✅ File Size Validation
- ✅ Resume Parsing
- ✅ Resume Text Extraction
- ✅ ATS Score Analysis
- ✅ Resume Suggestions
- ✅ Resume History
- ✅ Resume Details
- ✅ Resume Deletion

---

## Career Recommendation Engine

- ✅ Skill Extraction
- ✅ Career Recommendation
- ✅ Career Match Score Calculation
- ✅ Missing Skill Detection
- ✅ AI Career Summary Generation
- ✅ Recommendation History
- ✅ Career Details API
- ✅ Learning Resource Recommendations

---

## AI Career Assistant

- ✅ Conversation Creation
- ✅ Conversation History
- ✅ AI Chat
- ✅ Personalized Responses
- ✅ Career Comparison
- ✅ Career Roadmap Generation
- ✅ Project Recommendations
- ✅ Certification Recommendations
- ✅ Learning Resource Recommendations
- ✅ AI Feedback Submission

---

## Security

- ✅ JWT Authentication
- ✅ User-specific Resource Protection
- ✅ Prompt Injection Filtering
- ✅ Rate Limiting
- ✅ Input Validation
- ✅ Output Sanitization
- ✅ API Key Protection

---

## Error Handling

- ✅ Invalid JWT
- ✅ Missing Resume
- ✅ Missing Career Recommendation
- ✅ Empty Messages
- ✅ Long Prompt Handling
- ✅ Gemini API Quota Handling (HTTP 429)
- ✅ Invalid Requests
- ✅ Validation Errors

---

# Current Project Status

## ✅ Completed

- Authentication & Authorization
- Resume Intelligence Module
- ATS Analysis Module
- Career Recommendation Engine
- AI Career Assistant Backend
- Google Gemini Integration
- Security Enhancements
- REST API Development
- Database Design & Integration

---

## 🚧 In Progress

- Frontend Integration for AI Career Assistant

---

## 📅 Upcoming

- Resume-to-Job Matching
- AI Mock Interview
- Voice-Based Interview
- AI Proctored Interview
- Placement Readiness Prediction
- Analytics Dashboard
- GitHub Portfolio Analyzer
- Multi-Agent AI
- Cloud Deployment

---

# Future Scope

The project is designed to evolve into a complete AI-powered placement platform.

Planned enhancements include:

- AI Resume Builder
- Resume-to-Job Matching
- Company Recruitment Portal
- LinkedIn Profile Analyzer
- GitHub Portfolio Analyzer
- AI Mock Interview
- Voice-Based Interview Analysis
- AI Proctored Interview
- Placement Readiness Prediction
- Analytics Dashboard
- Multi-Agent AI Collaboration
- AI Mentor Recommendation System
- Cloud Deployment
- Mobile Application (Android & iOS)

---

# Repository Status

🚧 **Actively Under Development**

The backend is currently completed through **Phase 6 – AI Career Assistant**.

### Completed Modules

- Authentication & Authorization
- Resume Intelligence
- ATS Analysis
- Career Recommendation Engine
- AI Career Assistant
- Google Gemini Integration
- Security & Rate Limiting

Future development will focus on AI Interview modules, Predictive Analytics, Multi-Agent AI, and production deployment.

---

# Contributing

Contributions, suggestions, and feedback are welcome.

If you would like to contribute:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Submit a Pull Request.

Please ensure that new code follows the existing project structure and coding standards.

---

# Author

**Subin Paul**

Bachelor of Technology (B.Tech) – Computer Science & Engineering

Final Year Major Project

---

# License

This project has been developed for **academic, educational, and research purposes**.

Copyright © 2026 Subin Paul.

All Rights Reserved.
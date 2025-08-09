# Resume Ranking Application


## Overview

The Resume Ranking Application is an AI-powered recruitment tool that leverages Large Language Models (LLM) and advanced NLP techniques to automatically evaluate, analyze, and rank resumes based on job requirements. Built with FastAPI, Next.js, and Ollama (local LLM), it provides intelligent candidate-job matching with detailed scoring and analysis.


## Key Technologies

- **Backend**: FastAPI, MongoDB
- **Frontend**: Next.js 14, TypeScript, TailwindCSS
- **AI/ML**: Ollama (Local LLM), Llama 3.1
- **Infrastructure**: Docker, Nginx

## Features

### Job Description Analysis

- **Local LLM Analysis**:
  - Extracts key requirements, skills, and qualifications using Ollama
  - Structures data into standardized format for matching
  - Privacy-focused with local processing
  - Fast processing with local inference

### Resume Analysis

- **Local CV Processing**:
  - Handles PDF and Word documents
  - Extracts and structures candidate information using local LLM
  - Identifies skills, experience, and qualifications
  - No data leaves your infrastructure

### AI-Powered Matching

- **Local Matching Algorithm**:
  - Uses Ollama for local LLM operations
  - Semantic understanding of job requirements and candidate qualifications
  - Privacy-preserving analysis

### Intelligent Ranking

- **Local Evaluation System**:
  - Generates detailed match analysis using local LLM
  - Provides scoring based on multiple criteria
  - Offers AI-generated feedback and comments
  - Ranks candidates based on overall fit


## Getting Started

### Prerequisites

- Docker and Docker Compose
- At least 8GB RAM for Ollama

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/vectornguyen76/resume-ranking.git
   cd resume-ranking
   ```

2. **Start the Application**:

   ```bash
   docker compose up -d
   ```

3. **Install Ollama Model**:

   ```bash
   # Wait for Ollama to start, then install the model
   docker exec -it ollama ollama pull llama3.1
   ```

4. **Access Application**:
   - Frontend: `http://localhost`
   - Backend API: `http://localhost/backend`

## Usage

1. **Create Job Positions**: Add job descriptions with requirements
2. **Upload Resumes**: Upload candidate CV files (PDF/DOCX)
3. **Run Matching**: Select a job and run AI-powered matching
4. **Review Results**: View detailed scoring and recommendations

## Local Development

1. **Install Dependencies**:
   ```bash
   # Frontend
   cd frontend && npm install
   
   # Backend
   cd backend && pip install -r requirements.txt
   
   # Analysis Service
   cd analysis_service && pip install -r requirements.txt
   ```

2. **Start Services**:
   ```bash
   # Start Ollama
   docker run -d -p 11434:11434 --name ollama ollama/ollama
   docker exec -it ollama ollama pull llama3.1
   
   # Start MongoDB
   docker run -d -p 27017:27017 --name mongo mongo
   
   # Start services
   cd analysis_service && uvicorn app:app --port 7000
   cd backend && flask run --port 5000
   cd frontend && npm run dev
   ```

## Configuration

### Environment Variables

- `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:5000)
- `MONGO_URL`: MongoDB connection string
- `OLLAMA_HOST`: Ollama server host (default: localhost:11434)

### Ollama Models

The application uses Llama 3.1 by default. You can use other models by updating the model name in the analysis service configuration.

## Privacy & Security

- **Local Processing**: All AI analysis happens locally using Ollama
- **No External API Calls**: No data is sent to external AI services
- **Data Privacy**: Resume and job data stays within your infrastructure
- **Secure**: No API keys or external dependencies for AI processing

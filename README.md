# Resume Ranking Application

## Overview

The Resume Ranking Application is an AI-powered recruitment tool that leverages Google Gemini and advanced NLP techniques to automatically evaluate, analyze, and rank resumes based on job requirements. Built with FastAPI, Next.js, and Google Gemini, it provides intelligent candidate-job matching with detailed scoring and analysis.

## Key Technologies

- **Backend**: Flask, MongoDB
- **Frontend**: Next.js 14, TypeScript, TailwindCSS
- **AI/ML**: Google Gemini API
- **Database**: MongoDB (local installation)

## Features

### Job Description Analysis

- **Gemini AI Analysis**:
  - Extracts key requirements, skills, and qualifications using Google Gemini
  - Structures data into standardized format for matching
  - Fast processing with cloud-based AI

### Resume Analysis

- **AI-Powered CV Processing**:
  - Handles PDF and Word documents
  - Extracts and structures candidate information using Gemini
  - Identifies skills, experience, and qualifications

### AI-Powered Matching

- **Intelligent Matching Algorithm**:
  - Uses Google Gemini for semantic understanding
  - Analyzes job requirements and candidate qualifications
  - Provides detailed scoring and recommendations

### Intelligent Ranking

- **Advanced Evaluation System**:
  - Generates detailed match analysis using Gemini
  - Provides scoring based on multiple criteria
  - Offers AI-generated feedback and comments
  - Ranks candidates based on overall fit

## Prerequisites

- Python 3.10+
- Node.js 18+
- MongoDB (local installation)
- Google Gemini API key

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/vectornguyen76/resume-ranking.git
cd resume-ranking
```

### 2. Install Dependencies

```bash
npm run install:all
```

### 3. Set Up MongoDB

Install MongoDB locally:

**Ubuntu/Debian:**
```bash
sudo apt-get install mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

**macOS:**
```bash
brew install mongodb-community
brew services start mongodb-community
```

**Windows:**
Download and install from [MongoDB official website](https://www.mongodb.com/try/download/community)

### 4. Configure Environment Variables

**Analysis Service:**
```bash
cd analysis_service
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

**Backend:**
```bash
cd backend
cp .env.example .env
# Edit .env with your MongoDB connection string
```

### 5. Get Google Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `analysis_service/.env` file

## Usage

### Development Mode

Start all services in development mode:

```bash
npm run dev
```

This will start:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- Analysis Service: http://localhost:7000

### Production Mode

Build and start in production mode:

```bash
npm run build
npm start
```

## Application Workflow

1. **Create Job Positions**: Add job descriptions with requirements
2. **Upload Resumes**: Upload candidate CV files (PDF/DOCX)
3. **Run Matching**: Select a job and run AI-powered matching
4. **Review Results**: View detailed scoring and recommendations

## Local Development Setup

### Individual Service Setup

**Analysis Service:**
```bash
cd analysis_service
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --port 7000 --reload
```

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
flask run --port 5000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Configuration

### Environment Variables

**Analysis Service (.env):**
- `GEMINI_API_KEY`: Your Google Gemini API key

**Backend (.env):**
- `MONGO_URL`: MongoDB connection string (default: mongodb://localhost:27017/resume_ranking_db)
- `ANALYSIS_SERVICE_URL`: Analysis service URL (default: http://localhost:7000)
- `SECRET_KEY`: Flask secret key

**Frontend (.env.local):**
- `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:5000)

## API Documentation

Access the Swagger documentation at:
```
http://localhost:5000/swagger-ui
```

## Troubleshooting

### Common Issues

1. **MongoDB Connection Error**:
   - Ensure MongoDB is running: `sudo systemctl status mongodb`
   - Check connection string in backend/.env

2. **Gemini API Error**:
   - Verify your API key is correct
   - Check API quota and billing in Google Cloud Console

3. **Port Conflicts**:
   - Make sure ports 3000, 5000, and 7000 are available
   - Modify ports in package.json scripts if needed

### Logs

- Backend logs: `backend/logs/api.log`
- Analysis service logs: `analysis_service/logs/api.log`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.
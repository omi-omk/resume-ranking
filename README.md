# Resume Ranking System

A unified AI-powered recruitment platform that analyzes resumes and matches candidates with job opportunities using Google Gemini AI.

## Features

- **Resume Analysis**: Upload PDF/DOCX files and extract candidate information using AI
- **Job Management**: Create and manage job descriptions with automatic requirement extraction
- **AI Matching**: Intelligent candidate-job matching with detailed scoring
- **Modern Web Interface**: Clean, responsive web interface built with vanilla JavaScript
- **Unified Architecture**: Single FastAPI service with integrated frontend

## Technology Stack

- **Backend**: FastAPI (Python 3.10+)
- **Database**: MongoDB
- **AI**: Google Gemini API
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Document Processing**: PyPDF, python-docx

## Quick Start

### Prerequisites

- Python 3.10 or higher
- MongoDB (local installation)
- Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd resume-ranking
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

4. **Start MongoDB**
   ```bash
   # Ubuntu/Debian
   sudo systemctl start mongodb
   
   # macOS
   brew services start mongodb-community
   
   # Windows
   net start MongoDB
   ```

5. **Run the application**
   ```bash
   python -m uvicorn app.main:app --reload
   ```

6. **Access the application**
   - Open your browser and go to: http://localhost:8000
   - API documentation: http://localhost:8000/docs

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Google Gemini API Key (required)
GEMINI_API_KEY="your-gemini-api-key-here"

# MongoDB Configuration
MONGODB_URL="mongodb://localhost:27017/resume_ranking"

# App Configuration
APP_NAME="Resume Ranking System"
APP_ENV="development"
DEBUG=true
```

### Getting Google Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file

## Usage

### 1. Upload Candidates
- Navigate to the "Candidates" section
- Click "Upload CVs" 
- Select or drag & drop PDF/DOCX resume files
- The system will automatically analyze and extract candidate information

### 2. Create Jobs
- Go to the "Jobs" section
- Click "Create Job"
- Enter job title and description
- The AI will automatically extract requirements and qualifications

### 3. Run Matching
- Visit the "Matching" section
- Select a job from the dropdown
- Click "Start Matching"
- View detailed matching results with scores and analysis

## API Endpoints

### Candidates
- `POST /api/candidates/upload` - Upload resume files
- `GET /api/candidates/` - List candidates (paginated)
- `GET /api/candidates/{id}` - Get candidate details
- `PUT /api/candidates/{id}` - Update candidate
- `DELETE /api/candidates/{id}` - Delete candidate

### Jobs
- `POST /api/jobs/` - Create job
- `GET /api/jobs/` - List jobs (paginated)
- `GET /api/jobs/all` - Get all jobs (for dropdowns)
- `GET /api/jobs/{id}` - Get job details
- `PUT /api/jobs/{id}` - Update job
- `DELETE /api/jobs/{id}` - Delete job

### Matching
- `POST /api/matching/process` - Process matching for a job
- `GET /api/matching/results` - Get matching results
- `GET /api/matching/detail/{candidate_id}/{job_id}` - Get detailed match analysis

## Development

### Project Structure
```
app/
├── main.py              # FastAPI application entry point
├── core/
│   ├── config.py        # Configuration settings
│   └── database.py      # Database connection and setup
├── models/              # Pydantic models
├── services/            # Business logic services
├── api/                 # API routes and endpoints
├── static/              # Static files (CSS, JS)
└── templates/           # HTML templates
```

### Running in Development Mode
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
ruff format app/
ruff check app/
```

## Deployment

### Production Setup

1. **Set environment variables**
   ```bash
   export GEMINI_API_KEY="your-production-api-key"
   export MONGODB_URL="your-production-mongodb-url"
   export APP_ENV="production"
   export DEBUG=false
   ```

2. **Run with production server**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

### Docker Deployment (Optional)

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Troubleshooting

### Common Issues

1. **MongoDB Connection Error**
   - Ensure MongoDB is running: `sudo systemctl status mongodb`
   - Check connection string in `.env` file

2. **Gemini API Error**
   - Verify API key is correct and has proper permissions
   - Check API quota in Google Cloud Console

3. **File Upload Issues**
   - Ensure `uploads/` directory exists and is writable
   - Check file size limits (default: 10MB)

4. **Port Already in Use**
   - Change port in startup command: `--port 8001`
   - Kill existing process: `lsof -ti:8000 | xargs kill`

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Run tests and linting: `pytest && ruff check app/`
5. Submit a pull request

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Check the API documentation at `/docs`
- Review the troubleshooting section above
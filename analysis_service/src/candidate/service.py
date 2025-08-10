import json
import os
import time
from datetime import datetime
import google.generativeai as genai

from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader
from src.candidate.config import candidate_config
from src.candidate.prompts import fn_candidate_analysis, system_prompt_candidate
from src.utils import LOGGER


async def save_cv_candidate(file):
    # Prepend the current datetime to the filename
    file_name = datetime.now().strftime("%Y%m%d%H%M%S-") + file.filename

    # Construct the full image path based on the settings
    image_path = candidate_config.CV_UPLOAD_DIR + file_name

    # Read the contents of the uploaded file asynchronously
    contents = await file.read()

    # Write the uploaded contents to the specified image path
    with open(image_path, "wb") as f:
        f.write(contents)

    return file_name


def load_pdf_docx(file_path):
    # Determine the file type and choose the appropriate loader
    if os.path.basename(file_path).lower().endswith((".pdf", ".docx")):
        loader = (
            PyPDFLoader(file_path)
            if file_path.lower().endswith(".pdf")
            else Docx2txtLoader(file_path)
        )

    # Load and split the document using the selected loader
    documents = loader.load_and_split()

    return documents


def read_cv_candidate(file_name):
    file_path = candidate_config.CV_UPLOAD_DIR + file_name

    documents = load_pdf_docx(file_path=file_path)
    content = ""
    for page in documents:
        content += page.page_content
    return content


def analyse_candidate(cv_content):
    start = time.time()
    LOGGER.info("Start analyse candidate")

    # Use Gemini instead of Ollama
    json_output = analyse_with_gemini(cv_content)

    LOGGER.info("Done analyse candidate")
    LOGGER.info(f"Time analyse candidate: {time.time() - start}")

    return json_output


def analyse_with_gemini(cv_content):
    """Analyze candidate CV using Google Gemini"""
    
    # Configure Gemini
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        LOGGER.error("GEMINI_API_KEY not found in environment variables")
        return get_default_candidate_response()
    
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    {system_prompt_candidate}
    
    Please analyze the following CV and extract the information in JSON format:
    
    CV Content:
    {cv_content}
    
    Return a JSON object with the following structure:
    {{
        "candidate_name": "string",
        "phone_number": "string", 
        "email": "string",
        "degree": ["array of strings"],
        "experience": ["array of strings"],
        "technical_skill": ["array of strings"],
        "responsibility": ["array of strings"],
        "certificate": ["array of strings"],
        "soft_skill": ["array of strings"],
        "comment": "string",
        "job_recommended": ["array of strings"],
        "office": 0,
        "sql": 0
    }}
    
    Respond only with valid JSON, no additional text.
    """
    
    try:
        response = model.generate_content(prompt)
        
        # Extract JSON from response
        response_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        
        return json.loads(response_text.strip())
        
    except Exception as e:
        LOGGER.error(f"Error calling Gemini: {str(e)}")
        return get_default_candidate_response()


def get_default_candidate_response():
    """Return default response when Gemini fails"""
    return {
        "candidate_name": "Unknown",
        "phone_number": "",
        "email": "",
        "degree": [],
        "experience": [],
        "technical_skill": [],
        "responsibility": [],
        "certificate": [],
        "soft_skill": [],
        "comment": "Analysis failed - please try again",
        "job_recommended": [],
        "office": 0,
        "sql": 0
    }
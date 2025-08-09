import json
import os
import time
from datetime import datetime
import httpx

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


def output2json(output):
    """GPT Output Object >>> json"""
    opts = jsbeautifier.default_options()
    return json.loads(jsbeautifier.beautify(output["function_call"]["arguments"], opts))


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

    # Use Ollama instead of OpenAI
    json_output = analyse_with_ollama(cv_content)

    LOGGER.info("Done analyse candidate")
    LOGGER.info(f"Time analyse candidate: {time.time() - start}")

    return json_output


async def analyse_with_ollama(cv_content):
    """Analyze candidate CV using Ollama local LLM"""
    
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
    """
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3.1",
                    "prompt": prompt,
                    "stream": False,
                    "format": "json"
                },
                timeout=120.0
            )
            
            if response.status_code == 200:
                result = response.json()
                return json.loads(result["response"])
            else:
                LOGGER.error(f"Ollama API error: {response.status_code}")
                return get_default_candidate_response()
                
    except Exception as e:
        LOGGER.error(f"Error calling Ollama: {str(e)}")
        return get_default_candidate_response()


def get_default_candidate_response():
    """Return default response when Ollama fails"""
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

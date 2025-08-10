import json
import time
import os
import google.generativeai as genai

from src.job.config import job_config
from src.job.prompts import fn_job_analysis, system_prompt_job
from src.utils import LOGGER


def analyse_job(job_data):
    start = time.time()
    LOGGER.info("Start analyse job")

    # Use Gemini instead of Ollama
    json_output = analyse_job_with_gemini(job_data.job_description)

    LOGGER.info("Done analyse job")
    LOGGER.info(f"Time analyse job: {time.time() - start}")

    return json_output


def analyse_job_with_gemini(job_description):
    """Analyze job description using Google Gemini"""
    
    # Configure Gemini
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        LOGGER.error("GEMINI_API_KEY not found in environment variables")
        return get_default_job_response()
    
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    {system_prompt_job}
    
    Please analyze the following job description and extract the requirements in JSON format:
    
    Job Description:
    {job_description}
    
    Return a JSON object with the following structure:
    {{
        "degree": ["array of educational requirements"],
        "experience": ["array of experience requirements"],
        "technical_skill": ["array of technical skills"],
        "responsibility": ["array of job responsibilities"],
        "certificate": ["array of required certificates"],
        "soft_skill": ["array of soft skills"]
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
        return get_default_job_response()


def get_default_job_response():
    """Return default response when Gemini fails"""
    return {
        "degree": [],
        "experience": [],
        "technical_skill": [],
        "responsibility": [],
        "certificate": [],
        "soft_skill": []
    }
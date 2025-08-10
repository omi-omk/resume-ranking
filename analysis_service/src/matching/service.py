import json
import time
import os
import google.generativeai as genai

from src.matching.config import matching_config
from src.matching.prompts import fn_matching_analysis, system_prompt_matching
from src.utils import LOGGER


def generate_content(job, candidate):
    content = "\nRequirement:" + str(job) + "\nCandidate:" + str(candidate)
    return content


def analyse_matching(matching_data):
    start = time.time()
    LOGGER.info("Start analyse matching")

    content = generate_content(job=matching_data.job, candidate=matching_data.candidate)

    # Use Gemini instead of Ollama
    json_output = analyse_matching_with_gemini(content)

    # Extract scores and store them in a list
    weights = {
        "degree": 0.1,  # The importance of the candidate's degree
        "experience": 0.2,  # The weight given to the candidate's relevant work experience
        "technical_skill": 0.3,  # Weight for technical skills and qualifications
        "responsibility": 0.25,  # How well the candidate's past responsibilities align with the job
        "certificate": 0.1,  # The significance of relevant certifications
        "soft_skill": 0.05,  # Importance of soft skills like communication, teamwork, etc.
    }
    total_weight = 0
    weighted_score = 0

    for section in json_output:
        if section != "summary_comment":
            weighted_score += int(json_output[section]["score"]) * weights[section]
            total_weight += weights[section]

    final_score = weighted_score / total_weight

    json_output["score"] = final_score

    LOGGER.info("Done analyse matching")
    LOGGER.info(f"Time analyse matching: {time.time() - start}")

    return json_output


def analyse_matching_with_gemini(content):
    """Analyze candidate-job matching using Google Gemini"""
    
    # Configure Gemini
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        LOGGER.error("GEMINI_API_KEY not found in environment variables")
        return get_default_matching_response()
    
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    {system_prompt_matching}
    
    Please analyze the matching between candidate and job requirements:
    
    {content}
    
    Return a JSON object with detailed scoring and comments for each category:
    {{
        "degree": {{"score": 0-100, "comment": "explanation"}},
        "experience": {{"score": 0-100, "comment": "explanation"}},
        "technical_skill": {{"score": 0-100, "comment": "explanation"}},
        "responsibility": {{"score": 0-100, "comment": "explanation"}},
        "certificate": {{"score": 0-100, "comment": "explanation"}},
        "soft_skill": {{"score": 0-100, "comment": "explanation"}},
        "summary_comment": "overall assessment"
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
        return get_default_matching_response()


def get_default_matching_response():
    """Return default response when Gemini fails"""
    return {
        "degree": {"score": 0, "comment": "Analysis failed"},
        "experience": {"score": 0, "comment": "Analysis failed"},
        "technical_skill": {"score": 0, "comment": "Analysis failed"},
        "responsibility": {"score": 0, "comment": "Analysis failed"},
        "certificate": {"score": 0, "comment": "Analysis failed"},
        "soft_skill": {"score": 0, "comment": "Analysis failed"},
        "summary_comment": "Analysis failed - please try again"
    }
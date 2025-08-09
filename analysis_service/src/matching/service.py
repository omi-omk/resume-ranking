import json
import time
import httpx

from src.matching.config import matching_config
from src.matching.prompts import fn_matching_analysis, system_prompt_matching
from src.utils import LOGGER


def output2json(output):
    """GPT Output Object >>> json"""
    opts = jsbeautifier.default_options()
    return json.loads(jsbeautifier.beautify(output["function_call"]["arguments"], opts))


def generate_content(job, candidate):
    content = "\nRequirement:" + str(job) + "\nCandidate:" + str(candidate)
    return content


def analyse_matching(matching_data):
    start = time.time()
    LOGGER.info("Start analyse matching")

    content = generate_content(job=matching_data.job, candidate=matching_data.candidate)

    # Use Ollama instead of OpenAI
    json_output = analyse_matching_with_ollama(content)

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


async def analyse_matching_with_ollama(content):
    """Analyze candidate-job matching using Ollama local LLM"""
    
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
                return get_default_matching_response()
                
    except Exception as e:
        LOGGER.error(f"Error calling Ollama: {str(e)}")
        return get_default_matching_response()


def get_default_matching_response():
    """Return default response when Ollama fails"""
    return {
        "degree": {"score": 0, "comment": "Analysis failed"},
        "experience": {"score": 0, "comment": "Analysis failed"},
        "technical_skill": {"score": 0, "comment": "Analysis failed"},
        "responsibility": {"score": 0, "comment": "Analysis failed"},
        "certificate": {"score": 0, "comment": "Analysis failed"},
        "soft_skill": {"score": 0, "comment": "Analysis failed"},
        "summary_comment": "Analysis failed - please try again"
    }

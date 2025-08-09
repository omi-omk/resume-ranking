import json
import time
import httpx

from src.job.config import job_config
from src.job.prompts import fn_job_analysis, system_prompt_job
from src.utils import LOGGER


def output2json(output):
    """GPT Output Object >>> json"""
    opts = jsbeautifier.default_options()
    return json.loads(jsbeautifier.beautify(output["function_call"]["arguments"], opts))


def analyse_job(job_data):
    start = time.time()
    LOGGER.info("Start analyse job")

    # Use Ollama instead of OpenAI
    json_output = analyse_job_with_ollama(job_data.job_description)

    LOGGER.info("Done analyse job")
    LOGGER.info(f"Time analyse job: {time.time() - start}")

    return json_output


async def analyse_job_with_ollama(job_description):
    """Analyze job description using Ollama local LLM"""
    
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
                return get_default_job_response()
                
    except Exception as e:
        LOGGER.error(f"Error calling Ollama: {str(e)}")
        return get_default_job_response()


def get_default_job_response():
    """Return default response when Ollama fails"""
    return {
        "degree": [],
        "experience": [],
        "technical_skill": [],
        "responsibility": [],
        "certificate": [],
        "soft_skill": []
    }

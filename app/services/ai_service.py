import json
import os
import logging
import google.generativeai as genai
from app.core.config import settings

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        if not settings.GEMINI_API_KEY:
            logger.error("GEMINI_API_KEY not found in environment variables")
            raise ValueError("GEMINI_API_KEY is required")
        
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def analyze_candidate(self, cv_content: str) -> dict:
        """Analyze candidate CV using Google Gemini"""
        
        system_prompt = """
        Let's think step by step.
        CV details might be out of order or incomplete.
        Analyze the CV concerning the candidate's experience and career. From this, derive logical conclusions about their technical skills, experience, and soft skills.
        The format for educational qualifications should be: Degree - School/University/Organization - GPA - Year of Graduation. It's acceptable if some details are missing.
        Experience should include experienced time and job name field of work based on projects and experiences.
        Ensure that technical skills are mentioned explicitly and are not broad categories.
        Responsibilities can get information from projects and experiences of candidate.
        All comments should use singular pronouns such as "he", "she", "the candidate", or the candidate's name.
        """
        
        prompt = f"""
        {system_prompt}
        
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
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            return json.loads(response_text.strip())
            
        except Exception as e:
            logger.error(f"Error analyzing candidate with Gemini: {str(e)}")
            return self._get_default_candidate_response()

    async def analyze_job(self, job_description: str) -> dict:
        """Analyze job description using Google Gemini"""
        
        system_prompt = """
        Let's think step by step.
        Respond using only the provided information and do not rely on your basic knowledge. The details given might be out of sequence or incomplete.
        Experience should include required duration time and job name field of work.
        Only use the given data to determine educational qualifications and certificates; do not make assumptions about these qualifications.
        However, you are allowed to combine the provided details to draw logical conclusions about soft skills.
        """
        
        prompt = f"""
        {system_prompt}
        
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
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            return json.loads(response_text.strip())
            
        except Exception as e:
            logger.error(f"Error analyzing job with Gemini: {str(e)}")
            return self._get_default_job_response()

    async def analyze_matching(self, candidate: dict, job: dict) -> dict:
        """Analyze candidate-job matching using Google Gemini"""
        
        system_prompt = """
        Scoring Guide:
        It's ok to say candidate does not match the requirement.
        Degree Section: Prioritize major than degree level. Candidate with degrees more directly relevant to the required degree should receive higher score, even if their degree level is lower.
        Experience Section: Candidate with more relevant experience field get higher score.
        Technical Skills Section: Candidate with more relevant technical skills get higher score.
        Responsibilities Section: Candidate with more relevant responsibilities get higher score.
        Certificates Section: Candidate with required certificates get higher score. Candidate without required certificates get no score. Candidate with related certificates to the position get medium score.
        Soft Skills Section: Prioritize foreign language and leadership skills. Candidate with more relevant soft skills get higher score.
        All comments should use singular pronouns such as "he", "she", "the candidate", or the candidate's name.
        """
        
        content = f"\nRequirement: {str(job)}\nCandidate: {str(candidate)}"
        
        prompt = f"""
        {system_prompt}
        
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
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            result = json.loads(response_text.strip())
            
            # Calculate weighted score
            weights = {
                "degree": 0.1,
                "experience": 0.2,
                "technical_skill": 0.3,
                "responsibility": 0.25,
                "certificate": 0.1,
                "soft_skill": 0.05,
            }
            
            weighted_score = 0
            for section, weight in weights.items():
                if section in result:
                    weighted_score += result[section]["score"] * weight
            
            result["score"] = weighted_score
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing matching with Gemini: {str(e)}")
            return self._get_default_matching_response()

    def _get_default_candidate_response(self):
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

    def _get_default_job_response(self):
        """Return default response when Gemini fails"""
        return {
            "degree": [],
            "experience": [],
            "technical_skill": [],
            "responsibility": [],
            "certificate": [],
            "soft_skill": []
        }

    def _get_default_matching_response(self):
        """Return default response when Gemini fails"""
        return {
            "degree": {"score": 0, "comment": "Analysis failed"},
            "experience": {"score": 0, "comment": "Analysis failed"},
            "technical_skill": {"score": 0, "comment": "Analysis failed"},
            "responsibility": {"score": 0, "comment": "Analysis failed"},
            "certificate": {"score": 0, "comment": "Analysis failed"},
            "soft_skill": {"score": 0, "comment": "Analysis failed"},
            "summary_comment": "Analysis failed - please try again",
            "score": 0
        }


# Global AI service instance
ai_service = AIService()
export interface Job {
  _id: string
  job_name: string
  job_description: string
  created_at: string
  degree?: string[]
  experience?: string[]
  technical_skill?: string[]
  responsibility?: string[]
  certificate?: string[]
  soft_skill?: string[]
}

export interface Candidate {
  _id: string
  candidate_name: string
  phone_number: string
  email: string
  comment: string
  job_recommended: string[]
  cv_name: string
  created_at: string
  degree: string[]
  experience: string[]
  responsibility: string[]
  soft_skill: string[]
  technical_skill: string[]
  certificate: string[]
}

export interface CandidateResponse {
  results: Candidate[]
  total_file: number
  total_page: number
}

export interface MatchingResult {
  id: string
  candidate_name: string
  candidate_email: string
  candidate_phone: string
  cv_name: string
  score: number
  comment: string
  matching_status: boolean
}

export interface MatchingResponse {
  results: MatchingResult[]
  total_page: number
  total_matching: number
}
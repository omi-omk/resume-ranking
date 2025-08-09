import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)
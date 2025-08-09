'use client'

import { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { CloudArrowUpIcon, DocumentIcon } from '@heroicons/react/24/outline'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '@/lib/api'
import toast from 'react-hot-toast'

export function UploadCandidates() {
  const queryClient = useQueryClient()

  const uploadMutation = useMutation({
    mutationFn: (files: File[]) => {
      const formData = new FormData()
      files.forEach(file => formData.append('file_upload', file))
      return api.post('/upload-cv', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['candidates'] })
      toast.success('Candidates uploaded successfully')
    },
    onError: () => {
      toast.error('Failed to upload candidates')
    }
  })

  const onDrop = useCallback((acceptedFiles: File[]) => {
    uploadMutation.mutate(acceptedFiles)
  }, [uploadMutation])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']
    },
    multiple: true
  })

  return (
    <div className="card p-6">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">Upload Candidate Resumes</h2>
      
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
          isDragActive 
            ? 'border-primary-500 bg-primary-50' 
            : 'border-gray-300 hover:border-gray-400'
        }`}
      >
        <input {...getInputProps()} />
        
        <div className="space-y-4">
          <div className="flex justify-center">
            {uploadMutation.isPending ? (
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600" />
            ) : (
              <CloudArrowUpIcon className="h-12 w-12 text-gray-400" />
            )}
          </div>
          
          <div>
            <p className="text-lg font-medium text-gray-900">
              {isDragActive ? 'Drop files here' : 'Drag & drop resume files here'}
            </p>
            <p className="text-gray-600">or click to browse</p>
            <p className="text-sm text-gray-500 mt-2">
              Supports PDF and DOCX files
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
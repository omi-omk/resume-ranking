'use client'

import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { ChevronDownIcon, SparklesIcon } from '@heroicons/react/24/outline'
import { api } from '@/lib/api'
import toast from 'react-hot-toast'

export function JobSelector() {
  const [selectedJob, setSelectedJob] = useState<string>('')
  const queryClient = useQueryClient()

  const { data: jobs } = useQuery({
    queryKey: ['jobs'],
    queryFn: () => api.get('/job')
  })

  const matchingMutation = useMutation({
    mutationFn: (jobName: string) => api.post('/process-matching', { job_name: jobName }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['matching'] })
      toast.success('Matching process completed')
    },
    onError: () => {
      toast.error('Failed to process matching')
    }
  })

  const handleMatch = () => {
    if (!selectedJob) {
      toast.error('Please select a job first')
      return
    }
    matchingMutation.mutate(selectedJob)
  }

  return (
    <div className="card p-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className="relative">
            <select
              value={selectedJob}
              onChange={(e) => setSelectedJob(e.target.value)}
              className="appearance-none bg-white border border-gray-300 rounded-md px-4 py-2 pr-8 focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="">Select a job position</option>
              {jobs?.map((job: any) => (
                <option key={job._id} value={job.job_name}>
                  {job.job_name}
                </option>
              ))}
            </select>
            <ChevronDownIcon className="absolute right-2 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400 pointer-events-none" />
          </div>
        </div>

        <button
          onClick={handleMatch}
          disabled={!selectedJob || matchingMutation.isPending}
          className="btn btn-primary px-4 py-2 disabled:opacity-50"
        >
          <SparklesIcon className="h-4 w-4 mr-2" />
          {matchingMutation.isPending ? 'Processing...' : 'Start Matching'}
        </button>
      </div>
    </div>
  )
}
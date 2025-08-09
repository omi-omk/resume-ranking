'use client'

import { useQuery } from '@tanstack/react-query'
import { EyeIcon } from '@heroicons/react/24/outline'
import { api } from '@/lib/api'

export function MatchingTable() {
  const { data: matching, isLoading } = useQuery({
    queryKey: ['matching'],
    queryFn: () => api.post('/data-matching', { 
      job_name: 'All Jobs', 
      page: 1, 
      page_size: 10 
    })
  })

  if (isLoading) {
    return <div className="animate-pulse">Loading matching results...</div>
  }

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600 bg-green-100'
    if (score >= 60) return 'text-blue-600 bg-blue-100'
    if (score >= 40) return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
  }

  return (
    <div className="space-y-4">
      <h2 className="text-lg font-semibold text-gray-900">Matching Results</h2>
      
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Candidate
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Email
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Match Score
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {matching?.results?.map((match: any) => (
              <tr key={match.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm font-medium text-gray-900">
                    {match.candidate_name}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {match.candidate_email}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getScoreColor(match.score)}`}>
                    {match.score}%
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                    match.matching_status 
                      ? 'text-green-800 bg-green-100' 
                      : 'text-gray-800 bg-gray-100'
                  }`}>
                    {match.matching_status ? 'Matched' : 'Pending'}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <button className="text-blue-600 hover:text-blue-900">
                    <EyeIcon className="h-4 w-4" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
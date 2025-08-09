'use client'

import { useQuery } from '@tanstack/react-query'
import { EyeIcon, TrashIcon } from '@heroicons/react/24/outline'
import { api } from '@/lib/api'

export function CandidatesTable() {
  const { data: candidates, isLoading } = useQuery({
    queryKey: ['candidates'],
    queryFn: () => api.post('/list-candidate', { page: 1, page_size: 10 })
  })

  if (isLoading) {
    return <div className="animate-pulse">Loading candidates...</div>
  }

  return (
    <div className="space-y-4">
      <h2 className="text-lg font-semibold text-gray-900">Uploaded Candidates</h2>
      
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Name
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Email
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                CV File
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Upload Date
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {candidates?.results?.map((candidate: any) => (
              <tr key={candidate._id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm font-medium text-gray-900">
                    {candidate.candidate_name}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {candidate.email}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {candidate.cv_name}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {new Date(candidate.created_at).toLocaleDateString()}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <div className="flex justify-end space-x-2">
                    <button className="text-blue-600 hover:text-blue-900">
                      <EyeIcon className="h-4 w-4" />
                    </button>
                    <button className="text-red-600 hover:text-red-900">
                      <TrashIcon className="h-4 w-4" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
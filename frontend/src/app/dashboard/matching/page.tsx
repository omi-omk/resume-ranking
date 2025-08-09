import { MatchingTable } from '@/components/matching/matching-table'
import { JobSelector } from '@/components/matching/job-selector'

export default function MatchingPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Matching</h1>
        <p className="text-gray-600">Match candidates with job opportunities</p>
      </div>
      
      <JobSelector />
      
      <div className="card p-6">
        <MatchingTable />
      </div>
    </div>
  )
}
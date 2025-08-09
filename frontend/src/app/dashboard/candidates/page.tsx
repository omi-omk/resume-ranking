import { CandidatesTable } from '@/components/candidates/candidates-table'
import { UploadCandidates } from '@/components/candidates/upload-candidates'

export default function CandidatesPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Candidates</h1>
        <p className="text-gray-600">Upload and manage candidate resumes</p>
      </div>
      
      <UploadCandidates />
      
      <div className="card p-6">
        <CandidatesTable />
      </div>
    </div>
  )
}
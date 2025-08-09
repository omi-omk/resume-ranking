import { JobsTable } from '@/components/jobs/jobs-table'
import { CreateJobButton } from '@/components/jobs/create-job-button'

export default function JobsPage() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Jobs</h1>
          <p className="text-gray-600">Manage job positions and requirements</p>
        </div>
        <CreateJobButton />
      </div>
      
      <div className="card p-6">
        <JobsTable />
      </div>
    </div>
  )
}
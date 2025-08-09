import { StatsCards } from '@/components/dashboard/stats-cards'
import { RecentActivity } from '@/components/dashboard/recent-activity'

export default function Dashboard() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600">Welcome to your resume ranking dashboard</p>
      </div>
      
      <StatsCards />
      <RecentActivity />
    </div>
  )
}
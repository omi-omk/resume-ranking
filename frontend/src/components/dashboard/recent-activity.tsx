'use client'

export function RecentActivity() {
  const activities = [
    { id: 1, action: 'New candidate uploaded', time: '2 minutes ago' },
    { id: 2, action: 'Job "AI Engineer" created', time: '1 hour ago' },
    { id: 3, action: 'Matching completed for "Frontend Developer"', time: '3 hours ago' },
  ]

  return (
    <div className="card p-6">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h2>
      <div className="space-y-3">
        {activities.map((activity) => (
          <div key={activity.id} className="flex justify-between items-center py-2">
            <span className="text-gray-700">{activity.action}</span>
            <span className="text-sm text-gray-500">{activity.time}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
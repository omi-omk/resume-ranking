'use client'

import { useQuery } from '@tanstack/react-query'
import { BriefcaseIcon, UsersIcon, ChartBarIcon } from '@heroicons/react/24/outline'

export function StatsCards() {
  const { data: stats } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: async () => {
      // Mock data - replace with actual API call
      return {
        totalJobs: 12,
        totalCandidates: 45,
        totalMatches: 23
      }
    }
  })

  const cards = [
    {
      title: 'Total Jobs',
      value: stats?.totalJobs || 0,
      icon: BriefcaseIcon,
      color: 'text-blue-600'
    },
    {
      title: 'Total Candidates',
      value: stats?.totalCandidates || 0,
      icon: UsersIcon,
      color: 'text-green-600'
    },
    {
      title: 'Matches Made',
      value: stats?.totalMatches || 0,
      icon: ChartBarIcon,
      color: 'text-purple-600'
    }
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {cards.map((card) => (
        <div key={card.title} className="card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">{card.title}</p>
              <p className="text-3xl font-bold text-gray-900">{card.value}</p>
            </div>
            <card.icon className={`h-8 w-8 ${card.color}`} />
          </div>
        </div>
      ))}
    </div>
  )
}
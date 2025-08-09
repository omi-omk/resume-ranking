'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { 
  HomeIcon, 
  BriefcaseIcon, 
  UsersIcon, 
  ChartBarIcon 
} from '@heroicons/react/24/outline'
import { clsx } from 'clsx'

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: HomeIcon },
  { name: 'Jobs', href: '/dashboard/jobs', icon: BriefcaseIcon },
  { name: 'Candidates', href: '/dashboard/candidates', icon: UsersIcon },
  { name: 'Matching', href: '/dashboard/matching', icon: ChartBarIcon },
]

export function Sidebar() {
  const pathname = usePathname()

  return (
    <div className="fixed inset-y-0 left-0 z-40 w-64 bg-white border-r border-gray-200 pt-16">
      <nav className="p-4 space-y-2">
        {navigation.map((item) => {
          const isActive = pathname === item.href
          return (
            <Link
              key={item.name}
              href={item.href}
              className={clsx(
                'flex items-center space-x-3 px-3 py-2 rounded-md text-sm font-medium transition-colors',
                isActive
                  ? 'bg-primary-50 text-primary-700 border-r-2 border-primary-700'
                  : 'text-gray-700 hover:bg-gray-100'
              )}
            >
              <item.icon className="h-5 w-5" />
              <span>{item.name}</span>
            </Link>
          )
        })}
      </nav>
    </div>
  )
}
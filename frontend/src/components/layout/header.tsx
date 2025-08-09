'use client'

import { Bars3Icon } from '@heroicons/react/24/outline'

export function Header() {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-white border-b border-gray-200">
      <div className="flex items-center justify-between px-6 py-4">
        <div className="flex items-center space-x-4">
          <button className="lg:hidden">
            <Bars3Icon className="h-6 w-6" />
          </button>
          <h1 className="text-xl font-bold text-gray-900">Resume Ranking</h1>
        </div>
        
        <div className="flex items-center space-x-4">
          <div className="text-sm text-gray-600">
            AI-Powered Recruitment
          </div>
        </div>
      </div>
    </header>
  )
}
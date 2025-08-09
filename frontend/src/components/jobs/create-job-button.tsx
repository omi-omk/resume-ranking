'use client'

import { useState } from 'react'
import { PlusIcon } from '@heroicons/react/24/outline'
import { CreateJobModal } from './create-job-modal'

export function CreateJobButton() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <>
      <button
        onClick={() => setIsOpen(true)}
        className="btn btn-primary px-4 py-2"
      >
        <PlusIcon className="h-4 w-4 mr-2" />
        Create Job
      </button>
      
      <CreateJobModal isOpen={isOpen} onClose={() => setIsOpen(false)} />
    </>
  )
}
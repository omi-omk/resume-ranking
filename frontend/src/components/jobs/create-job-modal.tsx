'use client'

import { Fragment } from 'react'
import { Dialog, Transition } from '@headlessui/react'
import { XMarkIcon } from '@heroicons/react/24/outline'
import { useForm } from 'react-hook-form'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '@/lib/api'
import toast from 'react-hot-toast'

interface CreateJobModalProps {
  isOpen: boolean
  onClose: () => void
}

interface JobFormData {
  job_name: string
  job_description: string
}

export function CreateJobModal({ isOpen, onClose }: CreateJobModalProps) {
  const queryClient = useQueryClient()
  const { register, handleSubmit, reset, formState: { errors } } = useForm<JobFormData>()

  const createJobMutation = useMutation({
    mutationFn: (data: JobFormData) => api.post('/job', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['jobs'] })
      toast.success('Job created successfully')
      reset()
      onClose()
    },
    onError: () => {
      toast.error('Failed to create job')
    }
  })

  const onSubmit = (data: JobFormData) => {
    createJobMutation.mutate(data)
  }

  return (
    <Transition appear show={isOpen} as={Fragment}>
      <Dialog as="div" className="relative z-50" onClose={onClose}>
        <Transition.Child
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-black bg-opacity-25" />
        </Transition.Child>

        <div className="fixed inset-0 overflow-y-auto">
          <div className="flex min-h-full items-center justify-center p-4">
            <Transition.Child
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 scale-95"
              enterTo="opacity-100 scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 scale-100"
              leaveTo="opacity-0 scale-95"
            >
              <Dialog.Panel className="w-full max-w-2xl transform overflow-hidden rounded-lg bg-white p-6 shadow-xl transition-all">
                <div className="flex items-center justify-between mb-4">
                  <Dialog.Title className="text-lg font-medium text-gray-900">
                    Create New Job
                  </Dialog.Title>
                  <button
                    onClick={onClose}
                    className="text-gray-400 hover:text-gray-600"
                  >
                    <XMarkIcon className="h-6 w-6" />
                  </button>
                </div>

                <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Job Title
                    </label>
                    <input
                      {...register('job_name', { required: 'Job title is required' })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                      placeholder="e.g., Senior Frontend Developer"
                    />
                    {errors.job_name && (
                      <p className="text-red-500 text-sm mt-1">{errors.job_name.message}</p>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Job Description
                    </label>
                    <textarea
                      {...register('job_description', { required: 'Job description is required' })}
                      rows={8}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                      placeholder="Describe the job requirements, responsibilities, and qualifications..."
                    />
                    {errors.job_description && (
                      <p className="text-red-500 text-sm mt-1">{errors.job_description.message}</p>
                    )}
                  </div>

                  <div className="flex justify-end space-x-3 pt-4">
                    <button
                      type="button"
                      onClick={onClose}
                      className="btn btn-secondary px-4 py-2"
                    >
                      Cancel
                    </button>
                    <button
                      type="submit"
                      disabled={createJobMutation.isPending}
                      className="btn btn-primary px-4 py-2 disabled:opacity-50"
                    >
                      {createJobMutation.isPending ? 'Creating...' : 'Create Job'}
                    </button>
                  </div>
                </form>
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </div>
      </Dialog>
    </Transition>
  )
}
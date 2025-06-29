import type { ReactNode } from 'react'

interface PageLayoutProps {
  children: ReactNode
  className?: string
}

export function PageLayout({ children, className = '' }: PageLayoutProps) {
  return (
    <div className={`w-full space-y-4 sm:space-y-6 p-3 sm:p-6 min-w-0 ${className}`}>
      {children}
    </div>
  )
} 
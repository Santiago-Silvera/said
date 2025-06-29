import type { ReactNode } from 'react'

interface StatsGridProps {
  children: ReactNode
  columns?: 1 | 2 | 3 | 4
  className?: string
}

const gridConfig = {
  1: 'grid-cols-1',
  2: 'grid-cols-1 sm:grid-cols-2',
  3: 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3',
  4: 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-4',
}

export function StatsGrid({ children, columns = 4, className = '' }: StatsGridProps) {
  return (
    <div className={`grid ${gridConfig[columns]} gap-4 sm:gap-6 ${className}`}>
      {children}
    </div>
  )
} 
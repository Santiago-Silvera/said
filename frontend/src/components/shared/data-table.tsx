import type { ReactNode } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

interface DataTableProps {
  title: string
  children: ReactNode
  className?: string
}

export function DataTable({ title, children, className = '' }: DataTableProps) {
  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent className="overflow-x-auto">
        {children}
      </CardContent>
    </Card>
  )
} 
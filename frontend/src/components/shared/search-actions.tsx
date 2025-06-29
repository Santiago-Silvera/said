import { Search, Plus } from 'lucide-react'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'

interface SearchAndActionsProps {
  searchTerm: string
  onSearchChange: (value: string) => void
  searchPlaceholder: string
  actionLabel: string
  onActionClick: () => void
  className?: string
}

export function SearchAndActions({
  searchTerm,
  onSearchChange,
  searchPlaceholder,
  actionLabel,
  onActionClick,
  className = ''
}: SearchAndActionsProps) {
  return (
    <div className={`flex flex-col sm:flex-row gap-4 justify-between items-start sm:items-center ${className}`}>
      <div className="relative w-full sm:w-96">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground" size={16} />
        <Input
          placeholder={searchPlaceholder}
          value={searchTerm}
          onChange={(e) => onSearchChange(e.target.value)}
          className="pl-10"
        />
      </div>
      <Button className="w-full sm:w-auto" onClick={onActionClick}>
        <Plus size={16} className="mr-2" />
        {actionLabel}
      </Button>
    </div>
  )
} 
import { Bell, Search, HelpCircle } from 'lucide-react'
import { useLocation } from 'react-router-dom'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { SidebarTrigger } from '@/components/ui/sidebar'

export function Header() {
  const location = useLocation()
  
  const getTitle = () => {
    switch (location.pathname) {
      case '/':
        return 'Dashboard'
      case '/professors':
        return 'Professor Management'
      case '/courses':
        return 'Course Management'
      case '/departments':
        return 'Department Management'
      case '/schedule':
        return 'Schedule Management'
      case '/reports':
        return 'Reports'
      case '/settings':
        return 'Settings'
      default:
        if (location.pathname.startsWith('/professors/')) {
          return 'Professor Details'
        }
        return 'Dashboard'
    }
  }

  return (
    <header className="bg-background border-b px-4 py-4 flex-shrink-0">
      <div className="flex justify-between items-center min-w-0">
        <div className="flex items-center gap-4 min-w-0">
          <SidebarTrigger />
          <h1 className="text-xl font-bold text-foreground truncate">{getTitle()}</h1>
        </div>
        <div className="flex items-center gap-2 min-w-0">
          <div className="relative w-48 sm:w-64">
            <Search
              className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground"
              size={18}
            />
            <Input
              type="text"
              placeholder="Search..."
              className="pl-10"
            />
          </div>
          <Button variant="ghost" size="sm" className="relative p-2 h-10 w-10 flex-shrink-0">
            <Bell size={20} />
            <span className="absolute top-2 right-2 w-2 h-2 bg-destructive rounded-full"></span>
          </Button>
          <Button variant="ghost" size="sm" className="p-2 h-10 w-10 flex-shrink-0">
            <HelpCircle size={20} />
          </Button>
        </div>
      </div>
    </header>
  )
} 
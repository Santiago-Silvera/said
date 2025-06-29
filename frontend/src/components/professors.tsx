import { useState } from 'react'
import { Link } from 'react-router-dom'
import { 
  Users, 
  UserCheck, 
  UserX, 
  Clock, 
  ArrowUpDown,
  MoreHorizontal,
  Pencil,
  Trash2,
  Eye
} from 'lucide-react'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableHead, 
  TableHeader, 
  TableRow 
} from '@/components/ui/table'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { 
  MOCK_PROFESSORS, 
  getProfessorStats, 
  type Professor 
} from '@/data/professors'
import { 
  StatCard, 
  PageLayout, 
  StatsGrid, 
  SearchAndActions, 
  DataTable 
} from '@/components/shared'

const getStatusBadge = (status: Professor['status']) => {
  const variants = {
    'Active': 'default' as const,
    'On Leave': 'secondary' as const,
    'Inactive': 'destructive' as const,
  }
  
  return <Badge variant={variants[status]}>{status}</Badge>
}

export function Professors() {
  const [searchTerm, setSearchTerm] = useState('')
  const stats = getProfessorStats()

  const filteredProfessors = MOCK_PROFESSORS.filter(professor =>
    professor.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    professor.department.toLowerCase().includes(searchTerm.toLowerCase()) ||
    professor.email.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const handleAddProfessor = () => {
    // TODO: Implement add professor functionality
    console.log('Add professor clicked')
  }

  return (
    <PageLayout>
      {/* Stats Overview */}
      <StatsGrid columns={4}>
        <StatCard
          title="Total Professors"
          value={stats.total}
          icon={Users}
          color="blue"
        />
        <StatCard
          title="Active"
          value={stats.active}
          icon={UserCheck}
          color="green"
          subtitle={`${stats.activePercentage}% of total`}
        />
        <StatCard
          title="On Leave"
          value={stats.onLeave}
          icon={Clock}
          color="yellow"
        />
        <StatCard
          title="Inactive"
          value={stats.inactive}
          icon={UserX}
          color="red"
        />
      </StatsGrid>

      {/* Search and Actions */}
      <SearchAndActions
        searchTerm={searchTerm}
        onSearchChange={setSearchTerm}
        searchPlaceholder="Search professors..."
        actionLabel="Add Professor"
        onActionClick={handleAddProfessor}
      />

      {/* Professors Table */}
      <DataTable title="Professors">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>
                <div className="flex items-center gap-1">
                  Name
                  <Button variant="ghost" size="sm" className="h-6 w-6 p-0">
                    <ArrowUpDown size={12} />
                  </Button>
                </div>
              </TableHead>
              <TableHead>Department</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Courses</TableHead>
              <TableHead>Contact</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filteredProfessors.map((professor) => (
              <TableRow key={professor.id}>
                <TableCell>
                  <div className="flex items-center gap-3 min-w-0">
                    <img
                      src={professor.imageUrl}
                      alt={professor.name}
                      className="w-10 h-10 rounded-full object-cover flex-shrink-0"
                    />
                    <div className="min-w-0 flex-1">
                      <Link 
                        to={`/professors/${professor.id}`}
                        className="font-medium hover:text-primary transition-colors truncate block"
                      >
                        {professor.name}
                      </Link>
                      <p className="text-sm text-muted-foreground truncate">{professor.email}</p>
                    </div>
                  </div>
                </TableCell>
                <TableCell className="truncate">{professor.department}</TableCell>
                <TableCell>{getStatusBadge(professor.status)}</TableCell>
                <TableCell>
                  <div className="flex flex-wrap gap-1">
                    {professor.courses.slice(0, 2).map((course, index) => (
                      <Badge key={index} variant="outline" className="text-xs">
                        {course}
                      </Badge>
                    ))}
                    {professor.courses.length > 2 && (
                      <Badge variant="outline" className="text-xs">
                        +{professor.courses.length - 2} more
                      </Badge>
                    )}
                  </div>
                </TableCell>
                <TableCell className="truncate">
                  <p className="text-sm">{professor.phone}</p>
                </TableCell>
                <TableCell className="text-right">
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
                        <MoreHorizontal size={16} />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuItem asChild>
                        <Link to={`/professors/${professor.id}`}>
                          <Eye size={16} className="mr-2" />
                          View Details
                        </Link>
                      </DropdownMenuItem>
                      <DropdownMenuItem>
                        <Pencil size={16} className="mr-2" />
                        Edit
                      </DropdownMenuItem>
                      <DropdownMenuItem className="text-destructive">
                        <Trash2 size={16} className="mr-2" />
                        Delete
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </DataTable>
    </PageLayout>
  )
} 
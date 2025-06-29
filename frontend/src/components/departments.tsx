import { useState } from 'react'
import { 
  Building2, 
  Users, 
  BookOpen, 
  GraduationCap, 
  DollarSign, 
  ArrowUpDown,
  MoreHorizontal,
  Pencil,
  Trash2,
  Eye,
  Mail,
  Phone,
  MapPin
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
  MOCK_DEPARTMENTS, 
  getDepartmentStats, 
  type Department 
} from '@/data/departments'
import { 
  StatCard, 
  PageLayout, 
  StatsGrid, 
  SearchAndActions, 
  DataTable 
} from '@/components/shared'

const formatBudget = (budget: number) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(budget)
}

export function Departments() {
  const [searchTerm, setSearchTerm] = useState('')
  const stats = getDepartmentStats()

  const filteredDepartments = MOCK_DEPARTMENTS.filter(department =>
    department.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    department.code.toLowerCase().includes(searchTerm.toLowerCase()) ||
    department.chair.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const handleAddDepartment = () => {
    // TODO: Implement add department functionality
    console.log('Add department clicked')
  }

  return (
    <PageLayout>
      {/* Stats Overview */}
      <StatsGrid columns={4}>
        <StatCard
          title="Total Departments"
          value={stats.total}
          icon={Building2}
          color="blue"
        />
        <StatCard
          title="Active Departments"
          value={stats.active}
          icon={GraduationCap}
          color="green"
        />
        <StatCard
          title="Total Budget"
          value={formatBudget(stats.totalBudget)}
          icon={DollarSign}
          color="purple"
        />
        <StatCard
          title="Total Students"
          value={stats.totalStudents}
          icon={Users}
          color="yellow"
        />
      </StatsGrid>

      {/* Search and Actions */}
      <SearchAndActions
        searchTerm={searchTerm}
        onSearchChange={setSearchTerm}
        searchPlaceholder="Search departments..."
        actionLabel="Add Department"
        onActionClick={handleAddDepartment}
      />

      {/* Departments Table */}
      <DataTable title="Departments">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>
                <div className="flex items-center gap-1">
                  Department
                  <Button variant="ghost" size="sm" className="h-6 w-6 p-0">
                    <ArrowUpDown size={12} />
                  </Button>
                </div>
              </TableHead>
              <TableHead>Chair</TableHead>
              <TableHead>Contact</TableHead>
              <TableHead>Stats</TableHead>
              <TableHead>Budget</TableHead>
              <TableHead>Status</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filteredDepartments.map((department) => (
              <TableRow key={department.id}>
                <TableCell>
                  <div>
                    <p className="font-medium">{department.name}</p>
                    <p className="text-sm text-muted-foreground">{department.code}</p>
                  </div>
                </TableCell>
                <TableCell>
                  <div>
                    <p className="font-medium">{department.chair}</p>
                  </div>
                </TableCell>
                <TableCell>
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <Mail size={14} className="text-muted-foreground" />
                      <span className="text-sm">{department.email}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Phone size={14} className="text-muted-foreground" />
                      <span className="text-sm">{department.phone}</span>
                    </div>
                  </div>
                </TableCell>
                <TableCell>
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <Users size={14} className="text-muted-foreground" />
                      <span className="text-sm">{department.professors} professors</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <BookOpen size={14} className="text-muted-foreground" />
                      <span className="text-sm">{department.courses} courses</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <GraduationCap size={14} className="text-muted-foreground" />
                      <span className="text-sm">{department.students} students</span>
                    </div>
                  </div>
                </TableCell>
                <TableCell>
                  <p className="font-medium">{formatBudget(department.budget)}</p>
                </TableCell>
                <TableCell>
                  <Badge variant={department.status === 'Active' ? 'default' : 'secondary'}>
                    {department.status}
                  </Badge>
                </TableCell>
                <TableCell className="text-right">
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
                        <MoreHorizontal size={16} />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuItem>
                        <Eye size={16} className="mr-2" />
                        View Details
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
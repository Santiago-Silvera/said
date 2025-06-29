import { useState } from 'react'
import { 
  BookOpen, 
  Users, 
  Clock, 
  MapPin, 
  ArrowUpDown,
  MoreHorizontal,
  Pencil,
  Trash2,
  Eye,
  GraduationCap,
  Calendar
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
  MOCK_COURSES, 
  getCourseStats, 
  type Course 
} from '@/data/courses'
import { 
  StatCard, 
  PageLayout, 
  StatsGrid, 
  SearchAndActions, 
  DataTable 
} from '@/components/shared'

const getStatusBadge = (status: Course['status']) => {
  const variants = {
    'Active': 'default' as const,
    'Inactive': 'secondary' as const,
    'Full': 'destructive' as const,
  }
  
  return <Badge variant={variants[status]}>{status}</Badge>
}

export function Courses() {
  const [searchTerm, setSearchTerm] = useState('')
  const stats = getCourseStats()

  const filteredCourses = MOCK_COURSES.filter(course =>
    course.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    course.code.toLowerCase().includes(searchTerm.toLowerCase()) ||
    course.department.toLowerCase().includes(searchTerm.toLowerCase()) ||
    course.professor?.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const handleAddCourse = () => {
    // TODO: Implement add course functionality
    console.log('Add course clicked')
  }

  return (
    <PageLayout>
      {/* Stats Overview */}
      <StatsGrid columns={4}>
        <StatCard
          title="Total Courses"
          value={stats.total}
          icon={BookOpen}
          color="blue"
        />
        <StatCard
          title="Active Courses"
          value={stats.active}
          icon={GraduationCap}
          color="green"
        />
        <StatCard
          title="Total Enrolled"
          value={stats.totalEnrolled}
          icon={Users}
          color="purple"
          subtitle={`${stats.enrollmentRate}% capacity`}
        />
        <StatCard
          title="Inactive"
          value={stats.inactive}
          icon={Clock}
          color="red"
        />
      </StatsGrid>

      {/* Search and Actions */}
      <SearchAndActions
        searchTerm={searchTerm}
        onSearchChange={setSearchTerm}
        searchPlaceholder="Search courses..."
        actionLabel="Add Course"
        onActionClick={handleAddCourse}
      />

      {/* Courses Table */}
      <DataTable title="Courses">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>
                <div className="flex items-center gap-1">
                  Course
                  <Button variant="ghost" size="sm" className="h-6 w-6 p-0">
                    <ArrowUpDown size={12} />
                  </Button>
                </div>
              </TableHead>
              <TableHead>Department</TableHead>
              <TableHead>Professor</TableHead>
              <TableHead>Schedule</TableHead>
              <TableHead>Enrollment</TableHead>
              <TableHead>Status</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filteredCourses.map((course) => (
              <TableRow key={course.id}>
                <TableCell>
                  <div>
                    <p className="font-medium">{course.name}</p>
                    <p className="text-sm text-muted-foreground">{course.code}</p>
                    <p className="text-xs text-muted-foreground">{course.credits} credits</p>
                  </div>
                </TableCell>
                <TableCell>
                  <Badge variant="outline">{course.department}</Badge>
                </TableCell>
                <TableCell>
                  <p className="text-sm">{course.professor || 'Unassigned'}</p>
                </TableCell>
                <TableCell>
                  <div className="flex items-center gap-2">
                    <Calendar size={14} className="text-muted-foreground" />
                    <span className="text-sm">{course.schedule}</span>
                  </div>
                  <div className="flex items-center gap-2 mt-1">
                    <MapPin size={14} className="text-muted-foreground" />
                    <span className="text-xs text-muted-foreground">{course.location}</span>
                  </div>
                </TableCell>
                <TableCell>
                  <div className="text-sm">
                    <p>{course.enrolled}/{course.capacity}</p>
                    <div className="w-full bg-gray-200 rounded-full h-2 mt-1">
                      <div 
                        className="bg-blue-600 h-2 rounded-full" 
                        style={{ width: `${(course.enrolled / course.capacity) * 100}%` }}
                      ></div>
                    </div>
                  </div>
                </TableCell>
                <TableCell>{getStatusBadge(course.status)}</TableCell>
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
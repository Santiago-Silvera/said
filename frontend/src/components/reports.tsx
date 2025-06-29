import { useState } from 'react'
import { 
  BarChart3, 
  TrendingUp, 
  Users, 
  BookOpen, 
  Building2, 
  Calendar,
  Download,
  Filter,
  Eye,
  FileText,
  PieChart,
  Activity
} from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
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
import { MOCK_PROFESSORS } from '@/data/professors'
import { MOCK_COURSES } from '@/data/courses'
import { MOCK_DEPARTMENTS } from '@/data/departments'

interface ReportData {
  id: number
  title: string
  description: string
  type: 'enrollment' | 'faculty' | 'department' | 'schedule' | 'financial'
  lastGenerated: string
  status: 'ready' | 'generating' | 'error'
  size: string
}

const MOCK_REPORTS: ReportData[] = [
  {
    id: 1,
    title: 'Enrollment Report',
    description: 'Comprehensive enrollment statistics and trends',
    type: 'enrollment',
    lastGenerated: '2024-01-15',
    status: 'ready',
    size: '2.3 MB',
  },
  {
    id: 2,
    title: 'Faculty Performance Report',
    description: 'Professor performance metrics and evaluations',
    type: 'faculty',
    lastGenerated: '2024-01-14',
    status: 'ready',
    size: '1.8 MB',
  },
  {
    id: 3,
    title: 'Department Budget Report',
    description: 'Budget allocation and spending analysis',
    type: 'financial',
    lastGenerated: '2024-01-13',
    status: 'ready',
    size: '3.1 MB',
  },
  {
    id: 4,
    title: 'Course Schedule Report',
    description: 'Class scheduling and room utilization',
    type: 'schedule',
    lastGenerated: '2024-01-12',
    status: 'generating',
    size: '1.5 MB',
  },
  {
    id: 5,
    title: 'Department Statistics Report',
    description: 'Department-wise statistics and comparisons',
    type: 'department',
    lastGenerated: '2024-01-11',
    status: 'ready',
    size: '2.7 MB',
  },
]

const StatCard = ({ 
  title, 
  value, 
  icon: Icon, 
  color,
  subtitle 
}: { 
  title: string
  value: number | string
  icon: React.ComponentType<{ size?: number }>
  color: string
  subtitle?: string
}) => {
  const colorClasses = {
    blue: 'bg-blue-100 text-blue-700',
    green: 'bg-green-100 text-green-700',
    yellow: 'bg-yellow-100 text-yellow-700',
    red: 'bg-red-100 text-red-700',
    purple: 'bg-purple-100 text-purple-700',
  }

  return (
    <Card>
      <CardContent className="p-6">
        <div className="flex items-center gap-4">
          <div className={`p-3 rounded-lg ${colorClasses[color as keyof typeof colorClasses]}`}>
            <Icon size={24} />
          </div>
          <div>
            <p className="text-3xl font-semibold">{value}</p>
            <p className="text-muted-foreground">{title}</p>
            {subtitle && <p className="text-xs text-muted-foreground">{subtitle}</p>}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

const getStatusBadge = (status: ReportData['status']) => {
  const variants = {
    'ready': 'default' as const,
    'generating': 'secondary' as const,
    'error': 'destructive' as const,
  }
  
  return <Badge variant={variants[status]}>{status}</Badge>
}

const getTypeIcon = (type: ReportData['type']) => {
  switch (type) {
    case 'enrollment': return Users
    case 'faculty': return BookOpen
    case 'department': return Building2
    case 'schedule': return Calendar
    case 'financial': return TrendingUp
    default: return FileText
  }
}

const getTypeColor = (type: ReportData['type']) => {
  switch (type) {
    case 'enrollment': return 'blue'
    case 'faculty': return 'green'
    case 'department': return 'purple'
    case 'schedule': return 'yellow'
    case 'financial': return 'red'
    default: return 'blue'
  }
}

export function Reports() {
  const [selectedType, setSelectedType] = useState<string>('all')

  // Calculate summary statistics
  const totalProfessors = MOCK_PROFESSORS.length
  const totalCourses = MOCK_COURSES.length
  const totalDepartments = MOCK_DEPARTMENTS.length
  const totalEnrolled = MOCK_COURSES.reduce((sum, course) => sum + course.enrolled, 0)
  const totalCapacity = MOCK_COURSES.reduce((sum, course) => sum + course.capacity, 0)
  const enrollmentRate = Math.round((totalEnrolled / totalCapacity) * 100)

  const filteredReports = selectedType === 'all' 
    ? MOCK_REPORTS 
    : MOCK_REPORTS.filter(report => report.type === selectedType)

  return (
    <div className="w-full space-y-6 p-6">
      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <StatCard
          title="Total Professors"
          value={totalProfessors}
          icon={Users}
          color="blue"
        />
        <StatCard
          title="Total Courses"
          value={totalCourses}
          icon={BookOpen}
          color="green"
        />
        <StatCard
          title="Total Enrolled"
          value={totalEnrolled}
          icon={TrendingUp}
          color="purple"
          subtitle={`${enrollmentRate}% capacity`}
        />
        <StatCard
          title="Departments"
          value={totalDepartments}
          icon={Building2}
          color="yellow"
        />
      </div>

      {/* Quick Reports */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BarChart3 size={20} />
              Enrollment Trends
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-sm text-muted-foreground">This Semester</span>
                <span className="font-medium">{totalEnrolled}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-muted-foreground">Capacity</span>
                <span className="font-medium">{totalCapacity}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-muted-foreground">Utilization</span>
                <Badge variant="outline">{enrollmentRate}%</Badge>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <PieChart size={20} />
              Department Distribution
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {MOCK_DEPARTMENTS.slice(0, 4).map(dept => (
                <div key={dept.id} className="flex justify-between items-center">
                  <span className="text-sm">{dept.name}</span>
                  <span className="text-sm font-medium">{dept.professors} prof.</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Activity size={20} />
              Course Status
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-sm text-muted-foreground">Active Courses</span>
                <span className="font-medium">{MOCK_COURSES.filter(c => c.status === 'Active').length}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-muted-foreground">Inactive Courses</span>
                <span className="font-medium">{MOCK_COURSES.filter(c => c.status === 'Inactive').length}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-muted-foreground">Full Courses</span>
                <span className="font-medium">{MOCK_COURSES.filter(c => c.status === 'Full').length}</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Reports Table */}
      <Card>
        <CardHeader>
          <div className="flex justify-between items-center">
            <CardTitle>Generated Reports</CardTitle>
            <div className="flex gap-2">
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="outline" size="sm">
                    <Filter size={16} className="mr-2" />
                    Filter
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent>
                  <DropdownMenuItem onClick={() => setSelectedType('all')}>
                    All Reports
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => setSelectedType('enrollment')}>
                    Enrollment Reports
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => setSelectedType('faculty')}>
                    Faculty Reports
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => setSelectedType('department')}>
                    Department Reports
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => setSelectedType('schedule')}>
                    Schedule Reports
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => setSelectedType('financial')}>
                    Financial Reports
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
              <Button size="sm">
                <FileText size={16} className="mr-2" />
                Generate Report
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Report</TableHead>
                <TableHead>Type</TableHead>
                <TableHead>Last Generated</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Size</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredReports.map((report) => {
                const TypeIcon = getTypeIcon(report.type)
                const typeColor = getTypeColor(report.type)
                
                return (
                  <TableRow key={report.id}>
                    <TableCell>
                      <div>
                        <p className="font-medium">{report.title}</p>
                        <p className="text-sm text-muted-foreground">{report.description}</p>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <div className={`p-1 rounded ${typeColor === 'blue' ? 'bg-blue-100' : typeColor === 'green' ? 'bg-green-100' : typeColor === 'purple' ? 'bg-purple-100' : typeColor === 'yellow' ? 'bg-yellow-100' : 'bg-red-100'}`}>
                          <TypeIcon size={16} className={typeColor === 'blue' ? 'text-blue-700' : typeColor === 'green' ? 'text-green-700' : typeColor === 'purple' ? 'text-purple-700' : typeColor === 'yellow' ? 'text-yellow-700' : 'text-red-700'} />
                        </div>
                        <span className="text-sm capitalize">{report.type}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <p className="text-sm">{report.lastGenerated}</p>
                    </TableCell>
                    <TableCell>{getStatusBadge(report.status)}</TableCell>
                    <TableCell>
                      <p className="text-sm">{report.size}</p>
                    </TableCell>
                    <TableCell className="text-right">
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
                            <Eye size={16} />
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                          <DropdownMenuItem>
                            <Eye size={16} className="mr-2" />
                            View Report
                          </DropdownMenuItem>
                          <DropdownMenuItem>
                            <Download size={16} className="mr-2" />
                            Download
                          </DropdownMenuItem>
                          <DropdownMenuItem>
                            <FileText size={16} className="mr-2" />
                            Regenerate
                          </DropdownMenuItem>
                        </DropdownMenuContent>
                      </DropdownMenu>
                    </TableCell>
                  </TableRow>
                )
              })}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
} 
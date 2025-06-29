import { useState } from 'react'
import { 
  Calendar, 
  Clock, 
  Users, 
  BookOpen, 
  MapPin, 
  Search, 
  Plus, 
  ArrowUpDown,
  MoreHorizontal,
  Pencil,
  Trash2,
  Eye,
  Grid3X3,
  List
} from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
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
  MOCK_SCHEDULE, 
  getScheduleStats, 
  DAYS,
  type ScheduleItem 
} from '@/data/schedule'

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

const getTypeBadge = (type: ScheduleItem['type']) => {
  const variants = {
    'Lecture': 'default' as const,
    'Lab': 'secondary' as const,
    'Discussion': 'outline' as const,
    'Seminar': 'destructive' as const,
  }
  
  return <Badge variant={variants[type]}>{type}</Badge>
}

const WeeklyCalendar = ({ schedule }: { schedule: ScheduleItem[] }) => {
  const timeSlots = ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00']
  
  const getSessionsForTimeSlot = (day: string, time: string) => {
    return schedule.filter(session => 
      session.day === day && 
      session.startTime === time
    )
  }

  return (
    <div className="overflow-x-auto">
      <div className="min-w-[800px]">
        {/* Header */}
        <div className="grid grid-cols-6 gap-2 mb-2">
          <div className="h-12"></div>
          {DAYS.map(day => (
            <div key={day} className="h-12 flex items-center justify-center bg-muted rounded-lg">
              <span className="font-medium text-sm">{day}</span>
            </div>
          ))}
        </div>
        
        {/* Time slots */}
        {timeSlots.map(time => (
          <div key={time} className="grid grid-cols-6 gap-2 mb-2">
            <div className="h-16 flex items-center justify-end pr-2 text-sm text-muted-foreground">
              {time}
            </div>
            {DAYS.map(day => {
              const sessions = getSessionsForTimeSlot(day, time)
              return (
                <div key={`${day}-${time}`} className="h-16 border rounded-lg p-1">
                  {sessions.map(session => (
                    <div
                      key={session.id}
                      className="bg-blue-100 border border-blue-200 rounded p-1 text-xs h-full overflow-hidden"
                    >
                      <p className="font-medium text-blue-900">{session.courseCode}</p>
                      <p className="text-blue-700 truncate">{session.courseName}</p>
                      <p className="text-blue-600 truncate">{session.room}</p>
                    </div>
                  ))}
                </div>
              )
            })}
          </div>
        ))}
      </div>
    </div>
  )
}

export function Schedule() {
  const [searchTerm, setSearchTerm] = useState('')
  const [viewMode, setViewMode] = useState<'calendar' | 'list'>('calendar')
  const stats = getScheduleStats()

  const filteredSchedule = MOCK_SCHEDULE.filter(session =>
    session.courseName.toLowerCase().includes(searchTerm.toLowerCase()) ||
    session.courseCode.toLowerCase().includes(searchTerm.toLowerCase()) ||
    session.professor.toLowerCase().includes(searchTerm.toLowerCase()) ||
    session.department.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <div className="w-full space-y-6 p-6">
      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <StatCard
          title="Total Sessions"
          value={stats.totalSessions}
          icon={Calendar}
          color="blue"
        />
        <StatCard
          title="Unique Courses"
          value={stats.uniqueCourses}
          icon={BookOpen}
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
          title="Professors"
          value={stats.uniqueProfessors}
          icon={Clock}
          color="yellow"
        />
      </div>

      {/* Search and Actions */}
      <div className="flex flex-col sm:flex-row gap-4 justify-between items-start sm:items-center">
        <div className="relative w-full sm:w-96">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground" size={16} />
          <Input
            placeholder="Search schedule..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
        <div className="flex gap-2">
          <Button
            variant={viewMode === 'calendar' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setViewMode('calendar')}
          >
            <Grid3X3 size={16} className="mr-2" />
            Calendar
          </Button>
          <Button
            variant={viewMode === 'list' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setViewMode('list')}
          >
            <List size={16} className="mr-2" />
            List
          </Button>
          <Button className="w-full sm:w-auto">
            <Plus size={16} className="mr-2" />
            Add Session
          </Button>
        </div>
      </div>

      {/* Schedule View */}
      {viewMode === 'calendar' ? (
        <Card>
          <CardHeader>
            <CardTitle>Weekly Schedule</CardTitle>
          </CardHeader>
          <CardContent>
            <WeeklyCalendar schedule={filteredSchedule} />
          </CardContent>
        </Card>
      ) : (
        <Card>
          <CardHeader>
            <CardTitle>Schedule List</CardTitle>
          </CardHeader>
          <CardContent>
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
                  <TableHead>Professor</TableHead>
                  <TableHead>Day & Time</TableHead>
                  <TableHead>Location</TableHead>
                  <TableHead>Enrollment</TableHead>
                  <TableHead>Type</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredSchedule.map((session) => (
                  <TableRow key={session.id}>
                    <TableCell>
                      <div>
                        <p className="font-medium">{session.courseName}</p>
                        <p className="text-sm text-muted-foreground">{session.courseCode}</p>
                        <p className="text-xs text-muted-foreground">{session.department}</p>
                      </div>
                    </TableCell>
                    <TableCell>
                      <p className="text-sm">{session.professor}</p>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <Calendar size={14} className="text-muted-foreground" />
                        <span className="text-sm">{session.day}</span>
                      </div>
                      <div className="flex items-center gap-2 mt-1">
                        <Clock size={14} className="text-muted-foreground" />
                        <span className="text-sm">{session.startTime} - {session.endTime}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <MapPin size={14} className="text-muted-foreground" />
                        <span className="text-sm">{session.location}, {session.room}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="text-sm">
                        <p>{session.enrolled}/{session.capacity}</p>
                        <div className="w-full bg-gray-200 rounded-full h-2 mt-1">
                          <div 
                            className="bg-blue-600 h-2 rounded-full" 
                            style={{ width: `${(session.enrolled / session.capacity) * 100}%` }}
                          ></div>
                        </div>
                      </div>
                    </TableCell>
                    <TableCell>{getTypeBadge(session.type)}</TableCell>
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
          </CardContent>
        </Card>
      )}
    </div>
  )
} 
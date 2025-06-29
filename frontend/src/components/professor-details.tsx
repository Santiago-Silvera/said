import { useParams, useNavigate } from 'react-router-dom'
import { 
  ChevronLeft, 
  MoreHorizontal, 
  BookOpen, 
  Users, 
  Clock, 
  Award, 
  FileText, 
  Mail, 
  Phone, 
  MapPin, 
  Calendar,
  Star,
  Presentation
} from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { 
  getProfessorById, 
  MOCK_ACTIVITIES,
  type Professor,
  type Course,
  type Activity 
} from '@/data/professors'

const ProfessorHeader = ({ professor }: { professor: Professor }) => {
  const navigate = useNavigate()
  
  return (
    <Card>
      <CardContent className="p-6">
        <Button
          variant="ghost"
          onClick={() => navigate('/professors')}
          className="flex items-center gap-2 text-primary mb-6 hover:text-primary/80 p-0 h-auto"
        >
          <ChevronLeft size={20} />
          <span className="font-medium">Back to Professors</span>
        </Button>
        <div className="flex justify-between">
          <div className="flex gap-6">
            <img
              src={professor.imageUrl}
              alt={professor.name}
              className="w-24 h-24 rounded-lg object-cover"
            />
            <div>
              <h1 className="text-2xl font-bold text-foreground">
                {professor.name}
              </h1>
              <p className="text-muted-foreground">{professor.title}</p>
              <div className="flex items-center gap-2 mt-2">
                <span className="text-sm text-muted-foreground">
                  {professor.department}
                </span>
                <span className="w-1 h-1 bg-muted rounded-full"></span>
                <Badge variant={professor.status === 'Active' ? 'default' : professor.status === 'On Leave' ? 'secondary' : 'destructive'}>
                  {professor.status}
                </Badge>
              </div>
              <div className="flex gap-2 mt-3">
                {professor.expertise?.map((item) => (
                  <Badge key={item} variant="outline" className="text-xs">
                    {item}
                  </Badge>
                ))}
              </div>
            </div>
          </div>
          <Button variant="ghost" size="sm" className="h-fit p-2">
            <MoreHorizontal className="text-muted-foreground" />
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}

const ProfessorStats = ({ professor }: { professor: Professor }) => {
  if (!professor.stats) return null
  
  const stats = [
    { label: 'Students', value: professor.stats.students, icon: Users, color: 'blue' },
    { label: 'Courses', value: professor.stats.courses, icon: BookOpen, color: 'purple' },
    { label: 'Rating', value: professor.stats.rating, icon: Star, color: 'yellow' },
    { label: 'Experience', value: professor.stats.experience, icon: Clock, color: 'green' },
  ]

  const colorClasses = {
    blue: 'bg-blue-100 text-blue-700',
    purple: 'bg-purple-100 text-purple-700',
    yellow: 'bg-yellow-100 text-yellow-700',
    green: 'bg-green-100 text-green-700',
  }

  return (
    <Card>
      <CardContent className="p-4">
        <div className="grid grid-cols-2 gap-4">
          {stats.map((stat) => {
            const Icon = stat.icon
            return (
              <div key={stat.label} className="flex items-center gap-3">
                <div className={`p-2 rounded-lg ${colorClasses[stat.color as keyof typeof colorClasses]}`}>
                  <Icon size={20} />
                </div>
                <div>
                  <p className="text-2xl font-semibold">{stat.value}</p>
                  <p className="text-sm text-muted-foreground">{stat.label}</p>
                </div>
              </div>
            )
          })}
        </div>
      </CardContent>
    </Card>
  )
}

const CourseCard = ({ course }: { course: Course }) => (
  <div className="flex items-center justify-between p-4 border rounded-lg">
    <div className="flex items-center gap-4">
      <div className="p-2 bg-blue-100 rounded-lg">
        <BookOpen className="text-blue-700" size={20} />
      </div>
      <div>
        <h3 className="font-medium">{course.name}</h3>
        <p className="text-sm text-muted-foreground">{course.code}</p>
      </div>
    </div>
    <div className="flex items-center gap-6">
      <div className="flex items-center gap-2">
        <Users size={16} className="text-muted-foreground" />
        <span className="text-sm text-muted-foreground">
          {course.students} Students
        </span>
      </div>
      <div className="flex items-center gap-2">
        <Clock size={16} className="text-muted-foreground" />
        <span className="text-sm text-muted-foreground">
          {course.schedule}
        </span>
      </div>
    </div>
  </div>
)

const ActivityItem = ({ activity }: { activity: Activity }) => {
  const getIcon = (iconName: string) => {
    switch (iconName) {
      case 'FileText': return FileText
      case 'Award': return Award
      case 'Presentation': return Presentation
      default: return FileText
    }
  }

  const Icon = getIcon(activity.icon)
  
  const colorClasses = {
    green: 'bg-green-100 text-green-700',
    purple: 'bg-purple-100 text-purple-700',
    blue: 'bg-blue-100 text-blue-700',
  }

  return (
    <div className="flex gap-4 items-start">
      <div className={`p-2 rounded-lg ${colorClasses[activity.color as keyof typeof colorClasses]}`}>
        <Icon size={20} />
      </div>
      <div>
        <p className="font-medium">{activity.title}</p>
        <p className="text-sm text-muted-foreground">
          {activity.description}
        </p>
        <p className="text-xs text-muted-foreground mt-1">{activity.date}</p>
      </div>
    </div>
  )
}

export function ProfessorDetails() {
  const { id } = useParams<{ id: string }>()
  const professor = getProfessorById(Number(id))

  if (!professor) {
    return (
      <div className="p-6">Professor not found</div>
    )
  }

  return (
    <div className="w-full space-y-6 p-6">
      <ProfessorHeader professor={professor} />
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          {/* Current Courses */}
          <Card>
            <CardHeader>
              <CardTitle>Current Courses</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {professor.currentCourses && professor.currentCourses.length > 0 ? (
                  professor.currentCourses.map((course) => (
                    <CourseCard key={course.code} course={course} />
                  ))
                ) : (
                  <p className="text-muted-foreground text-center py-8">
                    No current courses assigned
                  </p>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Recent Activity */}
          <Card>
            <CardHeader>
              <CardTitle>Recent Activity</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {MOCK_ACTIVITIES.map((activity, index) => (
                  <ActivityItem key={index} activity={activity} />
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="space-y-6">
          {/* Professor Stats */}
          <ProfessorStats professor={professor} />

          {/* Contact Information */}
          <Card>
            <CardHeader>
              <CardTitle>Contact Information</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <Mail className="text-muted-foreground" size={20} />
                  <span className="text-muted-foreground">{professor.email}</span>
                </div>
                <div className="flex items-center gap-3">
                  <Phone className="text-muted-foreground" size={20} />
                  <span className="text-muted-foreground">{professor.phone}</span>
                </div>
                {professor.office && (
                  <div className="flex items-center gap-3">
                    <MapPin className="text-muted-foreground" size={20} />
                    <span className="text-muted-foreground">{professor.office}</span>
                  </div>
                )}
                {professor.joinDate && (
                  <div className="flex items-center gap-3">
                    <Calendar className="text-muted-foreground" size={20} />
                    <span className="text-muted-foreground">
                      Joined {professor.joinDate}
                    </span>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
} 
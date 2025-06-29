import { Users, BookOpen, Presentation } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { 
  MOCK_PROFESSORS, 
  MOCK_COURSES, 
  getDashboardStats, 
  STATS_CONFIG,
  type Professor,
  type Course 
} from '@/data/dashboard'
import { StatCard, PageLayout, StatsGrid } from '@/components/shared'

export function Dashboard() {
  const stats = getDashboardStats()
  const recentProfessors = MOCK_PROFESSORS.slice(0, 5)

  return (
    <PageLayout>
      {/* Stats Overview */}
      <StatsGrid columns={3}>
        <StatCard
          title={STATS_CONFIG.professors.title}
          value={stats.professors}
          icon={Users}
          color={STATS_CONFIG.professors.color}
        />
        <StatCard
          title={STATS_CONFIG.courses.title}
          value={stats.courses}
          icon={BookOpen}
          color={STATS_CONFIG.courses.color}
        />
        <StatCard
          title={STATS_CONFIG.assignedPercentage.title}
          value={stats.assignedPercentage}
          icon={Presentation}
          color={STATS_CONFIG.assignedPercentage.color}
        />
      </StatsGrid>

      {/* Recent Professors */}
      <Card>
        <CardHeader>
          <CardTitle>Recent Professors</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3 sm:space-y-4">
            {recentProfessors.map((professor, index) => (
              <div key={index} className="flex items-center gap-3 sm:gap-4 p-3 sm:p-4 border rounded-lg min-w-0">
                <img
                  src={professor.imageUrl}
                  alt={professor.name}
                  className="w-10 h-10 sm:w-12 sm:h-12 rounded-full object-cover flex-shrink-0"
                />
                <div className="flex-1 min-w-0">
                  <h3 className="font-medium truncate">{professor.name}</h3>
                  <p className="text-sm text-muted-foreground truncate">{professor.department}</p>
                  <div className="flex gap-1 sm:gap-2 mt-1 flex-wrap">
                    {professor.courses.map((course, courseIndex) => (
                      <Badge key={courseIndex} variant="outline" className="text-xs">
                        {course}
                      </Badge>
                    ))}
                  </div>
                </div>
                <Button variant="outline" size="sm" className="flex-shrink-0">
                  View Details
                </Button>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Course Overview */}
      <Card>
        <CardHeader>
          <CardTitle>Course Overview</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3 sm:space-y-4">
            {MOCK_COURSES.map((course, index) => (
              <div key={index} className="flex items-center justify-between p-3 sm:p-4 border rounded-lg min-w-0">
                <div className="flex-1 min-w-0">
                  <h3 className="font-medium truncate">{course.name}</h3>
                  <p className="text-sm text-muted-foreground truncate">{course.code}</p>
                </div>
                <div className="flex items-center gap-2 sm:gap-4 flex-shrink-0">
                  <div className="text-right">
                    <p className="text-sm font-medium">{course.enrolled} enrolled</p>
                    <p className="text-xs text-muted-foreground">Students</p>
                  </div>
                  <Badge variant={course.assigned ? "default" : "secondary"}>
                    {course.assigned ? "Assigned" : "Unassigned"}
                  </Badge>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </PageLayout>
  )
} 
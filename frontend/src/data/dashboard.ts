import type { StatCardColor } from '@/components/shared'

export interface Professor {
  name: string
  department: string
  imageUrl: string
  courses: string[]
}

export interface Course {
  name: string
  code: string
  enrolled: number
  assigned: boolean
}

export interface DashboardStats {
  professors: number
  courses: number
  assignedPercentage: number
}

export const MOCK_PROFESSORS: Professor[] = [
  {
    name: 'Dr. Maria Rodriguez',
    department: 'Computer Science',
    imageUrl:
      'https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&auto=format&fit=crop&w=256&h=256&q=80',
    courses: ['Data Structures', 'Algorithms'],
  },
  {
    name: 'Prof. James Wilson',
    department: 'Engineering',
    imageUrl:
      'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?ixlib=rb-1.2.1&auto=format&fit=crop&w=256&h=256&q=80',
    courses: ['Circuit Design', 'Digital Electronics'],
  },
  {
    name: 'Dr. Sarah Johnson',
    department: 'Mathematics',
    imageUrl:
      'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-1.2.1&auto=format&fit=crop&w=256&h=256&q=80',
    courses: ['Calculus I', 'Linear Algebra'],
  },
]

export const MOCK_COURSES: Course[] = [
  {
    name: 'Data Structures',
    code: 'CS301',
    enrolled: 45,
    assigned: true,
  },
  {
    name: 'Circuit Design',
    code: 'EE201',
    enrolled: 38,
    assigned: true,
  },
  {
    name: 'Quantum Physics',
    code: 'PHY401',
    enrolled: 25,
    assigned: false,
  },
  {
    name: 'Linear Algebra',
    code: 'MAT202',
    enrolled: 52,
    assigned: true,
  },
]

export const getDashboardStats = (): DashboardStats => {
  const assignedPercentage = (MOCK_COURSES.filter((c) => c.assigned).length / MOCK_COURSES.length) * 100
  return {
    professors: MOCK_PROFESSORS.length,
    courses: MOCK_COURSES.length,
    assignedPercentage: Math.round(assignedPercentage),
  }
}

export const STATS_CONFIG = {
  professors: {
    title: 'Active Professors',
    icon: 'Users',
    color: 'blue' as StatCardColor,
  },
  courses: {
    title: 'Total Courses',
    icon: 'BookOpen',
    color: 'purple' as StatCardColor,
  },
  assignedPercentage: {
    title: 'Courses Assigned',
    icon: 'Presentation',
    color: 'green' as StatCardColor,
  },
} 
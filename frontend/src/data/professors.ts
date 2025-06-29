export interface Professor {
  id: number
  name: string
  department: string
  email: string
  phone: string
  status: 'Active' | 'On Leave' | 'Inactive'
  courses: string[]
  imageUrl: string
  // Additional fields for details page
  title?: string
  office?: string
  joinDate?: string
  expertise?: string[]
  currentCourses?: Course[]
  stats?: ProfessorStats
}

export interface Course {
  code: string
  name: string
  students: number
  schedule: string
}

export interface ProfessorStats {
  students: number
  courses: number
  rating: number
  experience: string
}

export interface Activity {
  type: 'publication' | 'award' | 'conference' | 'other'
  title: string
  description: string
  date: string
  icon: string
  color: string
}

export const MOCK_PROFESSORS: Professor[] = [
  {
    id: 1,
    name: 'Dr. Maria Rodriguez',
    department: 'Computer Science',
    email: 'm.rodriguez@university.edu',
    phone: '+1 (555) 123-4567',
    status: 'Active',
    courses: ['Data Structures', 'Algorithms'],
    imageUrl:
      'https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&auto=format&fit=crop&w=256&h=256&q=80',
    title: 'Associate Professor',
    office: 'Science Building, Room 405',
    joinDate: '2018',
    expertise: ['Machine Learning', 'Data Science', 'Algorithm Design'],
    currentCourses: [
      {
        code: 'CS401',
        name: 'Advanced Algorithms',
        students: 45,
        schedule: 'Mon/Wed 10:00-11:30',
      },
      {
        code: 'CS550',
        name: 'Machine Learning',
        students: 38,
        schedule: 'Tue/Thu 14:00-15:30',
      },
    ],
    stats: {
      students: 83,
      courses: 2,
      rating: 4.8,
      experience: '5y',
    },
  },
  {
    id: 2,
    name: 'Prof. James Wilson',
    department: 'Engineering',
    email: 'j.wilson@university.edu',
    phone: '+1 (555) 234-5678',
    status: 'On Leave',
    courses: ['Circuit Design', 'Digital Electronics'],
    imageUrl:
      'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?ixlib=rb-1.2.1&auto=format&fit=crop&w=256&h=256&q=80',
    title: 'Assistant Professor',
    office: 'Engineering Building, Room 302',
    joinDate: '2020',
    expertise: ['Digital Electronics', 'Circuit Design', 'VLSI'],
    currentCourses: [
      {
        code: 'EE201',
        name: 'Circuit Design',
        students: 42,
        schedule: 'Mon/Wed 14:00-15:30',
      },
    ],
    stats: {
      students: 42,
      courses: 1,
      rating: 4.6,
      experience: '3y',
    },
  },
  {
    id: 3,
    name: 'Dr. Sarah Johnson',
    department: 'Mathematics',
    email: 's.johnson@university.edu',
    phone: '+1 (555) 345-6789',
    status: 'Active',
    courses: ['Calculus I', 'Linear Algebra'],
    imageUrl:
      'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-1.2.1&auto=format&fit=crop&w=256&h=256&q=80',
    title: 'Professor',
    office: 'Math Building, Room 201',
    joinDate: '2015',
    expertise: ['Linear Algebra', 'Calculus', 'Mathematical Analysis'],
    currentCourses: [
      {
        code: 'MAT101',
        name: 'Calculus I',
        students: 65,
        schedule: 'Mon/Wed/Fri 09:00-10:30',
      },
      {
        code: 'MAT202',
        name: 'Linear Algebra',
        students: 48,
        schedule: 'Tue/Thu 11:00-12:30',
      },
    ],
    stats: {
      students: 113,
      courses: 2,
      rating: 4.9,
      experience: '8y',
    },
  },
  {
    id: 4,
    name: 'Prof. Michael Chang',
    department: 'Physics',
    email: 'm.chang@university.edu',
    phone: '+1 (555) 456-7890',
    status: 'Active',
    courses: ['Quantum Mechanics', 'Thermodynamics'],
    imageUrl:
      'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&auto=format&fit=crop&w=256&h=256&q=80',
    title: 'Associate Professor',
    office: 'Physics Building, Room 105',
    joinDate: '2019',
    expertise: ['Quantum Physics', 'Thermodynamics', 'Statistical Mechanics'],
    currentCourses: [
      {
        code: 'PHY301',
        name: 'Quantum Mechanics',
        students: 32,
        schedule: 'Mon/Wed 15:00-16:30',
      },
      {
        code: 'PHY302',
        name: 'Thermodynamics',
        students: 28,
        schedule: 'Tue/Thu 13:00-14:30',
      },
    ],
    stats: {
      students: 60,
      courses: 2,
      rating: 4.7,
      experience: '4y',
    },
  },
  {
    id: 5,
    name: 'Dr. Emily Chen',
    department: 'Biology',
    email: 'e.chen@university.edu',
    phone: '+1 (555) 567-8901',
    status: 'Active',
    courses: ['Cell Biology', 'Genetics'],
    imageUrl:
      'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-1.2.1&auto=format&fit=crop&w=256&h=256&q=80',
    title: 'Assistant Professor',
    office: 'Biology Building, Room 308',
    joinDate: '2021',
    expertise: ['Cell Biology', 'Genetics', 'Molecular Biology'],
    currentCourses: [
      {
        code: 'BIO201',
        name: 'Cell Biology',
        students: 55,
        schedule: 'Mon/Wed 11:00-12:30',
      },
      {
        code: 'BIO202',
        name: 'Genetics',
        students: 47,
        schedule: 'Tue/Thu 09:00-10:30',
      },
    ],
    stats: {
      students: 102,
      courses: 2,
      rating: 4.5,
      experience: '2y',
    },
  },
  {
    id: 6,
    name: 'Prof. David Thompson',
    department: 'Chemistry',
    email: 'd.thompson@university.edu',
    phone: '+1 (555) 678-9012',
    status: 'Inactive',
    courses: ['Organic Chemistry', 'Biochemistry'],
    imageUrl:
      'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?ixlib=rb-1.2.1&auto=format&fit=crop&w=256&h=256&q=80',
    title: 'Professor',
    office: 'Chemistry Building, Room 401',
    joinDate: '2010',
    expertise: ['Organic Chemistry', 'Biochemistry', 'Analytical Chemistry'],
    currentCourses: [],
    stats: {
      students: 0,
      courses: 0,
      rating: 4.3,
      experience: '13y',
    },
  },
]

export const MOCK_ACTIVITIES: Activity[] = [
  {
    type: 'publication',
    title: 'Published research paper',
    description: 'Published "Machine Learning Applications in Modern Computing"',
    date: '2 days ago',
    icon: 'FileText',
    color: 'green',
  },
  {
    type: 'award',
    title: 'Received Award',
    description: 'Excellence in Teaching Award 2023',
    date: '1 week ago',
    icon: 'Award',
    color: 'purple',
  },
  {
    type: 'conference',
    title: 'Conference Presentation',
    description: 'Presented at International Computer Science Conference',
    date: '2 weeks ago',
    icon: 'Presentation',
    color: 'blue',
  },
]

export const getProfessorStats = () => {
  const total = MOCK_PROFESSORS.length
  const active = MOCK_PROFESSORS.filter(p => p.status === 'Active').length
  const onLeave = MOCK_PROFESSORS.filter(p => p.status === 'On Leave').length
  const inactive = MOCK_PROFESSORS.filter(p => p.status === 'Inactive').length

  return {
    total,
    active,
    onLeave,
    inactive,
    activePercentage: Math.round((active / total) * 100)
  }
}

export const getProfessorById = (id: number): Professor | undefined => {
  return MOCK_PROFESSORS.find(professor => professor.id === id)
}

export const DEPARTMENTS = [
  'Computer Science',
  'Engineering', 
  'Mathematics',
  'Physics',
  'Biology',
  'Chemistry'
]

export const STATUS_OPTIONS = ['Active', 'On Leave', 'Inactive'] as const 
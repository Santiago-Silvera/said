export interface Course {
  id: number
  code: string
  name: string
  department: string
  credits: number
  enrolled: number
  capacity: number
  status: 'Active' | 'Inactive' | 'Full'
  professor?: string
  schedule: string
  location: string
  description: string
  prerequisites: string[]
  semester: 'Fall' | 'Spring'
  year: number
}

export const MOCK_COURSES: Course[] = [
  {
    id: 1,
    code: 'CS401',
    name: 'Advanced Algorithms',
    department: 'Computer Science',
    credits: 3,
    enrolled: 45,
    capacity: 50,
    status: 'Active',
    professor: 'Dr. Maria Rodriguez',
    schedule: 'Mon/Wed 10:00-11:30',
    location: 'Science Building, Room 405',
    description: 'Advanced study of algorithm design and analysis techniques.',
    prerequisites: ['CS301', 'MATH202'],
    semester: 'Fall',
    year: 2024,
  },
  {
    id: 2,
    code: 'CS550',
    name: 'Machine Learning',
    department: 'Computer Science',
    credits: 4,
    enrolled: 38,
    capacity: 40,
    status: 'Active',
    professor: 'Dr. Maria Rodriguez',
    schedule: 'Tue/Thu 14:00-15:30',
    location: 'Science Building, Room 405',
    description: 'Introduction to machine learning algorithms and applications.',
    prerequisites: ['CS401', 'STAT301'],
    semester: 'Fall',
    year: 2024,
  },
  {
    id: 3,
    code: 'EE201',
    name: 'Circuit Design',
    department: 'Engineering',
    credits: 3,
    enrolled: 42,
    capacity: 45,
    status: 'Active',
    professor: 'Prof. James Wilson',
    schedule: 'Mon/Wed 14:00-15:30',
    location: 'Engineering Building, Room 302',
    description: 'Fundamentals of electronic circuit design and analysis.',
    prerequisites: ['PHY101', 'MATH101'],
    semester: 'Fall',
    year: 2024,
  },
  {
    id: 4,
    code: 'MAT101',
    name: 'Calculus I',
    department: 'Mathematics',
    credits: 4,
    enrolled: 65,
    capacity: 70,
    status: 'Active',
    professor: 'Dr. Sarah Johnson',
    schedule: 'Mon/Wed/Fri 09:00-10:30',
    location: 'Math Building, Room 201',
    description: 'Introduction to differential calculus and its applications.',
    prerequisites: [],
    semester: 'Fall',
    year: 2024,
  },
  {
    id: 5,
    code: 'MAT202',
    name: 'Linear Algebra',
    department: 'Mathematics',
    credits: 3,
    enrolled: 48,
    capacity: 50,
    status: 'Active',
    professor: 'Dr. Sarah Johnson',
    schedule: 'Tue/Thu 11:00-12:30',
    location: 'Math Building, Room 201',
    description: 'Study of linear equations, matrices, and vector spaces.',
    prerequisites: ['MAT101'],
    semester: 'Fall',
    year: 2024,
  },
  {
    id: 6,
    code: 'PHY301',
    name: 'Quantum Mechanics',
    department: 'Physics',
    credits: 4,
    enrolled: 32,
    capacity: 35,
    status: 'Active',
    professor: 'Prof. Michael Chang',
    schedule: 'Mon/Wed 15:00-16:30',
    location: 'Physics Building, Room 105',
    description: 'Introduction to quantum mechanics and its mathematical foundations.',
    prerequisites: ['PHY201', 'MATH202'],
    semester: 'Fall',
    year: 2024,
  },
  {
    id: 7,
    code: 'BIO201',
    name: 'Cell Biology',
    department: 'Biology',
    credits: 3,
    enrolled: 55,
    capacity: 60,
    status: 'Active',
    professor: 'Dr. Emily Chen',
    schedule: 'Mon/Wed 11:00-12:30',
    location: 'Biology Building, Room 308',
    description: 'Study of cell structure, function, and cellular processes.',
    prerequisites: ['BIO101'],
    semester: 'Fall',
    year: 2024,
  },
  {
    id: 8,
    code: 'CHEM301',
    name: 'Organic Chemistry',
    department: 'Chemistry',
    credits: 4,
    enrolled: 0,
    capacity: 40,
    status: 'Inactive',
    professor: 'Prof. David Thompson',
    schedule: 'Tue/Thu 13:00-14:30',
    location: 'Chemistry Building, Room 401',
    description: 'Study of organic compounds and their reactions.',
    prerequisites: ['CHEM201'],
    semester: 'Fall',
    year: 2024,
  },
]

export const getCourseStats = () => {
  const total = MOCK_COURSES.length
  const active = MOCK_COURSES.filter(c => c.status === 'Active').length
  const inactive = MOCK_COURSES.filter(c => c.status === 'Inactive').length
  const full = MOCK_COURSES.filter(c => c.status === 'Full').length
  const totalEnrolled = MOCK_COURSES.reduce((sum, course) => sum + course.enrolled, 0)
  const totalCapacity = MOCK_COURSES.reduce((sum, course) => sum + course.capacity, 0)
  const enrollmentRate = Math.round((totalEnrolled / totalCapacity) * 100)

  return {
    total,
    active,
    inactive,
    full,
    totalEnrolled,
    totalCapacity,
    enrollmentRate,
  }
}

export const DEPARTMENTS = [
  'Computer Science',
  'Engineering',
  'Mathematics',
  'Physics',
  'Biology',
  'Chemistry'
]

export const SEMESTERS = ['Fall', 'Spring'] as const
export const STATUS_OPTIONS = ['Active', 'Inactive', 'Full'] as const 
export interface Department {
  id: number
  name: string
  code: string
  chair: string
  email: string
  phone: string
  location: string
  status: 'Active' | 'Inactive'
  professors: number
  courses: number
  students: number
  budget: number
  description: string
  established: string
}

export const MOCK_DEPARTMENTS: Department[] = [
  {
    id: 1,
    name: 'Computer Science',
    code: 'CS',
    chair: 'Dr. Maria Rodriguez',
    email: 'cs@university.edu',
    phone: '+1 (555) 123-4000',
    location: 'Science Building, Floor 4',
    status: 'Active',
    professors: 12,
    courses: 25,
    students: 450,
    budget: 2500000,
    description: 'Department focused on computer science, software engineering, and artificial intelligence.',
    established: '1985',
  },
  {
    id: 2,
    name: 'Engineering',
    code: 'ENG',
    chair: 'Prof. James Wilson',
    email: 'engineering@university.edu',
    phone: '+1 (555) 123-5000',
    location: 'Engineering Building, Floor 2',
    status: 'Active',
    professors: 15,
    courses: 30,
    students: 380,
    budget: 3200000,
    description: 'Comprehensive engineering department covering electrical, mechanical, and civil engineering.',
    established: '1970',
  },
  {
    id: 3,
    name: 'Mathematics',
    code: 'MATH',
    chair: 'Dr. Sarah Johnson',
    email: 'math@university.edu',
    phone: '+1 (555) 123-6000',
    location: 'Math Building, Floor 2',
    status: 'Active',
    professors: 8,
    courses: 20,
    students: 280,
    budget: 1800000,
    description: 'Department specializing in pure and applied mathematics, statistics, and mathematical modeling.',
    established: '1965',
  },
  {
    id: 4,
    name: 'Physics',
    code: 'PHY',
    chair: 'Prof. Michael Chang',
    email: 'physics@university.edu',
    phone: '+1 (555) 123-7000',
    location: 'Physics Building, Floor 1',
    status: 'Active',
    professors: 10,
    courses: 18,
    students: 220,
    budget: 2100000,
    description: 'Department focused on theoretical and experimental physics, including quantum mechanics and astrophysics.',
    established: '1975',
  },
  {
    id: 5,
    name: 'Biology',
    code: 'BIO',
    chair: 'Dr. Emily Chen',
    email: 'biology@university.edu',
    phone: '+1 (555) 123-8000',
    location: 'Biology Building, Floor 3',
    status: 'Active',
    professors: 14,
    courses: 22,
    students: 320,
    budget: 2800000,
    description: 'Department covering molecular biology, genetics, ecology, and environmental science.',
    established: '1980',
  },
  {
    id: 6,
    name: 'Chemistry',
    code: 'CHEM',
    chair: 'Prof. David Thompson',
    email: 'chemistry@university.edu',
    phone: '+1 (555) 123-9000',
    location: 'Chemistry Building, Floor 4',
    status: 'Inactive',
    professors: 6,
    courses: 12,
    students: 150,
    budget: 1200000,
    description: 'Department specializing in organic, inorganic, and analytical chemistry.',
    established: '1972',
  },
]

export const getDepartmentStats = () => {
  const total = MOCK_DEPARTMENTS.length
  const active = MOCK_DEPARTMENTS.filter(d => d.status === 'Active').length
  const inactive = MOCK_DEPARTMENTS.filter(d => d.status === 'Inactive').length
  const totalProfessors = MOCK_DEPARTMENTS.reduce((sum, dept) => sum + dept.professors, 0)
  const totalCourses = MOCK_DEPARTMENTS.reduce((sum, dept) => sum + dept.courses, 0)
  const totalStudents = MOCK_DEPARTMENTS.reduce((sum, dept) => sum + dept.students, 0)
  const totalBudget = MOCK_DEPARTMENTS.reduce((sum, dept) => sum + dept.budget, 0)

  return {
    total,
    active,
    inactive,
    totalProfessors,
    totalCourses,
    totalStudents,
    totalBudget,
  }
}

export const STATUS_OPTIONS = ['Active', 'Inactive'] as const 
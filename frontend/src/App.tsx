import './App.css'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from '@/app/layout'
import { Dashboard } from '@/components/dashboard'
import { Professors } from '@/components/professors'
import { ProfessorDetails } from '@/components/professor-details'
import { Courses } from '@/components/courses'
import { Departments } from '@/components/departments'
import { Schedule } from '@/components/schedule'
import { Reports } from '@/components/reports'
import { Settings } from '@/components/settings'

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/professors" element={<Professors />} />
          <Route path="/professors/:id" element={<ProfessorDetails />} />
          <Route path="/courses" element={<Courses />} />
          <Route path="/departments" element={<Departments />} />
          <Route path="/schedule" element={<Schedule />} />
          <Route path="/reports" element={<Reports />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App

import { 
  Users, 
  BookOpen, 
  Calendar, 
  Settings, 
  BarChart3, 
  GraduationCap, 
  Building2,
  LayoutDashboard 
} from "lucide-react"
import { useLocation } from "react-router-dom"
import { Link } from "react-router-dom"
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarFooter,
} from "@/components/ui/sidebar"

export function AppSidebar() {
  const location = useLocation()

  const navItems = [
    { icon: <LayoutDashboard size={20} />, label: "Dashboard", url: "/" },
    { icon: <Users size={20} />, label: "Professors", url: "/professors" },
    { icon: <BookOpen size={20} />, label: "Courses", url: "/courses" },
    { icon: <Building2 size={20} />, label: "Departments", url: "/departments" },
    { icon: <Calendar size={20} />, label: "Schedule", url: "/schedule" },
    { icon: <BarChart3 size={20} />, label: "Reports", url: "/reports" },
    { icon: <Settings size={20} />, label: "Settings", url: "/settings" },
  ]

  return (
    <Sidebar className="bg-[var(--main)] text-white border-r border-[var(--secondary)]">
      <SidebarHeader className="p-5 border-b border-[var(--secondary)]">
        <div className="flex items-center gap-2">
          <GraduationCap size={24} />
          <h1 className="text-xl font-bold">Admin Panel</h1>
        </div>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel className="sr-only">Navigation</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {navItems.map((item) => {
                const isActive = location.pathname === item.url
                return (
                  <SidebarMenuItem key={item.label}>
                    <SidebarMenuButton 
                      asChild 
                      isActive={isActive}
                      className="w-full justify-start gap-3 px-5 py-3 hover:bg-[var(--secondary)] data-[active=true]:bg-[var(--secondary)] data-[active=true]:border-l-4 data-[active=true]:border-[var(--accent)]"
                    >
                      <Link to={item.url}>
                        <span className="text-[var(--accent)]">{item.icon}</span>
                        <span className={isActive ? 'font-medium' : ''}>{item.label}</span>
                      </Link>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                )
              })}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter className="p-4 border-t border-[var(--secondary)]">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-[var(--secondary)] flex items-center justify-center">
            <span className="font-medium">AU</span>
          </div>
          <div>
            <p className="text-sm font-medium">Admin User</p>
            <p className="text-xs text-[var(--accent)]">admin@university.edu</p>
          </div>
        </div>
      </SidebarFooter>
    </Sidebar>
  )
}

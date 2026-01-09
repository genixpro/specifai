import { Briefcase, Folder, Home, Users } from "lucide-react"

import { SidebarAppearance } from "@/elements/Common/Appearance"
import { Logo } from "@/elements/Common/Logo"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
} from "@/elements/ui/sidebar"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/elements/ui/select"
import useAuth from "@auth/hooks/useAuth"
import { type Item, Main } from "./Main"
import { User } from "./User"
import { useWorkspaces } from "@workspaces/hooks/useWorkspaces"

const baseItems: Item[] = [
  { icon: Home, title: "Dashboard", path: "/" },
  { icon: Folder, title: "Workspaces", path: "/workspaces" },
  { icon: Briefcase, title: "Items", path: "/items" },
]

export function AppSidebar() {
  const { user: currentUser } = useAuth()
  const { workspaces, activeWorkspaceId, setActiveWorkspaceId } = useWorkspaces()

  const items = currentUser?.is_superuser
    ? [...baseItems, { icon: Users, title: "Admin", path: "/admin" }]
    : baseItems

  return (
    <Sidebar collapsible="icon">
      <SidebarHeader className="px-4 py-6 group-data-[collapsible=icon]:px-0 group-data-[collapsible=icon]:items-center">
        <Logo variant="responsive" />
      </SidebarHeader>
      <SidebarContent>
        <div className="px-4 pb-4 group-data-[collapsible=icon]:hidden">
          <p className="text-xs font-medium text-muted-foreground mb-2">
            Workspace
          </p>
          <Select
            value={activeWorkspaceId ?? ""}
            onValueChange={setActiveWorkspaceId}
          >
            <SelectTrigger className="h-9">
              <SelectValue placeholder="Select workspace" />
            </SelectTrigger>
            <SelectContent>
              {workspaces.map((workspace) => (
                <SelectItem key={workspace.id} value={workspace.id}>
                  {workspace.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
        <Main items={items} />
      </SidebarContent>
      <SidebarFooter>
        <SidebarAppearance />
        <User user={currentUser} />
      </SidebarFooter>
    </Sidebar>
  )
}

export default AppSidebar

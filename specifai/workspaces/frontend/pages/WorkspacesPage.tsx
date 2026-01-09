import { Check, Folder } from "lucide-react"

import AddWorkspace from "@workspaces/elements/AddWorkspace"
import { useWorkspaces } from "@workspaces/hooks/useWorkspaces"
import { Card, CardContent, CardHeader, CardTitle } from "@/elements/ui/card"
import { cn } from "@/utils/classnames"

export default function WorkspacesPage() {
  const { workspaces, activeWorkspaceId, setActiveWorkspaceId } =
    useWorkspaces()

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Workspaces</h1>
          <p className="text-muted-foreground">
            Organize everything by workspace.
          </p>
        </div>
        <AddWorkspace />
      </div>

      {workspaces.length === 0 ? (
        <div className="flex flex-col items-center justify-center text-center py-12">
          <div className="rounded-full bg-muted p-4 mb-4">
            <Folder className="h-8 w-8 text-muted-foreground" />
          </div>
          <h3 className="text-lg font-semibold">No workspaces yet</h3>
          <p className="text-muted-foreground">
            Create your first workspace to get started.
          </p>
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {workspaces.map((workspace) => {
            const isActive = workspace.id === activeWorkspaceId
            return (
              <Card
                key={workspace.id}
                className={cn(
                  "cursor-pointer transition hover:border-primary/60",
                  isActive && "border-primary",
                )}
                onClick={() => setActiveWorkspaceId(workspace.id)}
              >
                <CardHeader className="flex-row items-center justify-between">
                  <CardTitle className="flex items-center gap-2 text-base">
                    <Folder className="h-4 w-4 text-muted-foreground" />
                    {workspace.name}
                  </CardTitle>
                  {isActive ? (
                    <span className="inline-flex items-center gap-1 text-xs font-medium text-primary">
                      <Check className="h-3 w-3" />
                      Active
                    </span>
                  ) : null}
                </CardHeader>
                <CardContent>
                  <p className="text-xs text-muted-foreground font-mono">
                    {workspace.id}
                  </p>
                </CardContent>
              </Card>
            )
          })}
        </div>
      )}
    </div>
  )
}

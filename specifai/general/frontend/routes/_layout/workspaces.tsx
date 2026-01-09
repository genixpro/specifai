import { createFileRoute } from "@tanstack/react-router"

import WorkspacesPage from "@workspaces/pages/WorkspacesPage"

export const Route = createFileRoute("/_layout/workspaces")({
  component: WorkspacesPage,
  head: () => ({
    meta: [
      {
        title: "Workspaces - FastAPI Cloud",
      },
    ],
  }),
})

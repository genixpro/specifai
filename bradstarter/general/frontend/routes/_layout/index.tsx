import { createFileRoute } from "@tanstack/react-router"

import DashboardPage from "@/pages/DashboardPage"

export const Route = createFileRoute("/_layout/")({
  component: DashboardPage,
  head: () => ({
    meta: [
      {
        title: "Dashboard - FastAPI Cloud",
      },
    ],
  }),
})

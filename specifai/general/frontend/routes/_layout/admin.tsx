import { createFileRoute } from "@tanstack/react-router"

import AdminPage from "@admin/pages/AdminPage"

export const Route = createFileRoute("/_layout/admin")({
  component: AdminPage,
  head: () => ({
    meta: [
      {
        title: "Admin - FastAPI Cloud",
      },
    ],
  }),
})

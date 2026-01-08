import { createFileRoute } from "@tanstack/react-router"

import UserSettingsPage from "@users/pages/UserSettingsPage"

export const Route = createFileRoute("/_layout/settings")({
  component: UserSettingsPage,
  head: () => ({
    meta: [
      {
        title: "Settings - FastAPI Cloud",
      },
    ],
  }),
})

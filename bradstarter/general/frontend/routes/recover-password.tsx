import { createFileRoute, redirect } from "@tanstack/react-router"

import { isLoggedIn } from "@auth/hooks/useAuth"
import RecoverPasswordPage from "@auth/pages/RecoverPasswordPage"

export const Route = createFileRoute("/recover-password")({
  component: RecoverPasswordPage,
  beforeLoad: async () => {
    if (isLoggedIn()) {
      throw redirect({
        to: "/",
      })
    }
  },
  head: () => ({
    meta: [
      {
        title: "Recover Password - FastAPI Cloud",
      },
    ],
  }),
})

import { createFileRoute, redirect } from "@tanstack/react-router"
import { z } from "zod"

import { isLoggedIn } from "@auth/hooks/useAuth"
import ResetPasswordPage from "@auth/pages/ResetPasswordPage"

const searchSchema = z.object({
  token: z.string().catch(""),
})

export const Route = createFileRoute("/reset-password")({
  component: ResetPasswordRoute,
  validateSearch: searchSchema,
  beforeLoad: async ({ search }) => {
    if (isLoggedIn()) {
      throw redirect({ to: "/" })
    }
    if (!search.token) {
      throw redirect({ to: "/login" })
    }
  },
  head: () => ({
    meta: [
      {
        title: "Reset Password - FastAPI Cloud",
      },
    ],
  }),
})

function ResetPasswordRoute() {
  const { token } = Route.useSearch()
  return <ResetPasswordPage token={token} />
}

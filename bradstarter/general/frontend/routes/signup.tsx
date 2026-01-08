import { createFileRoute, redirect } from "@tanstack/react-router"

import { isLoggedIn } from "@auth/hooks/useAuth"
import SignupPage from "@auth/pages/SignupPage"

export const Route = createFileRoute("/signup")({
  component: SignupPage,
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
        title: "Sign Up - FastAPI Cloud",
      },
    ],
  }),
})

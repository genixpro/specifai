import { createFileRoute, redirect } from "@tanstack/react-router"

import LayoutShell from "@/pages/LayoutShell"
import { isLoggedIn } from "@auth/hooks/useAuth"

export const Route = createFileRoute("/_layout")({
  component: LayoutShell,
  beforeLoad: async () => {
    if (!isLoggedIn()) {
      throw redirect({
        to: "/login",
      })
    }
  },
})

export default LayoutShell

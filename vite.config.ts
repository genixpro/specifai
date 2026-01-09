import path from "node:path"
import tailwindcss from "@tailwindcss/vite"
import { tanstackRouter } from "@tanstack/router-plugin/vite"
import react from "@vitejs/plugin-react-swc"
import { defineConfig } from "vite"

// https://vitejs.dev/config/
export default defineConfig({
  publicDir: "specifai/general/frontend/public",
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "specifai", "general", "frontend"),
      "@auth": path.resolve(__dirname, "specifai", "auth", "frontend"),
      "@users": path.resolve(__dirname, "specifai", "users", "frontend"),
      "@items": path.resolve(__dirname, "specifai", "items", "frontend"),
      "@admin": path.resolve(__dirname, "specifai", "admin", "frontend"),
      "@workspaces": path.resolve(__dirname, "specifai", "workspaces", "frontend"),
    },
  },
  plugins: [
    tanstackRouter({
      target: "react",
      autoCodeSplitting: true,
      routesDirectory: "specifai/general/frontend/routes",
      generatedRouteTree: "specifai/general/frontend/routeTree.gen.ts",
    }),
    react(),
    tailwindcss(),
  ],
})

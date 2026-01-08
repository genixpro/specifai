import path from "node:path"
import tailwindcss from "@tailwindcss/vite"
import { tanstackRouter } from "@tanstack/router-plugin/vite"
import react from "@vitejs/plugin-react-swc"
import { defineConfig } from "vite"

// https://vitejs.dev/config/
export default defineConfig({
  publicDir: "bradstarter/general/frontend/public",
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "bradstarter", "general", "frontend"),
      "@auth": path.resolve(__dirname, "bradstarter", "auth", "frontend"),
      "@users": path.resolve(__dirname, "bradstarter", "users", "frontend"),
      "@items": path.resolve(__dirname, "bradstarter", "items", "frontend"),
      "@admin": path.resolve(__dirname, "bradstarter", "admin", "frontend"),
    },
  },
  plugins: [
    tanstackRouter({
      target: "react",
      autoCodeSplitting: true,
      routesDirectory: "bradstarter/general/frontend/routes",
      generatedRouteTree: "bradstarter/general/frontend/routeTree.gen.ts",
    }),
    react(),
    tailwindcss(),
  ],
})

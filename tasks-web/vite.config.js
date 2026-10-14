import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// En local, /api va a la API (uvicorn en :4010); en el contenedor lo hace nginx.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5180,
    proxy: { "/api": { target: "http://localhost:4010", rewrite: (p) => p.replace(/^\/api/, "") } },
  },
});

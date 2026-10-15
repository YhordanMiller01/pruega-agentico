import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { viteSingleFile } from "vite-plugin-singlefile";

// La GUI sale como UN index.html con el JS y el CSS inline (el CSP del clúster no deja cargar
// scripts aparte) y se escribe dentro de tasks-api, que la sirve en "/".
// En local (npm run dev) las llamadas a la API van a uvicorn en :4010.
export default defineConfig({
  plugins: [react(), viteSingleFile()],
  build: { outDir: "../tasks-api/app/static", emptyOutDir: true },
  server: {
    port: 5180,
    proxy: { "/tasks": "http://localhost:4010", "/health": "http://localhost:4010" },
  },
});

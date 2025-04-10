/// <reference types="vite/client" />

interface ImportMetaEnv {
    readonly VITE_API_URL: string
    // agregar más variables de entorno según se necesiten
  }
  
  interface ImportMeta {
    readonly env: ImportMetaEnv
  }
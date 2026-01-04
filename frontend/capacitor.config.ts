import type { CapacitorConfig } from "@capacitor/cli";

const config: CapacitorConfig = {
  appId: "com.olllama.chat.py",
  appName: "ollama mobile chat",
  webDir: "public", // not used if server.url is set
  server: {
    url: "https://chat-frontend-i7uy.onrender.com",
    cleartext: false,
  },
};

export default config;

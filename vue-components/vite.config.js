export default {
  base: "./",
  build: {
    lib: {
      entry: "./src/main.js",
      name: "trame_tauri",
      formats: ["umd"],
      fileName: "trame-tauri",
    },
    rollupOptions: {
      external: ["vue"],
      output: {
        globals: {
          vue: "Vue",
        },
      },
    },
    outDir: "../src/trame_tauri/module/serve",
    assetsDir: ".",
  },
};

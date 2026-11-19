import { open, save, message, confirm, ask } from "@tauri-apps/plugin-dialog";

export default {
  emits: ["open", "save", "message", "confirm", "ask"],
  setup(props, { emit, expose }) {
    expose({
      open: async (...args) => emit("open", await open(...args)),
      save: async (...args) => emit("save", await save(...args)),
      message: async (...args) => emit("message", await message(...args)),
      confirm: async (...args) => emit("confirm", await confirm(...args)),
      ask: async (...args) => emit("ask", await ask(...args)),
    });
  },
  template: `<slot />`,
};

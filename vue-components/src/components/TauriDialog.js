import { open, save, message, confirm, ask } from "@tauri-apps/api/dialog";

export default {
  emits: ["open", "save", "message", "confirm", "ask"],
  setup(props, { emit, expose }) {
    expose({
      open: async (kwargs) => emit("open", await open(kwargs)),
      save: async (kwargs) => emit("save", await save(kwargs)),
      message: async (kwargs) => emit("message", await message(kwargs)),
      confirm: async (kwargs) => emit("confirm", await confirm(kwargs)),
      ask: async (kwargs) => emit("ask", await ask(kwargs)),
    });
  },
};

import { listen, once } from "@tauri-apps/api/event";
import { onBeforeUnmount, onMounted } from "vue";

export default {
  props: {
    listen: {
      type: Array,
      default: () => [],
    },
    once: {
      type: Array,
      default: () => [],
    },
  },
  emits: [
    "noTauri",
    "update",
    "update-download-progress",
    "update-install",
    "menu",
    "update-status",
    "update-available",
    "blur",
    "close-requested",
    "window-created",
    "destroyed",
    "file-drop",
    "file-drop-cancelled",
    "file-drop-hover",
    "focus",
    "move",
    "resize",
    "scale-change",
    "theme-changed",
  ],
  setup(props, { emit }) {
    const subscriptions = [];

    onMounted(async () => {
      try {
        for (let i = 0; i < props.listen.length; i++) {
          const name = props.listen[i];
          const jsName = name.replaceAll("_", "-");
          const eventName = `tauri://${jsName}`;
          subscriptions.push(
            await listen(eventName, (e) => {
              emit(jsName, e.payload);
            })
          );
        }
        for (let i = 0; i < props.once.length; i++) {
          const name = props.once[i];
          const jsName = name.replaceAll("_", "-");
          const eventName = `tauri://${jsName}`;
          subscriptions.push(
            await once(eventName, (e) => {
              emit(jsName, e.payload);
            })
          );
        }
      } catch (e) {
        emit("noTauri");
      }
    });

    onBeforeUnmount(() => {
      while (subscriptions.length) {
        subscriptions.pop()();
      }
    });
  },
};

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
  setup(props, { emit }) {
    const subscriptions = [];

    onMounted(async () => {
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
    });

    onBeforeUnmount(() => {
      while (subscriptions.length) {
        subscriptions.pop()();
      }
    })
  },
};

import { listen, once } from "@tauri-apps/api/event";

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
  async mounted() {
    this.unsubscribes = [];
    for (let i = 0; i < this.listen.length; i++) {
      const name = this.listen[i];
      const eventName = `tauri://${name.replaceAll("_", "-")}`;
      const pyName = name.replaceAll("-", "_");
      this.unsubscribes.push(
        await listen(eventName, (e) => {
          this.$emit(pyName, e.payload);
        })
      );
    }
    for (let i = 0; i < this.once.length; i++) {
      const name = this.once[i];
      const eventName = `tauri://${name.replaceAll("_", "-")}`;
      const pyName = name.replaceAll("-", "_");
      this.unsubscribes.push(
        await once(eventName, (e) => {
          this.$emit(pyName, e.payload);
        })
      );
    }
  },
  beforeUnmount() {
    while (this.unsubscribes.length) {
      this.unsubscribes.pop()();
    }
  },
};

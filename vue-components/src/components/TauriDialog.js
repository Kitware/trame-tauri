import { open, save, message, confirm, ask } from '@tauri-apps/api/dialog';

export default {
  name: 'TauriDialog',
  methods: {
    async open(kwargs) {
      this.$emit('open', await open(kwargs));
    },
    async save(kwargs) {
      this.$emit('save', await save(kwargs));
    },
    async message(kwargs) {
      this.$emit('message', await message(kwargs));
    },
    async confirm(kwargs) {
      this.$emit('confirm', await confirm(kwargs));
    },
    async ask(kwargs) {
      this.$emit('ask', await ask(kwargs));
    },
  },
};

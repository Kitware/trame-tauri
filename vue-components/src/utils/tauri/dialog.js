export function ask(message, options) {
  return window.__TAURI__.dialog.ask(message, options);
}

export function confirm(message, options) {
  return window.__TAURI__.dialog.confirm(message, options);
}

export function open(options) {
  return window.__TAURI__.dialog.open(options);
}

export function save(options) {
  return window.__TAURI__.dialog.save(options);
}

export default {
  ask,
  confirm,
  open,
  save,
};

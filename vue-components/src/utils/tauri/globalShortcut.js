export function isRegistered(shortcut) {
  return window.__TAURI__.globalShortcut.isRegistered(shortcut);
}

export function register(shortcut, handler) {
  return window.__TAURI__.globalShortcut.register(shortcut, handler);
}

export function registerAll(shortcuts, handler) {
  return window.__TAURI__.globalShortcut.registerAll(shortcuts, handler);
}

export function unregister(shortcut) {
  return window.__TAURI__.globalShortcut.unregister(shortcut);
}

export function unregisterAll() {
  return window.__TAURI__.globalShortcut.unregisterAll();
}

export default {
  isRegistered,
  register,
  registerAll,
  unregister,
  unregisterAll,
};

export function invoke(cmd, args) {
  return window.__TAURI__.tauri.invoke(cmd, args);
}

export function transformCallback(fn, once = false) {
  return window.__TAURI__.tauri.transformCallback(fn, once);
}

export default {
  invoke,
  transformCallback,
};

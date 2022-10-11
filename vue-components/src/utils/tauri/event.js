export function emit(event, payload) {
  return window.__TAURI__.event.emit(event, payload);
}

export function listen(event, handler) {
  return window.__TAURI__.event.listen(event, handler);
}

export function once(event, handler) {
  return window.__TAURI__.event.once(event, handler);
}

export default {
  emit,
  listen,
  once,
};

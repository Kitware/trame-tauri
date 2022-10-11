export function isPermissionGranted() {
  return window.__TAURI__.globalShortcut.isPermissionGranted();
}

export function requestPermission() {
  return window.__TAURI__.globalShortcut.requestPermission();
}

export function sendNotification(options) {
  return window.__TAURI__.globalShortcut.sendNotification(options);
}

export default {
  isPermissionGranted,
  requestPermission,
  sendNotification,
};

export function readText() {
  return window.__TAURI__.clipboard.readText();
}

export function writeText(txt) {
  return window.__TAURI__.clipboard.writeText(txt);
}

export default {
  readText,
  writeText,
};

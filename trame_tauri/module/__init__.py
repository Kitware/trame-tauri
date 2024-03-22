from pathlib import Path

serve_path = str(Path(__file__).with_name("serve").resolve())
serve = {"__trame_tauri": serve_path}
scripts = ["__trame_tauri/trame-tauri.umd.js"]
vue_use = ["trame_tauri"]

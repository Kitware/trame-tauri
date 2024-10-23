# Cool app bundle

This example use tauri to bundle that could trame/vtk/wasm app.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install trame trame-vtklocal trame-vuetify trame-components pyinstaller
pip install "vtk==9.3.20241005.dev0" --extra-index-url https://wheels.vtk.org
```
Build bundle for tauri inside `./src-tauri/server/*` while skipping the web content.

```bash
python -m PyInstaller \
    --clean --noconfirm \
    --distpath src-tauri \
    --name server \
    --hidden-import pkgutil \
    widget.py
```

Generate webcontent for tauri to bundle

```bash
python -m trame.tools.www --output ./src-tauri/www
```
In order to build and bundle the application, just run

```bash
# Generate icon for application using ./app-icon.png
cargo tauri icon

# Generate application
cargo tauri build
```

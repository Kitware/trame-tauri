## Setup

Python setup for building sidecar as single file.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install trame trame-tauri pyinstaller

python -m PyInstaller \
    --clean --noconfirm \
    --distpath src-tauri \
    --name server \
    --hidden-import pkgutil \
    --collect-data trame_client \
    server.py

python -m trame.tools.www --output ./src-tauri/www

cd src-tauri
cargo tauri icon
cargo tauri build

open target/release/bundle/macos/Cone.app
```

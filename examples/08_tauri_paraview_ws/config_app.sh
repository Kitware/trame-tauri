#!/bin/bash

set -e
set -x

python -m PyInstaller \
    --clean --noconfirm \
    --distpath src-tauri \
    --name server --hidden-import pkgutil \
    --collect-all paraview
    cone.py

python -m trame.tools.www --output ./src-tauri/www
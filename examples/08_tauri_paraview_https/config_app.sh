#!/bin/bash

set -e
set -x

python -m PyInstaller \
    --clean --noconfirm \
    --distpath src-tauri \
    --name server --hidden-import pkgutil \
    --collect-data trame_vtk \
    --collect-data trame_client \
    --collect-data trame_vuetify \
    --collect-all paraview \
    --hidden-import pkgutil \
    cone.py

python -m trame.tools.www --output ./src-tauri/www

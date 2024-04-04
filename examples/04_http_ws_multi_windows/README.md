# HTTP + WebSocket

This example leverage tauri for just its WebView and let trame act as the full HTTP server by serving its content over HTTP and WebSocket.

## Tauri project

Please look at previous examples for references.

## Trame example

We use a simple example since it does not have any complex python dependency.


```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install trame trame-vuetify trame-tauri
```

## Tauri bundle

In order to build and bundle the application, just run

```bash
# Generate icon for application using ./app-icon.png
cargo tauri icon

# Generate application
cargo tauri build
```

## Running application

### Linux and macOS
```bash
# Start server
python ./server.py &

# Run desktop application
open ./src-tauri/target/release/bundle/macos/MultiWindows.app
```

### Windows
```batch
# Start server
python .\server.py

# Run desktop application in a new terminal or by navigating and opening the file
.\src-tauri\target\release\MultiWindows.exe
```

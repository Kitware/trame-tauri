# Client only

This example create a standalone tauri example that is going to connect to a remote trame server using a command line interface for providing where the application should connect.
Therefore, you will have to provide your server.

## Desktop client

### Linux and macOS
```bash
cargo tauri build
"./src-tauri/target/release/bundle/macos/Trame Client.app/Contents/MacOS/Trame Client" --url http://localhost:4444
```

### Windows
```batch
cargo tauri build
& '.\src-tauri\target\release\Trame Client.exe' --url http://localhost:4444
```

## Cheat sheet

Install Rust + Tauri

```sh
cargo install tauri-cli --version "^2.0.0" --locked
cargo tauri init
```

Build a tauri bundle

```sh
cargo tauri build
```

or with dedicated target:
- aarch64-apple-darwin
- x86_64-apple-darwin
- universal-apple-darwin


```sh
cargo tauri build --target aarch64-apple-darwin
```

Get binary extension for a platform

```sh
rustc -Vv | grep host | cut -f2 -d' '
aarch64-apple-darwin
```

## Refs

- Sidecar
    - https://v2.tauri.app/develop/sidecar/
    - https://v2.tauri.app/develop/sidecar/#running-it-from-rust
    - (Express) https://github.com/tauri-apps/tauri/discussions/5336
    - (Python) https://github.com/tauri-apps/tauri/discussions/2759
    - (example repo) https://github.com/cherob/tauri-rust-py
    - (kill sidecar) https://github.com/tauri-apps/tauri/discussions/3273

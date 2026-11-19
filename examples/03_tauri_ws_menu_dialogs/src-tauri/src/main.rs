#![cfg_attr(
  all(not(debug_assertions), target_os = "windows"),
  windows_subsystem = "windows"
)]

use tauri::menu::{MenuBuilder, SubmenuBuilder};
use tauri::{Emitter, Manager};
use tauri_plugin_shell::{process::CommandEvent, ShellExt};
use std::time::Duration;
use async_std::task;

fn main() {
  tauri::Builder::default()
    .plugin(tauri_plugin_shell::init())
    .plugin(tauri_plugin_dialog::init())
    .plugin(tauri_plugin_notification::init())
    .setup(|app| {
      let splashscreen_window = app.get_webview_window("splashscreen").unwrap();
      let main_window = app.get_webview_window("main").unwrap();

      let (mut rx, _) = app.shell().sidecar("trame")
        .expect("failed to create sidecar")
        .args(["--server", "--port", "0", "--timeout", "1", "--no-http"])
        .spawn()
        .expect("Failed to spawn server");

      tauri::async_runtime::spawn(async move {
        while let Some(event) = rx.recv().await {
          if let CommandEvent::Stdout(line) = event {
            let line = String::from_utf8_lossy(&line);
            if line.contains("tauri-server-port=") {
              let tokens: Vec<&str> = line.split("=").collect();
              let port_token = tokens[1].to_string();
              let port = port_token.trim();
              // println!("window.location.replace(window.location.href + '?sessionURL=ws://localhost:{}/ws')", port);
              let _ = main_window.eval(&format!("window.location.replace(window.location.href + '?sessionURL=ws://localhost:{}/ws')", port));
            }
            if line.contains("tauri-client-ready") {
              task::sleep(Duration::from_secs(2)).await;
              splashscreen_window.close().unwrap();
              main_window.show().unwrap();
            }
          }
        }
      });
      Ok(())
    })
    .menu(|handle| {
      // Native Menu
      let file_menu = SubmenuBuilder::new(handle, "File")
        .text("close", "Close")
        .text("quit", "Quit")
        .build()?;
      let view_menu = SubmenuBuilder::new(handle, "View")
        .text("reset_camera", "Reset Camera")
        .build()?;
      let dialog_menu = SubmenuBuilder::new(handle, "Dialog")
        .text("dialog::ask", "Ask")
        .text("dialog::confirm", "Confirm")
        .text("dialog::message", "Message")
        .text("dialog::open", "Open")
        .text("dialog::save", "Save")
        .build()?;
      MenuBuilder::new(handle)
        .item(&file_menu)
        .item(&view_menu)
        .item(&dialog_menu)
        .build()
    })
    .on_menu_event(|app, event| {
      // Forward menu clicks to trame: tauri.Events(listen=["menu"]) in cone.py
      let _ = app.emit("tauri://menu", event.id().as_ref());
      match event.id().as_ref() {
        "quit" => {
          app.exit(0);
        }
        "close" => {
          app.get_webview_window("main").unwrap().close().unwrap();
        }
        _ => {}
      }
    })
    .run(tauri::generate_context!())
    .expect("error while running application");
}

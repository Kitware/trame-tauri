#![cfg_attr(
  all(not(debug_assertions), target_os = "windows"),
  windows_subsystem = "windows"
)]

use tauri::api::process::{Command, CommandEvent};
use tauri::{CustomMenuItem, Menu, MenuItem, Submenu};
use tauri::Manager;
use std::time::Duration;
use async_std::task;

fn main() {
  // Menu definition
  let quit = CustomMenuItem::new("quit".to_string(), "Quit");
  let close = CustomMenuItem::new("close".to_string(), "Close");
  let submenu = Submenu::new("File", Menu::new().add_item(quit).add_item(close));
  let menu = Menu::new()
    .add_submenu(submenu);

  tauri::Builder::default()
    .setup(|app| {
      let splashscreen_window = app.get_window("splashscreen").unwrap();
      let main_window = app.get_window("main").unwrap();

      let (mut rx, _) = Command::new_sidecar("trame")
        .expect("failed to create sidecar")
        // --no-http: only available in trame-server>=2.4.0
        .args(["--server", "--port", "0", "--timeout", "10", "--no-http"])
        .spawn()
        .expect("Failed to spawn server");

      tauri::async_runtime::spawn(async move {
        while let Some(event) = rx.recv().await {
          if let CommandEvent::Stdout(line) = event {
            if line.contains("tauri-server-port=") {
              let tokens: Vec<&str> = line.split("=").collect();
              // println!("Connect to port {}", tokens[1]);
              main_window.eval(&format!("window.location.search = 'sessionURL=ws://localhost:{}/ws'", tokens[1]));
              task::sleep(Duration::from_secs(2)).await; // Just to keep splash longer
              splashscreen_window.close().unwrap();
              main_window.show().unwrap();
            }
          }
        }
      });
      Ok(())
    })
    .menu(menu)
    .run(tauri::generate_context!())
    .expect("error while running application");
}

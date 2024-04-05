// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use tauri::Manager;

fn main() {
  tauri::Builder::default()
    .setup(|app| {
      let main_window = app.get_window("main").unwrap();
      match app.get_cli_matches() {
        // `matches` here is a Struct with { args, subcommand }.
        // `args` is `HashMap<String, ArgData>` where `ArgData` is a struct with { value, occurrences }.
        // `subcommand` is `Option<Box<SubcommandMatches>>` where `SubcommandMatches` is a struct with { name, matches }.
        Ok(matches) => {
          let url_to_connect = &matches.args.get("url").unwrap().value;
          println!("{}", url_to_connect);
          let _ = main_window.eval(&format!("window.location.replace({})", url_to_connect));
          main_window.show().unwrap();
        }
        Err(_) => {}
      }
      Ok(())
    })
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
}

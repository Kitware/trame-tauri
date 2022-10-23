def test_import():
    from trame_tauri.widgets.tauri import Events  # noqa: F401

    # For components only, the Events is also importable via trame
    from trame.widgets.tauri import Events  # noqa: F401,F811

def test_import():
    from trame_tauri.widgets.tauri import CustomWidget  # noqa: F401

    # For components only, the CustomWidget is also importable via trame
    from trame.widgets.tauri import CustomWidget  # noqa: F401,F811

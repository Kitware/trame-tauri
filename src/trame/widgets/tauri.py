from trame_tauri.widgets.tauri import *  # noqa: F403


def initialize(server):
    from trame_tauri import module

    server.enable_module(module)

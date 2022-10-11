from trame_tauri.widgets.tauri import *


def initialize(server):
    from trame_tauri import module

    server.enable_module(module)

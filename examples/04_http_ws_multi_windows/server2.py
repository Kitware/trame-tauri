from trame.app import get_server
from trame.decorators import TrameApp
from trame.ui.vuetify3 import SinglePageLayout

from trame.widgets import html, tauri
from trame.widgets import vuetify3 as v3


@TrameApp()
class TestApp:
    def __init__(self, name=None):
        self.server = get_server(name)
        self.server.state.update(
            {
                "position": None,
                "size": None,
                "scale": 0,
                "window_list": [],
            }
        )
        tauri.initialize(self.server)
        self.build_ui_main()
        self.build_ui_hello_world()

    def window_event(self, event_type, window, event):
        print(event_type, window, event)

    def build_ui_main(self):
        with SinglePageLayout(self.server, full_height=True) as layout:
            with html.Div(v_if=("enable_windows", True)):
                self.windows = tauri.Window(
                    v_for="window_item, i in window_list",
                    key=("window_item.key || `window_${i}`",),
                    title=("window_item.title",),
                    url=("window_item.url",),
                    visible=("window_item.visible || true",),
                    width=("window_item.width",),
                    height=("window_item.height",),
                    x=("window_item.pos_x"),
                    y=("window_item.pos_y"),
                    # Will not work in Tauri v1: https://github.com/tauri-apps/tauri/issues/8435
                    # prevent_close=("window_item.prevent_close"),
                    options=("window_item.options",),
                    created=(self.window_event, "['created', window_item, $event]"),
                    closed=(self.window_event, "['closed', window_item, $event]"),
                    moved=(self.window_event, "['moved', window_item, $event]"),
                    resized=(self.window_event, "['resized', window_item, $event]"),
                    file_drop=(self.window_event, "['file_drop', window_item, $event]"),
                    focus_changed=(
                        self.window_event,
                        "['focus_changed', window_item, $event]",
                    ),
                    menu_clicked=(
                        self.window_event,
                        "['menu_clicked', window_item, $event]",
                    ),
                    scale_changed=(
                        self.window_event,
                        "['scale_changed', window_item, $event]",
                    ),
                    theme_changed=(
                        self.window_event,
                        "['theme_changed', window_item, $event]",
                    ),
                )

            with layout.toolbar.clear():
                v3.VToolbarTitle("Multi Window example")
                v3.VSpacer()
                html.Div("URL: {{ window.location }}")
                v3.VSpacer()
                v3.VBtn("Create Window", click=self.create_window)
                v3.VBtn(
                    "Open Hello World",
                    disabled=("window_hello_world", False),
                    click="window_hello_world = true",
                )
                v3.VBtn(
                    "Close Hello World",
                    disabled=("!window_hello_world",),
                    click="window_hello_world = false",
                )
                v3.VBtn(
                    "Toggle windows",
                    click="enable_windows = !enable_windows",
                )
            with layout.content:
                with v3.VContainer():
                    with v3.VCard():
                        v3.VCardTitle("Main Page")
                        with tauri.Window(main=True) as w:
                            self.server.controller.request_user_attention = (
                                w.request_user_attention
                            )
                            with v3.Template(
                                raw_attrs=['v-slot="{ position, size, scaleFactor }"']
                            ):
                                html.Div(
                                    "{{ position }} | {{ size }} | {{ scaleFactor }}"
                                )

                html.Div("p({{ position }}) - s({{ size }}) - d({{ scale }})")
                v3.VDivider(style="margin: 8px;")
                with html.Div(v_if=("window_hello_world", False)):
                    with tauri.Window(
                        url="http://localhost:4444/index.html?ui=hello_world",
                        visible=("window_hello_world", False),
                        title=("child_title", "Hello"),
                        x=("pos_x", 100),
                        y=("pos_y", 100),
                        width=("size_w", 300),
                        height=("size_h", 300),
                        options=(
                            "child_options",
                            {
                                # "alwaysOnTop": True,
                                # "center": True,
                                # "closable": False,
                                # "decorations": False,
                                "focus": False,  # Does not work
                                "minHeight": 200,
                                "minWidth": 200,
                                "maxHeight": 800,
                                "maxWidth": 800,
                                # "maximizable": False,  # You need `"decoration": True` to see this (button will be disabled)
                                # "minimizable": False,  # You need `"decoration": True` to see this (button will be disabled)
                                # "skipTaskbar": True,  # Does not work
                                "theme": "light",
                                "fileDropEnabled": False,
                            },
                        ),
                        prevent_close=True,  # Will not work using Tauri v1: https://github.com/tauri-apps/tauri/issues/8435
                        moved="position = $event",
                        resized="size = $event",
                        scale_changed="scale = $event",
                        created="{ position, size, scaleFactor: scale } = $event",
                        closed="window_hello_world = false; window.console.log('evt closed')",
                        file_drop="window.console.log('file:', $event)",
                        theme_changed="window.console.log('theme:', $event)",
                    ) as w:
                        self.server.controller.trigger_name(w.request_user_attention)
                        with v3.Template(raw_attrs=['v-slot="data"']):
                            v3.VTextField(v_model="child_title")
                            v3.VBtn("Center", click=w.center)
                            v3.VBtn("Show", click=w.show)
                            v3.VBtn("Close", click=w.close)
                            v3.VBtn("Hide", click=w.hide)
                            v3.VBtn("Maximize", click=w.maximize)
                            v3.VBtn("Un-Maximize", click=w.unmaximize)
                            v3.VBtn("Minimize", click=w.minimize)
                            v3.VBtn("Un-Minimize", click=w.unminimize)
                            v3.VBtn("Focus", click=w.grab_focus)
                            v3.VBtn("Fullscreen On", click=(w.set_fullscreen, "[true]"))
                            v3.VBtn(
                                "Fullscreen Off", click=(w.set_fullscreen, "[false]")
                            )
                            # Only usable if the app doesn't have focus...
                            v3.VBtn(
                                "Request User's Attention",
                                click=(
                                    w.request_user_attention,
                                    "[2]",
                                ),  # None and 1 don't work
                            )
                            v3.VBtn(
                                "Request User's Attention (main)",
                                click=(
                                    self.server.controller.request_user_attention,
                                    "[2]",
                                ),
                            )
                            v3.VBtn("Set Position", click=(w.set_position, "[0,0]"))
                            v3.VBtn("Set Size", click=(w.set_size, "[400, 400]"))
                            v3.VBtn("Set Title", click=(w.set_title, "['World']"))
                            html.Div("{{ data }}")
                            v3.VSlider(v_model="pos_x", min=100, max=500, step=5)
                            v3.VSlider(v_model="pos_y", min=100, max=500, step=5)
                            v3.VSlider(v_model="size_w", min=100, max=500, step=5)
                            v3.VSlider(v_model="size_h", min=100, max=500, step=5)

    def build_ui_hello_world(self):
        with SinglePageLayout(
            self.server, template_name="hello_world", full_height=True
        ) as layout:
            # Not working
            # with layout.toolbar as tb:
            #     tb._attributes["drag"] = 'data-tauri-drag-region'
            #     print(tb)

            with layout.content:
                with v3.VContainer():
                    with v3.VCard():
                        print(v3.VCardTitle("Hello World!"))

    def create_window(self):
        self.server.state.window_list.append(
            {
                "key": f"window_{len(self.server.state.window_list)}",
                "title": f"New Window {len(self.server.state.window_list)}",
                "url": "http://localhost:4444/index.html?ui=hello_world",
            }
        )
        self.server.state.dirty("window_list")


if __name__ == "__main__":
    app = TestApp()
    app.server.start(port=4444, open_browser=False)

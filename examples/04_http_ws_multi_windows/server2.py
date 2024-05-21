from trame.app import get_server
from trame.decorators import TrameApp
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import html, tauri, vuetify3 as v3


@TrameApp()
class TestApp:
    def __init__(self, name=None):
        self.server = get_server(name)
        self.server.state.update(
            {
                "position": None,
                "size": None,
                "scale": 0,
            }
        )
        tauri.initialize(self.server)
        self.build_ui_main()
        self.build_ui_hello_world()

    def build_ui_main(self):
        with SinglePageLayout(self.server, full_height=True) as layout:
            with layout.toolbar.clear():
                v3.VToolbarTitle("Multi Window example")
                v3.VSpacer()

                v3.VSpacer()
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
            with layout.content:
                with v3.VContainer():
                    with v3.VCard():
                        v3.VCardTitle("Main Page")
                        with tauri.Window(main=True) as w:
                            with v3.Template(
                                raw_attrs=['v-slot="{ position, size, scaleFactor }"']
                            ):
                                html.Div(
                                    "{{ position }} | {{ size }} | {{ scaleFactor }}"
                                )

                html.Div("p({{ position }}) - s({{ size }}) - d({{ scale }})")
                with tauri.Window(
                    url="http://localhost:4444/index.html?ui=hello_world",
                    visible=("window_hello_world", False),
                    title="Hello",
                    width=300,
                    height=300,
                    moved="position = $event",
                    resized="size = $event",
                    scale_changed="scale = $event",
                    created="{ position, size, scaleFactor: scale } = $event",
                    closed="window_hello_world = false",
                ) as w:
                    with v3.Template(raw_attrs=['v-slot="data"']):
                        v3.VBtn("Center", click=w.center)
                        v3.VBtn("Show", click=w.show)
                        v3.VBtn("Hide", click=w.hide)
                        v3.VBtn("Maximize", click=w.maximize)
                        v3.VBtn("Un-Maximize", click=w.unmaximize)
                        v3.VBtn("Minimize", click=w.minimize)
                        v3.VBtn("Un-Minimize", click=w.unminimize)
                        v3.VBtn("Focus", click=w.grab_focus)
                        html.Div("{{ data }}")

    def build_ui_hello_world(self):
        with SinglePageLayout(
            self.server, template_name="hello_world", full_height=True
        ) as layout:
            with layout.content:
                with v3.VContainer():
                    with v3.VCard():
                        v3.VCardTitle("Hello World!")


if __name__ == "__main__":
    app = TestApp()
    app.server.start(port=4444, open_browser=False)

from trame.app import get_server, asynchronous
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import vuetify3 as vuetify, vtk, tauri
from trame.decorators import TrameApp, life_cycle


@TrameApp()
class Cone:
    def __init__(self, server=None):
        self.server = get_server(server)
        self.ui = self._build_ui()

    @property
    def state(self):
        return self.server.state

    @property
    def ctrl(self):
        return self.server.controller

    # -----------------------------------------------------
    # Dialog interactions
    # -----------------------------------------------------

    async def dialog_ask(self):
        with self.state:
            self.state.logs += "Ask\n"

        with self.state:
            response = await self.ctrl.ask(
                "What is your name?",
                title="Just a question",
                type="warning",
            )
            self.state.logs += f"=> {response}\n"

    async def dialog_confirm(self):
        with self.state:
            self.state.logs += "Confirm\n"

        with self.state:
            response = await self.ctrl.confirm(
                "Is it a yes?",
                title="Just a yes/no",
                type="error",
            )
            self.state.logs += f"=> {response}\n"

    async def dialog_message(self):
        print("message", flush=True)
        with self.state:
            self.state.logs += "Message\n"

        with self.state:
            response = await self.ctrl.message(
                "Just a message",
                title="Just a text",
                type="info",
            )
            self.state.logs += f"=> {response}\n"

    async def dialog_open(self):
        with self.state:
            self.state.logs += "Open\n"

        with self.state:
            response = await self.ctrl.open("Open")
            self.state.logs += f"=> {response}\n"

    async def dialog_save(self):
        with self.state:
            self.state.logs += "Save\n"

        with self.state:
            response = await self.ctrl.save("Save")
            self.state.logs += f"=> {response}\n"

    # -----------------------------------------------------

    def on_menu(self, name):
        if name == "reset_camera":
            self.ctrl.reset_camera()
        elif name == "dialog::ask":
            asynchronous.create_task(self.dialog_ask())
        elif name == "dialog::confirm":
            asynchronous.create_task(self.dialog_confirm())
        elif name == "dialog::message":
            asynchronous.create_task(self.dialog_message())
        elif name == "dialog::open":
            asynchronous.create_task(self.dialog_open())
        elif name == "dialog::save":
            asynchronous.create_task(self.dialog_save())

        # Just letting you know about menu call
        print(f"on_menu={name}", flush=True)
        try:
            import os

            os.system(f"say menu {name}")
        except Exception:
            pass

    def _build_ui(self):
        with SinglePageLayout(self.server) as layout:
            # Tauri events
            tauri.Events(listen=["menu"], menu=(self.on_menu, "[$event]"))
            with tauri.Dialog() as dialog:
                self.ctrl.ask = dialog.ask
                self.ctrl.confirm = dialog.confirm
                self.ctrl.message = dialog.message
                self.ctrl.open = dialog.open
                self.ctrl.save = dialog.save

            with layout.content:
                with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
                    with vtk.VtkView(ref="view") as view:
                        self.ctrl.reset_camera = view.reset_camera
                        with vtk.VtkGeometryRepresentation():
                            vtk.VtkAlgorithm(
                                vtk_class="vtkConeSource", state=("{ resolution }",)
                            )
                    vuetify.VTextarea(
                        v_model=("logs", ""),
                        style=(
                            "position: absolute;"
                            "z-index: 1;"
                            "bottom: 10px;"
                            "left: 10px;"
                            "width: 50vw;"
                            "background: #fff;"
                        ),
                    )

            with layout.toolbar:
                vuetify.VSpacer()
                vuetify.VSlider(
                    v_model=("resolution", 6),
                    min=3,
                    max=60,
                    step=1,
                    hide_details=True,
                    dense="compact",
                    style="max-width: 300px;",
                )
                with vuetify.VBtn(icon=True, click=self.ctrl.reset_camera):
                    vuetify.VIcon("mdi-crop-free")
                vuetify.VBtn(
                    "Notification",
                    click="utils.tauri.notification.sendNotification('Hello from Tauri')",
                )

            return layout

    @life_cycle.server_ready
    def _tauri_ready(self, **_):
        print(f"tauri-server-port={self.server.port}", flush=True)

    @life_cycle.client_connected
    def _tauri_show(self, **_):
        print("tauri-client-ready", flush=True)


if __name__ == "__main__":
    app = Cone()
    app.server.start()

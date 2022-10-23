import os
from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify, vtk, tauri

server = get_server()
state, ctrl = server.state, server.controller


@ctrl.add("on_server_ready")
def notify_tauri(**kwargs):
    print(f"tauri-server-port={server.port}", flush=True)


@ctrl.set("on_menu")
def on_menu(name):
    os.system(f"say menu {name}")
    print(f"on_menu={name}", flush=True)


with SinglePageLayout(server) as layout:
    tauri.Events(listen=["menu"], menu=(ctrl.on_menu, "[$event]"))
    with layout.content:
        with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
            with vtk.VtkView(ref="view"):
                with vtk.VtkGeometryRepresentation():
                    vtk.VtkAlgorithm(
                        vtk_class="vtkConeSource", state=("{ resolution }",)
                    )

    with layout.toolbar:
        vuetify.VSpacer()
        vuetify.VSlider(
            v_model=("resolution", 6),
            min=3,
            max=60,
            step=1,
            hide_details=True,
            dense=True,
            style="max-width: 300px;",
        )
        with vuetify.VBtn(icon=True, click="$refs.view.resetCamera()"):
            vuetify.VIcon("mdi-crop-free")

if __name__ == "__main__":
    server.start()

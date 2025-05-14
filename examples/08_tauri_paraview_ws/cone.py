import os
from trame.app import get_server
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import vuetify3 as vuetify, paraview
from trame.decorators import TrameApp, change, life_cycle

from paraview import simple

# Configure ParaView for headless operation when using standard Python interpreter
# (pvpython sets this automatically, but regular python requires manual configuration)
from paraview.modules import vtkRemotingCore as rc

rc.vtkProcessModule.GetProcessModule().UpdateProcessType(
    rc.vtkProcessModule.PROCESS_BATCH, 0
)


@TrameApp()
class Cone:
    """
    This application uses the ParaView simple API to create a cone
    and display it in a web application using Tauri. This application
    uses remote rendering.
    """

    def __init__(self, server=None):
        self.server = get_server(server)
        self.state = self.server.state
        self.ctrl = self.server.controller

        cone = simple.Cone()
        representation = simple.Show(cone)
        view = simple.Render()

        self.cone = cone
        self.representation = representation
        self.view = view
        self.resolution = 6

        self.ui = self._build_ui()

    @change("resolution")
    def update_cone(self, resolution, **kwargs):
        self.cone.Resolution = resolution
        self.ctrl.view_update()

    def _build_ui(self):
        with SinglePageLayout(self.server) as layout:
            with layout.content:
                with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
                    html_view = paraview.VtkRemoteView(self.view, ref="view")
                    self.ctrl.view_reset_camera = html_view.reset_camera
                    self.ctrl.view_update = html_view.update

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
                with vuetify.VBtn(icon=True, click=self.server.controller.reset_camera):
                    vuetify.VIcon("mdi-crop-free")

            return layout

    # Use os.write for immediate unbuffered output to ensure Tauri
    # receives the port number before Python's stdout buffer flushes
    @life_cycle.server_ready
    def _tauri_ready(self, **_):
        os.write(1, f"tauri-server-port={self.server.port}\n".encode())

    @life_cycle.client_connected
    def _tauri_show(self, **_):
        os.write(1, "tauri-client-ready\n".encode())


if __name__ == "__main__":
    app = Cone()
    app.server.start()

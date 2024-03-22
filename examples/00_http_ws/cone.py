from trame.app import get_server
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import vuetify3 as vuetify, vtk
from trame.decorators import TrameApp, life_cycle

@TrameApp()
class Cone:
    def __init__(self, server=None):
        self.server = get_server(server)
        self.ui = self._build_ui()

    def _build_ui(self):
        with SinglePageLayout(self.server) as layout:
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
                    dense="compact",
                    style="max-width: 300px;",
                )
                with vuetify.VBtn(icon=True, click="$refs.view.resetCamera()"):
                    vuetify.VIcon("mdi-crop-free")
            
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

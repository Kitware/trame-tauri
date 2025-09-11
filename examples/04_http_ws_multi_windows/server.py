from trame.app import get_server
from trame.decorators import TrameApp
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import tauri, vuetify3 as v3


@TrameApp()
class TestApp:
    def __init__(self, name=None):
        self.server = get_server(name)
        tauri.initialize(self.server)
        self.build_ui_main()
        self.build_ui_hello_world()

    def build_ui_main(self):
        with SinglePageLayout(self.server, full_height=True) as layout:
            with layout.toolbar.clear():
                v3.VToolbarTitle("Multi Window example")
                v3.VSpacer()
                v3.VBtn(
                    "Open Hello World",
                    disabled=("window_hello_world", False),
                    click="""
                        async () => {
                            const LogicalPosition = trame.utils.tauri.window.LogicalPosition;
                            console.log(LogicalPosition)
                            console.log(new LogicalPosition(10, 20));
                            const appWindow = trame.utils.tauri.window.appWindow;
                            const position = await appWindow.outerPosition();
                            const size = await appWindow.outerSize();
                            let scaleFactor = await appWindow.scaleFactor();
                            appWindow.onScaleChanged(({ payload }) => {scaleFactor = payload.scaleFactor});
                            appWindow.onMoved(async ({ payload }) => {
                                const size = await appWindow.outerSize();
                                hello_window = trame.utils.tauri.window.WebviewWindow.getByLabel('hello_world');
                                await hello_window.setPosition(
                                    new LogicalPosition(
                                        (payload.x + size.width) / scaleFactor, payload.y / scaleFactor
                                    )
                                );
                            });

                            const hello_world = new trame.utils.tauri.window.WebviewWindow('hello_world', {
                                url: 'http://localhost:4444/index.html?ui=hello_world',
                                height: size.height / scaleFactor,
                                width: 300,
                                title: 'Hello',
                                x: (position.x + size.width) / scaleFactor,
                                y: position.y / scaleFactor,
                            });
                            hello_world.onCloseRequested(() => { window_hello_world = false; });
                            window_hello_world = true;
                        }
                    """,
                )
                v3.VBtn(
                    "Close Hello World",
                    disabled=("!window_hello_world",),
                    click="""
                        async () => {
                            window_hello_world = false;
                            hello_window = trame.utils.tauri.window.WebviewWindow.getByLabel('hello_world');
                            if (hello_window) {
                                await hello_window.close();
                            }
                        }
                    """,
                )
            with layout.content:
                with v3.VContainer():
                    with v3.VCard():
                        v3.VCardTitle("Main Page")
                v3.VFileInput(label="Test File Input")

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

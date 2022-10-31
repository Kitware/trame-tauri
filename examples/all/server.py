import os
from trame.app import get_server, asynchronous
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify, tauri

server = get_server()
state, ctrl = server.state, server.controller


@ctrl.add("on_server_ready")
def notify_tauri(**kwargs):
    print(f"tauri-server-port={server.port}", flush=True)


@ctrl.set("on_menu")
def on_menu(name):
    os.system(f"say menu {name}")
    print(f"on_menu={name}", flush=True)


@asynchronous.task
async def ask():
    with state:
        state.logs += "Ask\n"

    with state:
        response = await ctrl.ask(
            "What is your name?",
            title="Just a question",
            type="warn",
        )
        state.logs += f"=> {response}\n"


@asynchronous.task
async def confirm():
    with state:
        state.logs += "Confirm\n"

    with state:
        response = await ctrl.confirm(
            "Is it a yes?",
            title="Just a yes/no",
            type="error",
        )
        state.logs += f"=> {response}\n"


@asynchronous.task
async def message():
    print("message", flush=True)
    with state:
        state.logs += "Message\n"

    with state:
        response = await ctrl.message(
            "Just a message",
            title="Just a text",
            type="info",
        )
        state.logs += f"=> {response}\n"


@asynchronous.task
async def open():
    with state:
        state.logs += "Open\n"

    with state:
        response = await ctrl.open("Open")
        state.logs += f"=> {response}\n"


@asynchronous.task
async def save():
    with state:
        state.logs += "Save\n"

    with state:
        response = await ctrl.save("Save")
        state.logs += f"=> {response}\n"


with SinglePageLayout(server) as layout:
    tauri.Events(listen=["menu"], menu=(ctrl.on_menu, "[$event]"))
    d = tauri.Dialog()
    ctrl.ask = d.ask
    ctrl.confirm = d.confirm
    ctrl.message = d.message
    ctrl.open = d.open
    ctrl.save = d.save

    with layout.toolbar:
        vuetify.VSpacer()
        vuetify.VBtn("Ask", click=ask)
        vuetify.VBtn("Message", click=message)
        vuetify.VBtn("Confirm", click=confirm)
        vuetify.VBtn("Open", click=open)
        vuetify.VBtn("Save", click=save)

    with layout.content:
        vuetify.VTextarea(v_model=("logs", ""))

if __name__ == "__main__":
    server.start()

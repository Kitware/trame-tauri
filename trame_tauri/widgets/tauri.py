from trame_client.widgets.core import AbstractElement
from .. import module
import asyncio


class HtmlElement(AbstractElement):
    def __init__(self, _elem_name, children=None, **kwargs):
        super().__init__(_elem_name, children, **kwargs)
        if self.server:
            self.server.enable_module(module)


__all__ = [
    "Events",
    "Dialog",
]


# Expose your vue component(s)
class Events(HtmlElement):
    def __init__(self, listen=[], once=[], **kwargs):
        super().__init__(
            "tauri-events",
            **kwargs,
        )
        self._event_names += listen
        self._event_names += once
        l_names = ",".join(map(lambda n: f"'{n}'", listen))
        o_names = ",".join(map(lambda n: f"'{n}'", once))
        self._attributes["__listen"] = f':listen="[{l_names}]"'
        self._attributes["__once"] = f':once="[{o_names}]"'


# Expose your vue component(s)
class Dialog(HtmlElement):
    def __init__(self, ref="tauri_dialog", **kwargs):
        super().__init__(
            "tauri-dialog",
            **kwargs,
        )
        trigger_name = self.server.trigger_name(self._fill_queue)
        self._ref = ref
        self._attributes["__ref"] = f'ref="{self._ref}"'
        self._attributes["__open"] = (
            f'''@open="trigger('{trigger_name}', ['open', $event])"'''
        )
        self._attributes["__save"] = (
            f'''@save="trigger('{trigger_name}', ['save', $event])"'''
        )
        self._attributes["__ask"] = (
            f'''@ask="trigger('{trigger_name}', ['ask', $event])"'''
        )
        self._attributes["__confirm"] = (
            f'''@confirm="trigger('{trigger_name}', ['confirm', $event])"'''
        )
        self._attributes["__message"] = (
            f'''@message="trigger('{trigger_name}', ['message', $event])"'''
        )
        self._open_queue = asyncio.Queue(maxsize=1)
        self._save_queue = asyncio.Queue(maxsize=1)
        self._ask_queue = asyncio.Queue(maxsize=1)
        self._confirm_queue = asyncio.Queue(maxsize=1)
        self._message_queue = asyncio.Queue(maxsize=1)

    def _fill_queue(self, type, content):
        if type == "open":
            self._open_queue.put_nowait(content)
        if type == "save":
            self._save_queue.put_nowait(content)
        if type == "ask":
            self._ask_queue.put_nowait(content)
        if type == "confirm":
            self._confirm_queue.put_nowait(content)
        if type == "message":
            self._message_queue.put_nowait(content)

    async def ask(self, message, title=None, type=None, **kwargs):
        options = {}
        if title:
            options["title"] = title
        if type:
            options["type"] = type

        self.server.js_call(self._ref, "ask", message, options)
        return await self._ask_queue.get()

    async def confirm(self, message, title=None, type=None, **kwargs):
        options = {}
        if title:
            options["title"] = title
        if type:
            options["type"] = type

        self.server.js_call(self._ref, "confirm", message, options)
        return await self._confirm_queue.get()

    async def message(self, message, title=None, type=None, **kwargs):
        options = {}
        if title:
            options["title"] = title
        if type:
            options["type"] = type

        self.server.js_call(self._ref, "message", message, options)
        return await self._message_queue.get()

    async def open(
        self,
        title,
        default_path=None,
        directory=False,
        filters=[],
        multiple=False,
        recursive=False,
        **_,
    ):
        kwargs = dict(
            title=title,
            directory=directory,
            filters=filters,
            multiple=multiple,
            recursive=recursive,
        )
        if default_path:
            kwargs["defaultPath"] = default_path

        self.server.js_call(self._ref, "open", kwargs)
        return await self._open_queue.get()

    async def save(self, title=None, default_path=None, filters=[], **kwargs):
        options = {}
        if default_path:
            options["defaultPath"] = default_path

        if title:
            options["title"] = title

        if filters:
            options["filters"] = filters

        self.server.js_call(self._ref, "save", options)
        return await self._save_queue.get()

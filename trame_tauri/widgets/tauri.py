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
    "Window",
]


class Events(HtmlElement):
    def __init__(self, listen=[], once=[], **kwargs):
        super().__init__(
            "tauri-events",
            **kwargs,
        )
        self._event_names += [(name, name.replace("_", "-")) for name in listen]
        self._event_names += [(name, name.replace("_", "-")) for name in once]
        l_names = ",".join(map(lambda n: f"'{n}'", listen))
        o_names = ",".join(map(lambda n: f"'{n}'", once))
        self._attributes["__listen"] = f':listen="[{l_names}]"'
        self._attributes["__once"] = f':once="[{o_names}]"'


class Dialog(HtmlElement):
    def __init__(self, ref="tauri_dialog", **kwargs):
        super().__init__(
            "tauri-dialog",
            **kwargs,
        )
        trigger_name = self.server.trigger_name(self._fill_queue)
        self._ref = ref
        self._attributes["ref"] = f'ref="{self._ref}"'
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


class Window(HtmlElement):
    _next_id = 0

    def __init__(self, ref=None, **kwargs):
        super().__init__(
            "tauri-window",
            **kwargs,
        )

        if ref is None:
            Window._next_id += 1
            ref = f"trame__tauri_window_{Window._next_id}"
        self.__ref = ref
        self._attributes["ref"] = f'ref="{ref}"'

        self._attr_names += [
            "main",
            "title",
            "url",
            "visible",
            "width",
            "height",
            "x",
            "y",
            "options",
            ("prevent_close", "preventClose"),
        ]
        self._event_names += [
            "created",
            "closed",
            ("file_drop", "fileDrop"),
            ("focus_changed", "focusChanged"),
            ("menu_clicked", "menuClicked"),
            "moved",
            "resized",
            ("scale_changed", "scaleChanged"),
            ("theme_changed", "themeChanged"),
        ]

    @property
    def ref_name(self):
        return self.__ref

    def center(self):
        """Center the window."""
        self.server.js_call(
            self.__ref,
            "center",
        )

    def close(self):
        """Close the window."""
        self.server.js_call(
            self.__ref,
            "close",
        )

    def show(self):
        """Show the window. Same effect as updating the 'visible' property."""
        self.server.js_call(
            self.__ref,
            "show",
        )

    def hide(self):
        """Hide the window. Same effect as updating the 'visible' property."""
        self.server.js_call(
            self.__ref,
            "hide",
        )

    def maximize(self):
        """Maximize the window"""
        self.server.js_call(
            self.__ref,
            "maximize",
        )

    def unmaximize(self):
        """Unmaximize the window"""
        self.server.js_call(
            self.__ref,
            "unmaximize",
        )

    def minimize(self):
        """Minimize the window"""
        self.server.js_call(
            self.__ref,
            "minimize",
        )

    def unminimize(self):
        """Unminimize the window"""
        self.server.js_call(
            self.__ref,
            "unminimize",
        )

    def grab_focus(self):
        """Bring focus to the window"""
        self.server.js_call(
            self.__ref,
            "grabFocus",
        )

    def set_fullscreen(self, on=True):
        """Activate or deactivate full screen mode"""
        self.server.js_call(self.__ref, "setFullscreen", on)

    def request_user_attention(self, level=None):
        """Request user attention. Level can be None/1/2.
        https://tauri.app/v1/api/js/window#userattentiontype"""
        if level is None:
            self.server.js_call(
                self.__ref,
                "requestUserAttention",
            )
        else:
            self.server.js_call(self.__ref, "requestUserAttention", level)

    def set_position(self, x, y):
        """Update window position (logical)"""
        self.server.js_call(self.__ref, "setPosition", x, y)

    def set_size(self, w, h):
        """Update window size (logical)"""
        self.server.js_call(self.__ref, "setSize", w, h)

    def set_title(self, title):
        """Update window title"""
        self.server.js_call(self.__ref, "setTitle", title)

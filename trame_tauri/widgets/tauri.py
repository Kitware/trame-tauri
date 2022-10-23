from trame_client.widgets.core import AbstractElement
from .. import module


class HtmlElement(AbstractElement):
    def __init__(self, _elem_name, children=None, **kwargs):
        super().__init__(_elem_name, children, **kwargs)
        if self.server:
            self.server.enable_module(module)


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

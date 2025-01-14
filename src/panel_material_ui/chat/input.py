import param

from ..widgets import TextAreaInput


class ChatAreaInput(TextAreaInput):
    """
    The `ChatAreaInput` allows entering any multiline string using a text input
    box, with the ability to press enter to submit the message.

    Unlike TextAreaInput, the `ChatAreaInput` defaults to auto_grow=True and
    max_rows=10, and the value is not synced to the server until the enter key
    is pressed so bind on `value_input` if you need to access the existing value.

    Lines are joined with the newline character `\\n`.

    Reference: https://panel.holoviz.org/reference/chat/ChatAreaInput.html

    :Example:

    >>> ChatAreaInput(max_rows=10)
    """

    auto_grow = param.Boolean(
        default=True,
        doc="""
        Whether the text area should automatically grow vertically to
        accommodate the current text.""",
    )

    disabled_enter = param.Boolean(
        default=False,
        doc="If True, disables sending the message by pressing the `enter_sends` key.",
    )

    enter_sends = param.Boolean(
        default=True,
        doc="If True, pressing the Enter key sends the message, if False it is sent by pressing the Ctrl+Enter.",
    )

    enter_pressed = param.Event(
        default=False,
        doc="If True, pressing the Enter key sends the message, if False it is sent by pressing the Ctrl+Enter.",
    )

    rows = param.Integer(default=1, doc="""
        Number of rows in the text input field.""")

    max_rows = param.Integer(
        default=10,
        doc="""
        When combined with auto_grow this determines the maximum number
        of rows the input area can grow.""",
    )

    resizable = param.Selector(
        default="height",
        objects=["both", "width", "height", False],
        doc="""
        Whether the layout is interactively resizable,
        and if so in which dimensions: `width`, `height`, or `both`.
        Can only be set during initialization.""",
    )

    max_length = param.Integer(default=50000, doc="""
        Max count of characters in the input field.""")

    _esm = "ChatArea.jsx"

    def _handle_msg(self, msg) -> None:
        """
        Clear value on shift enter key down.
        """
        self.value = msg
        self.param.trigger('enter_pressed')
        with param.discard_events(self):
            self.value = ""
        self.value_input = ""

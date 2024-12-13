import pytest

pytest.importorskip("playwright")

from panel_material_ui.widgets import Button, ButtonIcon

from playwright.sync_api import expect
from tests.util import serve_component, wait_until

pytestmark = pytest.mark.ui


@pytest.mark.parametrize("button_style", ["contained", "outlined", "text"])
@pytest.mark.parametrize("button_type", ["primary", "secondary", "error", "info", "success", "warning"])
def test_button_display(page, button_style, button_type):
    btn = Button(name='Click', button_style=button_style, button_type=button_type)
    serve_component(page, btn)
    button = page.locator('.button')
    expect(button).to_have_count(1)
    # TODO: this check should pass
    # button_format = page.locator(f".MuiButton-{button_style}{button_type.capitalize()}")
    # expect(button_format).to_have_count(1)


def test_button_on_click(page):
    events = []
    def cb(event):
        events.append(event)

    btn = Button(name='Click', on_click=cb)
    serve_component(page, btn)
    button = page.locator('.button')
    button.click()
    wait_until(lambda: len(events) == 1, page)


def test_button_handle_click(page):
    btn = Button(name='Click')
    assert btn.clicks == 0
    serve_component(page, btn)
    button = page.locator('.button')
    button.click()
    assert btn.clicks == 1


def test_buttonicon_display(page):
    icon = ButtonIcon()

import pytest

pytest.importorskip('playwright')

from panel_material_ui.widgets import IntSlider

from playwright.sync_api import expect
from tests.util import serve_component, wait_until

pytestmark = pytest.mark.ui


@pytest.mark.parametrize('color', ['primary', 'secondary', 'error', 'info', 'success', 'warning'])
@pytest.mark.parametrize('orientation', ["horizontal", "vertical"])
@pytest.mark.parametrize('track', ["normal", "inverted", False])
def test_int_slider_format(page, color, orientation, track):
    widget = IntSlider(value=5, start=0, end=10, step=1, color=color, orientation=orientation, track=track)
    serve_component(page, widget)

    slider = page.locator('.int-slider')
    expect(slider).to_have_count(1)

    slider_value = page.locator('.MuiTypography-root')
    assert slider_value.inner_text() == str(widget.value)

    bar_color = page.locator(f'.MuiSlider-color{color.capitalize()}')
    expect(bar_color).to_have_count(1)
    if track != "normal":
        bar_track = page.locator(f'.MuiSlider-track{str(track).capitalize()}')
        expect(bar_track).to_have_count(1)

    if orientation == "vertical":
        bar_orientation = page.locator(f'.MuiSlider-{orientation}')
        expect(bar_orientation).to_have_count(1)

import pytest

pytest.importorskip('playwright')

from panel_material_ui.widgets import AutocompleteInput, Select, RadioBoxGroup, RadioButtonGroup

from playwright.sync_api import expect
from tests.util import serve_component, wait_until

pytestmark = pytest.mark.ui


@pytest.mark.parametrize('variant', ["filled", "outlined", "standard"])
def test_autocomplete_input_format(page, variant):
    widget = AutocompleteInput(name='Autocomplete Input test', variant=variant, options=["Option 1", "Option 2", "123"])
    serve_component(page, widget)
    ai = page.locator(".autocomplete-input")
    wait_until(lambda: expect(ai).to_have_count(1), page=page, timeout=20000)
    ai_format = page.locator(f"div[variant='{variant}']")
    wait_until(lambda: expect(ai_format).to_have_count(1), page=page, timeout=20000)


@pytest.mark.parametrize('variant', ["filled", "outlined", "standard"])
def test_select_format(page, variant):
    widget = Select(name='Select test', variant=variant, options=["Option 1", "Option 2", "Option 3"])
    serve_component(page, widget)
    select = page.locator(".select")
    wait_until(lambda: expect(select).to_have_count(1), page=page)
    select_format = page.locator(f".MuiSelect-{variant}")
    expect(select_format).to_have_count(1)


@pytest.mark.parametrize('color', ["primary", "secondary", "error", "info", "success", "warning"])
@pytest.mark.parametrize('orientation', ["horizontal", "vertical"])
def test_radio_box_group_format(page, color, orientation):
    widget = RadioBoxGroup(name='RadioBoxGroup test', options=["Option 1", "Option 2", "Option 3"], color=color, orientation=orientation)
    serve_component(page, widget)
    rbg = page.locator(".radio-box-group")
    wait_until(lambda: expect(rbg).to_have_count(1), page=page)
    rbg_color = page.locator(f".MuiRadio-color{color.capitalize()}")
    expect(rbg_color).to_have_count(len(widget.options))
    if orientation == "horizontal":
        rbg_orient = page.locator(".MuiRadioGroup-row")
        expect(rbg_orient).to_have_count(1)


@pytest.mark.parametrize('color', ["primary", "secondary", "error", "info", "success", "warning"])
@pytest.mark.parametrize('orientation', ["horizontal", "vertical"])
@pytest.mark.parametrize('size', ["small", "medium", "large"])
@pytest.mark.parametrize('variant', ["text", "outlined", "contained"])
def test_radio_button_group_format(page, color, orientation, size, variant):
    widget = RadioButtonGroup(
        name='RadioButtonGroup test',
        options=["Option 1", "Option 2", "Option 3"],
        color=color,
        orientation=orientation,
        size=size,
        variant=variant,
    )
    serve_component(page, widget)
    rbg = page.locator(".radio-button-group")
    wait_until(lambda: expect(rbg).to_have_count(1), page=page)
    # group level
    rbg_color = page.locator(f".MuiButtonGroup-color{color.capitalize()}")
    rbg_orient = page.locator(f".MuiButtonGroup-{orientation}")
    rbg_variant = page.locator(f".MuiButtonGroup-{variant}")
    expect(rbg_color).to_have_count(1)
    expect(rbg_orient).to_have_count(1)
    expect(rbg_variant).to_have_count(1)

    # option level
    option_color = page.locator(f".MuiButton-color{color.capitalize()}")
    option_size = page.locator(f".MuiButton-size{size.capitalize()}")
    option_outline = page.locator(f".MuiButton-{variant}")
    expect(option_color).to_have_count(len(widget.options))
    expect(option_size).to_have_count(len(widget.options))
    expect(option_outline).to_have_count(len(widget.options))

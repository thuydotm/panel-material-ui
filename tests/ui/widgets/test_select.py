import pytest

pytest.importorskip('playwright')

from panel_material_ui.widgets import AutocompleteInput, Select

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

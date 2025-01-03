from panel_material_ui.widgets import AutocompleteInput


def test_autocomplete_reset_none(document, comm):
    widget = AutocompleteInput(options=['A', 'B', 'C'], value='B')

    model = widget.get_root(document, comm=comm)

    assert widget.value == model.data.value == 'B'

    model.data.value = None

    assert widget.value is None

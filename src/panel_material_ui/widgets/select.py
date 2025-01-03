from __future__ import annotations

import param
from panel.widgets.select import (
    SingleSelectBase as _PnSingleSelectBase,
)
from panel.widgets.select import (
    _MultiSelectBase as _PnMultiSelectBase,
)

from ..base import COLORS
from .base import MaterialWidget


class MaterialSingleSelectBase(MaterialWidget, _PnSingleSelectBase):
    value = param.String(default=None, allow_None=True)

    __abstract = True


class MaterialMultiSelectBase(MaterialWidget, _PnMultiSelectBase):
    value = param.List(default=None, allow_None=True)

    __abstract = True


class AutocompleteInput(MaterialSingleSelectBase):
    """
    The `AutocompleteInput` widget allows searching and selecting a single value
    from a list of `options`.

    It falls into the broad category of single-value, option-selection widgets
    that provide a compatible API and include the  `Select`,
    `RadioBoxGroup` and `RadioButtonGroup` widgets.

    Some missing and extra features (if any) when comparing with the corresponding
    panel AutocompleteInput widget [panel.widgets.AutocompleteInput](https://panel.holoviz.org/reference/widgets/AutocompleteInput.html):
    - Missing features: case_sensitive, min_characters, placeholder, restrict, search_strategy, value_input
    - Extra features: label, on_event, on_msg, theme, variant

    :Example:

    >>> AutocompleteInput(
    ...     label='Study', options=['Biology', 'Chemistry', 'Physics'],
    ... )
    """

    variant = param.Selector(objects=["filled", "outlined", "standard"], default="outlined")

    _esm = "Autocomplete.jsx"

    _rename = {"name": "name"}


class Select(MaterialSingleSelectBase):
    """
    The `Select` widget allows selecting a value from a list.

    It falls into the broad category of single-value, option-selection widgets
    that provide a compatible API and include the  `AutocompleteInput`,
    `RadioBoxGroup` and `RadioButtonGroup` widgets.

    Some missing and extra features (if any) when comparing with the corresponding
    panel Select widget [panel.widgets.Select](https://panel.holoviz.org/reference/widgets/Select.html):
    - Missing features: disabled_options, groups, size
    - Extra features: label, on_event, on_msg, theme, variant

    :Example:

    >>> Select(label='Study', options=['Biology', 'Chemistry', 'Physics'])
    """

    variant = param.Selector(objects=["filled", "outlined", "standard"], default="outlined")

    _esm = "Select.jsx"

    _rename = {"name": "name"}


class RadioGroup(MaterialWidget):
    color = param.Selector(default="primary", objects=COLORS)

    orientation = param.Selector(
        default="horizontal",
        objects=["horizontal", "vertical"],
        doc="""
        Button group orientation, either 'horizontal' (default) or 'vertical'.""",
    )

    _esm = "RadioGroup.jsx"

    _rename = {"name": "name"}

    __abstract = True


class RadioBoxGroup(RadioGroup, MaterialSingleSelectBase):
    """
    The `RadioBoxGroup` widget allows selecting a value from a list of options.

    It falls into the broad category of single-value, option-selection widgets
    that provide a compatible API and include the  `AutocompleteInput`,
    `Select` and `RadioButtonGroup` widgets.

    Some missing and extra features (if any) when comparing with the corresponding
    panel RadioBoxGroup widget [panel.widgets.RadioBoxGroup](https://panel.holoviz.org/reference/widgets/RadioBoxGroup.html):
    - Missing features: inline
    - Extra features: color, description, label, on_event, on_msg, orientation, theme

    :Example:

    >>> RadioBoxGroup(
    ...     label='Study', options=['Biology', 'Chemistry', 'Physics'],
    ... )
    """

    value = param.String(default=None, allow_None=True)

    _constants = {"exclusive": True}


class CheckBoxGroup(RadioGroup, MaterialMultiSelectBase):
    """
    The `CheckBoxGroup` widget allows selecting between a list of options by
    ticking the corresponding checkboxes.

    It falls into the broad category of multi-option selection widgets that
    provide a compatible API that also include the `CheckButtonGroup` widget.

    Some missing and extra features (if any) when comparing with the corresponding
    panel CheckBoxGroup widget [panel.widgets.CheckBoxGroup](https://panel.holoviz.org/reference/widgets/CheckBoxGroup.html):
    - Missing features: inline
    - Extra features: color, description, label, on_event, on_msg, orientation, theme

    :Example:

    >>> CheckBoxGroup(
    ...     name='Fruits', value=['Apple', 'Pear'], options=['Apple', 'Banana', 'Pear', 'Strawberry'],
    ... )
    """

    value = param.List(default=None, allow_None=True)

    _constants = {"exclusive": False}


class ButtonGroup(MaterialWidget):
    color = param.Selector(default="primary", objects=COLORS)

    disableElevation = param.Boolean(default=False)

    exclusive = param.Boolean(default=False)

    fullWidth = param.Boolean(default=False)

    orientation = param.Selector(
        default="horizontal",
        objects=["horizontal", "vertical"],
        doc="""
        Button group orientation, either 'horizontal' (default) or 'vertical'.""",
    )

    size = param.Selector(objects=["small", "medium", "large"], default="medium")

    width = param.Integer(default=None, doc="""""")

    _esm = "ButtonGroup.jsx"

    _rename = {"name": "name"}

    __abstract = True


class RadioButtonGroup(ButtonGroup, MaterialSingleSelectBase):
    """
    The `RadioButtonGroup` widget allows selecting from a list or dictionary
    of values using a set of toggle buttons.

    It falls into the broad category of single-value, option-selection widgets
    that provide a compatible API and include the `AutocompleteInput`, `Select`,
    and `RadioBoxGroup` widgets.

    Some missing and extra features (if any) when comparing with the corresponding
    panel RadioButtonGroup widget [panel.widgets.RadioButtonGroup](https://panel.holoviz.org/reference/widgets/RadioButtonGroup.html):
    - Missing features: button_style, button_type, description_delay
    - Extra features: color, disableElevation, exclusive, fullWidth, label, on_event, on_msg, size, theme, variant

    :Example:

    >>> RadioButtonGroup(
    ...     label='Plotting library', options=['Matplotlib', 'Bokeh', 'Plotly'],
    ... )
    """

    value = param.Parameter()

    _constants = {"exclusive": True}


class CheckButtonGroup(ButtonGroup, MaterialMultiSelectBase):
    """
    The `CheckButtonGroup` widget allows selecting from a list or dictionary
    of values using a set of toggle buttons.

    It falls into the broad category of multi-option selection widgets that
    provide a compatible API that also include the `CheckBoxGroup` widget.

    Some missing and extra features (if any) when comparing with the corresponding
    panel CheckButtonGroup widget [panel.widgets.CheckButtonGroup](https://panel.holoviz.org/reference/widgets/CheckButtonGroup.html):
    - Missing features: button_style, button_type, description_delay
    - Extra features: color, disableElevation, exclusive, fullWidth, label, on_event, on_msg, size, theme, variant

    :Example:

    >>> CheckButtonGroup(
    ...     name='Regression Models', value=['Lasso', 'Ridge'],
    ...     options=['Lasso', 'Linear', 'Ridge', 'Polynomial']
    ... )

    """
    _constants = {"exclusive": False}

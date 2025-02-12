import datetime as dt
import inspect

from itertools import chain, product
from typing import Type

import panel as pn
import param

from panel_material_ui import *
from panel_material_ui.base import MaterialComponent
from panel_material_ui.template import Page

pn.extension(defer_load=True)

pn.config.design = MaterialDesign

color = pn.widgets.ColorPicker(value='#ff0000')
dark = Checkbox(value=pn.config.theme=='dark')

design_kwargs = dict(
    dark_theme=dark,
    theme_config={'palette': {'primary': {'main': color}}},
)

def insert_at_nth_position(main_list, insert_list, n):
    # Split main_list into chunks of size n
    chunks = [main_list[i:i+n] for i in range(0, len(main_list), n)]

    # Use chain to interleave insert_list items between these chunks
    result = list(chain.from_iterable(
        [insert] + chunk
        for i, (chunk, insert) in enumerate(zip(chunks, insert_list + [None] * (len(chunks) - len(insert_list))))
    ))
    return result

i = 0

def render_variant(component, variant, **kwargs):
    global i
    i += 1

    title = f'# {component.name}'
    if not variant:
        return pn.Column(title, component(**dict(kwargs, **design_kwargs)), name=component.name)
    elif inspect.isfunction(variant):
        return variant(component, **kwargs)
    values = []
    print(component)
    for p in variant:
        if isinstance(component.param[p], param.Integer):
            values.append(list(range(10)))
        elif isinstance(component.param[p], param.Boolean):
            values.append([False, True])
        else:
            values.append(component.param[p].objects)
    combinations = product(*values)
    ndim = len(variant)
    cols = len(values[-1])
    clabels = ([''] if ndim > 1 else []) + [f'### {v}' for v in values[-1]]
    grid_items = [
        component(**dict(zip(variant, vs), **dict(kwargs, **design_kwargs)))
        for vs in combinations
    ]
    if ndim > 1:
        rlabels = [pn.pane.Markdown(f'### {v}', styles={'rotate': '270deg'}) for v in values[0]]
        grid_items = insert_at_nth_position(grid_items, rlabels, len(values[1]))
        cols += 1
    grid = pn.GridBox(*clabels+grid_items, ncols=cols)
    combo = pn.Column(pn.pane.Markdown('### ' + variant[-1], align='center', styles={'margin-left': '-10%'}), grid)
    if ndim > 1:
        combo = pn.Row(pn.pane.Markdown('### '+variant[0], align='center', styles={'rotate': '270deg', 'margin-bottom': '-10%'}), combo)
    return combo


def show_variants(component, variants=None, **kwargs):
    if not variants:
        variants = ([
            pname for pname, p in component.param.objects().items()
            if p.owner is component and isinstance(p, (param.Boolean, param.Selector))
        ],)
    return pn.FlexBox(*(
        render_variant(component, variant, **kwargs) for variant in variants),
        name=component.name
    )


def render_spec(spec, depth=0, label='main'):
    if isinstance(spec, dict):
        tabs = Tabs(*(
            (title, render_spec(subspec, depth+1, label=title)) for title, subspec in spec.items()
        ), sizing_mode='stretch_width', **design_kwargs)
    else:
        tabs = Tabs(*(
            pn.param.ParamFunction(pn.bind(show_variants, component, variants=varss, **kwargs), lazy=True, name=component.name)
            for component, varss,  kwargs in spec
        ), dynamic=True, **design_kwargs)
    pn.state.location.sync(tabs, dict(active=f'active{label}'))
    return tabs


def render_openable(component: Type[MaterialComponent], **kwargs):
    close = Button(on_click=lambda _: inst.param.update(open=False), label='Close')  # type: ignore
    inst = component(LoadingIndicator(), close)
    button = Button(on_click=lambda _: inst.param.update(open=True), label=f'Open {component.name}')
    col = pn.Column(button, inst)
    return col

spec = {
    'Layouts': {
        'ListLike': [
            (Alert, (['severity', 'variant'], ['closeable']), dict(title='Title')),
            (Card, (['outlined', 'collapsed'], ['raised', 'collapsible']), dict(objects=['A', 'B', 'C'], title='A Card', margin=10)),
            (Divider, (['orientation', 'variant'],), dict(objects=['Foo'], width=200, height=200)),
            (Paper, (['elevation'],), dict(objects=['A', 'B', 'C'], margin=10, styles={'padding': '1em'})),
        ],
        'NamedListLike': [
            (Accordion, (), dict(objects=[('A', 'Some Text'), ('B', 'More text')], margin=10, active=[1])),
            (Tabs, (['color', 'tabs_location'],), dict(objects=[('A', 'Some Text'), ('B', 'More text')], margin=10, active=1)),
        ],
        'Overlays': [
            (Backdrop, (render_openable,), {}),
            (Dialog, (render_openable,), {}),
        ]
    },
    'Indicators': {
        'Progress': [
            (LoadingIndicator, (['color',], ['variant']), dict(value=50)),
            (Progress, (['color', 'variant'],), dict(value=50))
        ]
    },
    'Pane': {
        'Text': [
            (Avatar, (['variant'],), dict(object='https://panel.holoviz.org/_static/favicon.ico')),
            (Breadcrumbs, (), dict(items=["Home", "Catalog", "Accessories"])),
            (Chip, (['color', 'variant'], ['size']), dict(object='Foo', icon='favorite')),
            (List, (), dict(items=[
                "Home",
                {"label": "Catalog", "icon": "category"},
                {"label": "Checkout", "icon": "shopping_cart"},
                '---',
                {"label": "Accessories", "avatar": "A", "secondary": "Subtext here"},
            ])),
            (Skeleton, (), dict(width=100, height=100, margin=10)),
        ]
    },
    'Widgets': {
        'Buttons': [
            (Button, (['button_style', 'button_type'], ['disabled', 'button_style']), dict(label='Hello', icon='favorite', description='A Button')),
            (ButtonIcon, (['button_type'], ['disabled']), dict(label='Hello', icon='favorite', active_icon='rocket', description='A Button Icon')),
            (Toggle, (['button_type', 'value'], ['disabled']), dict(label='Toggle', icon='rocket', description='A toggle')),
        ],
        'Input': [
            (Checkbox, (['size', 'value'],), dict(label='I agree to the terms and conditions')),
            (DatePicker, (['color', 'variant'], ['disabled']), dict(label='DatePicker', value=dt.date(2024, 1, 1))),
            (DatetimePicker, (['color', 'variant'], ['disabled']), dict(label='DateTimePicker', value=dt.datetime(2024, 1, 1, 1, 0))),
            (FileInput, (['button_type', 'button_style'],), {}),
            (Switch, (['color', 'disabled'],), dict(label='Switch me!', value=True)),
            (TextAreaInput, (['color', 'variant'], ['disabled']), dict(label='TextAreaInput')),
            (TextInput, (['color', 'variant'], ['disabled', 'error_state']), dict(label='TextInput')),
            (ToggleIcon, (['color', 'value'],), dict(icon='favorite', active_icon='favorite-border')),
            (PasswordInput, (['color', 'variant'], ['disabled']), dict(label='PasswordInput')),
            (FloatInput, (['color', 'variant'], ['disabled']), dict(label='FloatInput', step=0.1)),
            (IntInput, (['color', 'variant'], ['disabled']), dict(label='IntInput')),
            (TimePicker, (['color', 'variant'], ['disabled', 'clock']), dict(label='TimePicker'))
        ],
        'Selection': [
            (AutocompleteInput, (['variant'], ['disabled']), dict(value='Foo', options=['Foo', 'Bar', 'Baz'], label='Autocomplete')),
            (CheckBoxGroup, (['color', 'orientation'],), dict(options=['Foo', 'Bar', 'Baz'], label='CheckBoxGroup', value=['Bar'])),
            (CheckButtonGroup, (['color', 'orientation'],), dict(options=['Foo', 'Bar', 'Baz'], label='CheckButtonGroup', value=['Foo', 'Bar'])),
            (RadioBoxGroup, (['color', 'orientation'],), dict(options=['Foo', 'Bar', 'Baz'], label='RadioBoxGroup', value='Foo')),
            (RadioButtonGroup, (['color', 'button_style'], ['size'], ['orientation']), dict(options=['Foo', 'Bar', 'Baz'], label='RadioButtonGroup', value='Foo')),
            (Select, (['variant', 'disabled'],), dict(value='Foo', options=['Foo', 'Bar', 'Baz'], label='Select')),
        ],
        'Sliders': [
            (FloatSlider, (['color', 'track'], ['disabled']), dict(start=0, end=7.2, value=3.14, label='FloatSlider')),
            (IntSlider, (['color', 'track'], ['disabled']), dict(start=0, end=10, value=5, label='IntSlider')),
            (IntRangeSlider, (['color', 'track'], ['disabled']), dict(start=0, end=10, value=(5, 7), label='IntRangeSlider')),
            (RangeSlider, (['color', 'track'], ['disabled']), dict(start=0, end=3.14, value=(0.1, 0.7), label='RangeSlider')),
            (Rating, [], dict(start=0, end=10, value=4))
        ]
    },
}

Page(header=[color, dark], main=[render_spec(spec)], sidebar=['# Foo'], title='panel-material-ui components', **design_kwargs).servable()

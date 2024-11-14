import param

from ..layout.base import COLORS, MaterialListLike


class AppBar(MaterialListLike):
    """
    AppBar
    """

    color = param.Selector(objects=COLORS, default="primary")

    logo = param.String(default=None)

    title = param.String(default="")

    position = param.Selector(default="static", objects=["fixed", "static", "sticky"])

    _esm = "AppBar.jsx"

    _stylesheets = ['https://fonts.googleapis.com/icon?family=Material+Icons']

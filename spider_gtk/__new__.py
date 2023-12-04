from dataclasses import dataclass
import sys

from typing import Any
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import GLib, Gtk, Adw

from spider import SpiderElement, SpiderNode, render as render_tree

from .widgets import GtkBoxSpiderWidget, GtkButtonSpiderWidget, GtkSpiderNativeWidget, GtkTreeViewSpiderWidget


def create_widget(element):
    if callable(element.type):
        return element.type(**element.props)

    if isinstance(element.type, str):
        widget_class = GtkBoxSpiderWidget
        if element.type == 'button':
            widget_class = GtkButtonSpiderWidget
        elif element.type in ['vbox', 'hbox', 'box']:
            widget_class = GtkBoxSpiderWidget
        elif element.type == 'treeview':
            widget_class = GtkTreeViewSpiderWidget
        
        return widget_class(
            element=element
        )


def render_widget_from_node(node, _widgets={}):
    key = node.props.get('key')
    widget = _widgets.get(key)
    if not key in _widgets:
        widget = create_widget(node)
        _widgets[key] = widget
        created = True
    
    for prop_key in node.props:
        widget.set_attribute(prop_key, node.props[prop_key])

    for child in node.children:
        widget.upsert(render_widget_from_node(child, _widgets=_widgets))
    return widget


def render(
    element: SpiderElement = None,
    container: Gtk.Widget = None,
    _widgets={},
) -> SpiderNode:
    node = render_tree(element, _widgets=_widgets)
    widget = render_widget_from_node(node, _widgets=_widgets)
    container.set_child(widget)
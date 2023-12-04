from typing import Any
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import GLib, Gtk, Adw

from spider import Spider, SpiderNode, SpiderRenderer


class SpiderGTK(SpiderRenderer):
    spider = None
    widgets = {}

    def __init__(self, spider : Spider=None, *args: Any, **kwargs: Any) -> Any:
        super().__init__(*args, **kwargs)
        self.spider = spider

    def create_widget(self, tag, props, children) -> Spider:
        from spider_gtk.widgets import GtkBoxSpiderWidget, GtkButtonSpiderWidget, GtkSpiderNativeWidget, GtkTreeViewSpiderWidget

        widget_class = GtkSpiderNativeWidget
        if tag == 'button':
            widget_class = GtkButtonSpiderWidget
        elif tag in ['vbox', 'hbox', 'box']:
            widget_class = GtkBoxSpiderWidget
            
        elif tag == 'treeview':
            widget_class = GtkTreeViewSpiderWidget
        return widget_class(
            renderer=self,
            tag=tag,
            props=props,
            children=children
        )

    def upsert_widget(self, element):
        if isinstance(element, str):
            element = SpiderNode(
                type=Gtk.Label,
                props=dict(
                    key=element,
                    label=element
                )
            )
        tag = element.type
        props = element.props
        key = props.get('key')
        created = False
        if not key in self.widgets:
            widget = self.create_widget(tag, props, [])
            self.widgets[key] = widget
            created = True
        widget = self.widgets[key]
        for prop_key in props:
            print(f"Setting attribute {prop_key}")
            widget.set_attribute(prop_key, props[prop_key])
        return widget, created

    def render(self, node: SpiderNode, container : Gtk.Widget = None) -> Gtk.Widget:
        print("Rendering widget")
        self.node = node
        if container:
            self.container = container
        else:
            container = self.container

        widget, created = self.upsert_widget(node)
        print("Rendered widget")
        if created:
            if hasattr(container, 'add_child'):
                container.add_child(widget.widget)
            if hasattr(container, 'append'):
                container.append(widget.widget)
        if isinstance(node, SpiderNode):
            print("Rendering children")
            for child in node.props.get('children', []):
                print("Rendering child")
                child_widget, child_created = self.render(child, widget.widget)
        return widget, created

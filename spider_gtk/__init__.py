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

    def set_widget_attr(self, tag, widget, key, value):
        if tag is Gtk.Widget:
            if key == 'on_click':
                widget.connect('clicked', value)
            if key == 'text':
                widget.set_label(value)
            if key == 'name':
                widget.set_name(value)
        elif tag is str:
            setattr(widget, key, value)
        if key == 'children':
            for child in value:
                self.render(child, widget)

    def create_widget(self, tag):
        widget = Gtk.Label()
        if tag == 'button':
            widget = Gtk.Button()
        elif tag in ['vbox', 'hbox', 'box']:
            widget = Gtk.Box()
            if tag == 'vbox':
                widget.set_orientation(Gtk.Orientation.VERTICAL)
            if tag == 'hbox':
                widget.set_orientation(Gtk.Orientation.HORIZONTAL)
        else:
            widget = Gtk.Label()
        return widget

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
            widget = self.create_widget(tag)
            self.widgets[key] = widget
            created = True
        widget = self.widgets[key]
        for prop_key in props:
            if prop_key.startswith('on'):
                event_name = prop_key[3:].lower()
                callback = props[prop_key]  
                if callable(callback):
                    def on_click_callback(*args):
                        print("Executing callback")
                        callback(*args)
                    try:
                        print(f"Disconnecting {event_name}ed")
                        widget.disconnect(f'{event_name}ed')
                    except:
                        pass
                    try:
                        widget.connect(f'{event_name}ed', on_click_callback) 
                    except:
                        pass

            if prop_key == 'children':
                if isinstance(props[prop_key], str):
                    widget.set_label(props[prop_key]) 
                for child in list(props[prop_key]):
                    if isinstance(child, str):
                        widget.set_label(child) 
            else:
                self.set_widget_attr(tag, widget, prop_key, props[prop_key])
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
                container.add_child(widget)
            if hasattr(container, 'append'):
                container.append(widget)
        if isinstance(node, SpiderNode):
            print("Rendering children")
            for child in node.props.get('children', []):
                print("Rendering child")
                child_widget, child_created = self.render(child, widget)
        return widget, created

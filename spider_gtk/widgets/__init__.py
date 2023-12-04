import gi 

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk

from spider import Spider
from .. import SpiderGTK


class SpiderWidget(Gtk.Stack):
    component = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spider = Spider()
        self.spider_gtk = SpiderGTK(self.spider)
        self.spider.renderer = self.spider_gtk

    def _handle_rerender(self, event):
        self.render()

    def render(self, component=None):
        sp = self.spider
        if component:
            self.spider.add_listener(
                'rerender',
                self._handle_rerender
            )
            self.component = component
        elif self.component:
            component = self.component
        self.spider_gtk.render(
            sp.create_element(
                component,
                dict(
                    key="body"
                )
            ),
            container=self
        )


class GtkSpiderNativeWidget:
    element = None
    widget = None

    def set_widget_attr(self, key, value):
        tag = self.element.tag
        widget = self.widget
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
                self.renderer.render(child, widget)

    def set_attribute(self, prop_key, value):
        if prop_key.startswith('on'):
            event_name = prop_key[3:].lower()
            callback = self.props[prop_key]  
            if callable(callback):
                def on_click_callback(*args):
                    print("Executing callback")
                    callback(*args)
                try:
                    print(f"Disconnecting {event_name}ed")
                    self.widget.disconnect(f'{event_name}ed')
                except:
                    pass
                try:
                    self.widget.connect(f'{event_name}ed', on_click_callback) 
                except:
                    pass

        if prop_key == 'children':
            if isinstance(self.props[prop_key], str):
                self.widget.set_label(self.props[prop_key]) 
            for child in list(self.props[prop_key]):
                if isinstance(child, str):
                    self.widget.set_label(child) 
        else:
            self.set_widget_attr(prop_key, self.props[prop_key])

    def __init__(self, element=None, *args, **kwargs):
        self.element = element


class GtkBoxSpiderWidget(GtkSpiderNativeWidget):
    def __init__(self, element=None, *props, **kwargs):
        super().__init__(element=element, *props, **kwargs)
        self.widget = Gtk.Box()
        if element.type == 'vbox':
            self.widget.set_orientation(Gtk.Orientation.VERTICAL)
        if element.type == 'hbox':
            self.widget.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.widget.set_spacing(10)



class GtkButtonSpiderWidget(GtkSpiderNativeWidget):
    widget = None

    def __init__(self, element=None, *props, **kwargs):
        super().__init__(element=element, *props, **kwargs)
        self.widget = Gtk.Button() 
      
    def set_attribute(self, key, value):
        if key == 'text':
            self.widget.set_label(value)
        else:
            super().set_attribute(key, value)


class GtkTreeViewSpiderNativeWidget(GtkSpiderNativeWidget):
    widget = None

    def __init__(self, element=None, *props, **kwargs):
        super().__init__(element=element, *props, **kwargs)
        self.widget = Gtk.Label()
        self.widget.set_text(element.children)

    def set_attribute(self, key, value):
        super().set_attribute(key, value)
        if key == 'text':
            self.widget.set_text(value)
        else:
            super().set_attribute(key, value)


class GtkTreeViewSpiderWidget(GtkSpiderNativeWidget):
    widget = None

    def __init__(self, element=None, *props, **kwargs):
        super().__init__(element=element, *props, **kwargs)
        self.widget = Gtk.TreeView()
        self.widget.set_model(Gtk.ListStore(str))

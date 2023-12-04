import os
import gi

from spider import use_state

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')


from gi.repository import GLib, Gtk, Adw

from spider_gtk.widgets import SpiderWidget

from spider import create_element, use_state


class SpiderExampleWindow(Gtk.Window):
    __gtype_name__ = "MainWindow"
 
    def __init__(self, *args, **kwargs):
        Gtk.ApplicationWindow.__init__(self, **kwargs)
        self.spider_widget = SpiderWidget()
        self.set_child(
            self.spider_widget
        )
        self.spider_widget.render(hello_world)
       

class SpiderExampleApplication(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        GLib.set_application_name('Spider Example')

    def do_activate(self):
        window = SpiderExampleWindow(application=self, title="Spider Example")
        window.present()


def hello_world(**props):
    [get_clicks, set_clicks] = use_state(0)

    def handle_click(event):
        print("props.key = " + props.get('key'))
        print(f"clicks: {get_clicks()}")
        set_clicks(get_clicks() + 1)
        print("Handle click")

    return create_element(
        'vbox',
        dict(
            key="vbox"
        ),
        create_element(
            'button',
            dict(
                on_click=handle_click,
                key="button_1",
            ),
            f"Clicks {get_clicks()}"
        ),
        create_element(
            'label',
            dict(
                key="label_2"
            ),
            f"You clicked {get_clicks()}"
        )
    )

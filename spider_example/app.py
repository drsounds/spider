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
    [clicks, set_clicks] = use_state(0)
    [clicks_2, set_clicks_2] = use_state(2)
    print(f"Clicks {clicks}")
    def handle_click(event):
        set_clicks(clicks + 1)
        print("Handle click")
        
    def handle_click_2(event):
        set_clicks_2(clicks_2 + 1)
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
            f"Clicks {clicks}"
        ),
        create_element(
            'button',
            dict(
                on_click=handle_click_2,
                key="button_2",
            ),
            f"Clicks 2 {clicks_2}"
        )
    )

import gi 

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk

from spider import Spider
from spider_gtk import SpiderGTK


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
                    key="text"
                ),
                "Hello World!"
            ),
            container=self
        )

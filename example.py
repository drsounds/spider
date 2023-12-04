import gi 

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gio

from spider_example.app import SpiderExampleApplication


if __name__ == '__main__':    
    app = SpiderExampleApplication(application_id='se.buddhaflow.Space')
    app.run(None)
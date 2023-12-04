from dataclasses import dataclass
import sys


class Listener:
    action = None
    callback = None

    def __init__(
        self,
        action,
        callback
    ):
        self.action = action
        self.callback = callback


class EventArgs:
    data = None
    sender = None

    def __init__(
        self,
        sender=None,
        data=None
    ):
        self.sender = sender
        self.data = data


class Observable:
    listeners = []

    def notify(self, action : str, event_args: EventArgs=None):
        for listener in self.listeners:
            if listener.action == action:
                listener.callback(event_args)

    def add_listener(self, action, callback) -> Listener:
        listener = Listener(
            action=action,
            callback=callback
        )
        self.listeners.append(
            listener   
        )
        return listener


@dataclass
class SpiderElement:
    type=None,
    props={}
    children=[]

    def __init__(
        self,
        type=None,
        props={},
        children=[]
    ):
        self.type = type
        self.props = props
        self.children = children


@dataclass
class SpiderNode:
    element : SpiderElement = None
    props : dict = {}
    children : list = []


class Spider:
    states = {}
    renderer = None

    def create_element(type, props, *children):
        if isinstance(type, str):
            return SpiderNode(
                type='str',
                props=props,
                children=children
            )

        if callable(type):
            return type(**props)


    def render(
        self,
        element: SpiderElement = None,
        stack : list = []
    ) -> SpiderNode:
        elm = self.create_element(
            type=element.type,
            props=element.props,
            *element.children
        )
        stack.append(elm)
        return elm


    def use_state(self, initial_value):
        parent = sys._getframe(1)
        key = parent.f_locals.get('props', {}).get('key')
        use_state_number = parent.f_locals.get('use_state_number', 0)
        value = self.states.get(key, {}).get(f"__use_state_{use_state_number}", initial_value)

        def set_value(value):
            if not self.states[key]:
                self.states[key] = {}
            self.states[key][f"__use_state_{use_state_number}"] = value

        return [value, set_value]

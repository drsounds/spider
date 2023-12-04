from abc import ABCMeta, abstractmethod
import random
from typing import Any


class SpiderRenderer(metaclass=ABCMeta):
    node = None

    @abstractmethod
    def render(
        self,
        element=None,
        container=None
    ):
        raise NotImplemented


class SpiderNode:
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


class SpiderElementInstance:
    key = None
    state = {}
    use_state_number = 0
    rendered_element = None

    def __init__(
        self,
        key=None,
        state={}
    ):
        self.key = key
        self.state = state


def create_node_func(type) -> SpiderNode:
    def create_spider_node(**props):
        return SpiderNode(
            type=type,
            props=props
        )
    return create_spider_node


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


class ContextEventArgs(EventArgs):
    pass


class Context(Observable):
    number = 0
    value = None
    spider = None

    def set_value(self, value):
        self.value = value
        event_args = ContextEventArgs(self, value)
        self.notify('change', event_args=event_args)

    def __init__(
        self,
        spider=None,
        value=None
    ):
        self.spider = spider
        self.value = value


class Spider(Observable):
    instance = None
    node = None
    state = {}

    rendering_elements = {}
    current_rending_element : SpiderElementInstance = None
    rendered_elements = {}
    renderer : SpiderRenderer = None

    contexts = {}

    current_key = None
    state_number = 0
    
    def rerender(self):
        self.notify('rerender')

    def __init__(self, renderer=None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.renderer = renderer

    def set_state(self, key, state_id, new_value):
        elm = self.rendering_elements[key]
        old_value = elm.state.get(state_id, None)
        elm.state[state_id] = new_value
        print(f"old_value != new_value => {old_value} != {new_value}")
        elm.state[state_id] = new_value
        if old_value != new_value:
            print("Triggering re-render")
            self.rerender()

    def resolve_element_type(
        self,
        tag
    ):
        print(tag)
        if callable(tag):
            return tag
        return create_node_func(tag)

    def create_element(
        self,
        tag,
        props,
        *children
    ):
        Spider.instance = self
        type = self.resolve_element_type(tag)
        key = props.get('key')
        elm = self.rendering_elements.get(key)
        if elm:
            print("Found existing element")
        else:
            elm = SpiderElementInstance(
                key=key,
                state={}
            )
            self.rendering_elements[key] = elm
            elm.use_state_number = 0
        self.current_rendering_element = elm

        rendered_element = type(
            **props,
            children=children
        )
        self.current_rendering_element.rendered_element = rendered_element
        self.current_rendering_element.use_state_number = 0
        self.rendered_elements[key] = rendered_element
        return rendered_element

    def render(self, element):
        Spider.instance = self
        return element.render()

    def use_state(
        self,
        initial_state=None
    ): 
        elm = self.rendering_elements[self.current_rendering_element.key]

        key = elm.key
        use_state_number = elm.use_state_number
        use_state_key = f"use_state_{use_state_number}"
        print(f"Use state key {use_state_key}")
        value = elm.state.get(use_state_key, initial_state)
        print(f"Value {value}")
        if value is None:
            value = initial_state

        def set_value(
            new_value
        ):  
            print(f"Set value of key = {key}")
            self.set_state(key, use_state_key, new_value)

        elm.use_state_number += 1
        return [value, set_value]

    def create_context(
        self,
        value
    ):
        context_id = random.randint(0, 1000000)
        self.contexts[context_id] = Context(
            id=context_id,
            value=value
        )

    def on_context_change(self, elm):
        self.render(elm)  

    def use_context(
        self,
        context
    ):
        context.add_listener(
            'change',
            lambda event_args: self.on_context_change(event_args, self.current_rendering_element)
        )
        return context.value

    def create_context(self, value):
        context = Context(self, value)
        context.spider = self
        return context


def use_state(initial_state: Any) -> Any:
    return Spider.instance.use_state(initial_state)


def use_context(context: Any) -> Any:
    return Spider.instance.use_context(context)


def create_context(context: Any) -> Any:
    return Spider.instance.create_context(context)


def create_element(
    tag,
    props,
    *children
):
    return Spider.instance.create_element(
        tag,
        props,
        *children
    )

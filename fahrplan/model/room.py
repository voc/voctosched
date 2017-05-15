from .event import Event


class Room:
    def __init__(self, name: str):
        self.name = name
        self.events = dict()

    def add_event(self, event: Event):
        event.room = self.name
        self.events[event.id] = event

    def get_start(self):
        return min(event.start for event in self.events.values())

    def get_end(self):
        return max(event.end for event in self.events.values())

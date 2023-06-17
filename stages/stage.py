from abc import ABC, abstractmethod
from enum import Enum


class StageUpdateType(Enum):
    START_MENU = 1
    PAUSE = 2
    CONTINUE = 3
    RESTART = 4
    QUIT = 10


class Stage(ABC):
    def __init__(self):
        self.observers = []

    def subscribe(self, subscriber):
        self.observers.append(subscriber)

    def notify(self, new_stage):
        for observer in self.observers:
            observer(new_stage)

    @abstractmethod
    def update(self, events, key_pressed):
        pass

    @abstractmethod
    def render(self, screen):
        pass

    def start_stage(self, update_type):
        pass

    def pause(self):
        pass

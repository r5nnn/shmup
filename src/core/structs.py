"""Module containing design patterns, data structures and other utilities.

These utilities specifically have no other dependencies for the game.
"""
from __future__ import annotations

import inspect
import logging
from abc import ABC, abstractmethod
from typing import Any, Callable

log = logging.getLogger(__name__)


class Validator(ABC):
    """Descriptor abstract base class for validating when a property is set."""

    def __set_name__(self, owner: type, name: str):
        self.private_name = "_" + name

    def __get__(self, instance: object | None, owner: type | None = None):
        if instance is None:
            return self
        return getattr(instance, self.private_name)

    def __set__(self, instance: object, value: Any):
        if getattr(instance, self.private_name) == value:
            return
        self.validate(instance, value)
        setattr(instance, self.private_name, value)

    @abstractmethod
    def validate(self, instance: object, value: Any) -> None:
        pass


class Bidict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inverse = {}
        for key, value in self.items():
            self.inverse.setdefault(value, []).append(key)

    def __setitem__(self, key: Any, value: Any):
        if key in self:
            self.inverse[self[key]].remove(key)
        super().__setitem__(key, value)
        self.inverse.setdefault(value, []).append(key)

    def __delitem__(self, key: Any):
        self.inverse.setdefault(self[key], []).remove(key)
        if self[key] in self.inverse and not self.inverse[self[key]]:
            del self.inverse[self[key]]
        super().__delitem__(key)


class Printable:
    def __str__(self):
        return self.__stringify(str)

    def __repr__(self):
        return self.__stringify(repr)

    def __stringify(self, strfunc: Callable[[object], str]) -> str:
        sig = inspect.signature(self.__init__)
        values = []
        for attr in sig.parameters:
            value = getattr(self, attr)
            values.append(strfunc(value))

        clsname = type(self).__name__
        args = ", ".join(values)
        return f"{clsname}({args})"

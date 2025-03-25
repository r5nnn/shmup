"""Module containing design patterns, data structures and other utilities.

These utilities specifically have no other dependencies for the game.
"""

from __future__ import annotations

import logging
import weakref
from abc import ABC, abstractmethod
from collections import OrderedDict
from collections.abc import MutableSet
from typing import Any, override

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


# Implementation of an insertion-ordered set. Necessary to keep track of the
# order in which widgets are added.
class OrderedSet(MutableSet):
    def __init__(self, values: tuple[weakref.ReferenceType] = ()):
        self._od = OrderedDict.fromkeys(values)

    @override
    def __len__(self):
        return len(self._od)

    @override
    def __iter__(self):
        return iter(self._od)

    @override
    def __contains__(self, value: weakref.ReferenceType):
        return value in self._od

    @override
    def add(self, value: weakref.ReferenceType) -> None:
        self._od[value] = None

    @override
    def discard(self, value: weakref.ReferenceType) -> None:
        self._od.pop(value, None)

    def move_to_end(self, value: weakref.ReferenceType) -> None:
        self._od.move_to_end(value)

    def move_to_start(self, value: weakref.ReferenceType) -> None:
        self._od.move_to_end(value, last=False)


class OrderedWeakset(weakref.WeakSet):
    _remove = ...  # Getting defined after the super().__init__() call

    def __init__(self, values: tuple = ()):
        super().__init__()

        self.data = OrderedSet()
        for elem in values:
            self.add(elem)

    def move_to_end(self, item: Any) -> None:
        self.data.move_to_end(weakref.ref(item, self._remove))

    def move_to_start(self, item: Any) -> None:
        self.data.move_to_start(weakref.ref(item, self._remove))

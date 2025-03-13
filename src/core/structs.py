import logging
from abc import abstractmethod, ABC
from typing import Any


log = logging.getLogger(__name__)


class Validator(ABC):
    """Descriptor abstract base class for validating when a property is set."""

    def __set_name__(self, owner: type, name: str):
        self.private_name = "_" + name

    def __get__(self, instance: object | None, owner: type | None = None):
        if instance is None:
            return self
        log.debug(f"Getting decorated property: {self.private_name}. Value is "
                  f"{(value := getattr(instance, self.private_name))}")
        return value

    def __set__(self, instance: object, value: Any):
        if val := getattr(instance, self.private_name) == value:
            log.debug(f"Set value of decorated property: {self.private_name} "
                      f"that is equal to value it already had: {val}. Ignoring"
                      f" call.")
            return
        self.validate(instance, value)
        log.debug(f"Validated decorated property: {self.private_name}. Setting"
                  f" property as {value}.")
        setattr(instance, self.private_name, value)

    @abstractmethod
    def validate(self, instance: object, value: Any) -> None:
        pass


class Bidict(dict):
    def __init__(self, *args, **kwargs):
        super(Bidict, self).__init__(*args, **kwargs)
        self.inverse = {}
        for key, value in self.items():
            self.inverse.setdefault(value, []).append(key)

    def __setitem__(self, key, value):
        if key in self:
            self.inverse[self[key]].remove(key)
        super(Bidict, self).__setitem__(key, value)
        self.inverse.setdefault(value, []).append(key)

    def __delitem__(self, key):
        self.inverse.setdefault(self[key], []).remove(key)
        if self[key] in self.inverse and not self.inverse[self[key]]:
            del self.inverse[self[key]]
        super(Bidict, self).__delitem__(key)

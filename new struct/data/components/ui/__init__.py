from typing import override

from data.globals import Validator


class RenderNeeded(Validator):
    @override
    def _validate(self, instance, value):
        instance._requires_render = True


class RectUpdateNeeded(Validator):
    @override
    def _validate(self, instance, value):
        instance._requires_rect_update = True
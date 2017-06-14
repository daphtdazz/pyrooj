"""Holds the :class:`Roojable` class."""
from collections import namedtuple
import json
from jsonschema import validate
from numbers import Number

from .roojable_type import RoojableType
from . import proxy
from .exceptions import UnroojableObjectException


class Roojable(metaclass=RoojableType):  # noqa
    """Mixin class to provide rooj functionality to concrete classes."""

    INFINITE_DEPTH = -1

    attr_names = namedtuple(
        'RoojAttributeNames',
        ['class_', 'self']
    )('_rooj_class', '_rooj_self')

    schema = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'type': 'object',
        'properties': {
            '_rooj_class': {'type': 'string'}
        },
        'required': ['_rooj_class', '_rooj_self']
    }

    @classmethod
    def from_rooj(cls, rooj):
        if isinstance(rooj, str):
            json_obj = json.loads(rooj)
        else:
            json_obj = rooj
        validate(json_obj, cls.schema)
        rooj_class_name = json_obj[cls.attr_names.class_]
        rooj_class = RoojableType.get_roojable_class(rooj_class_name)
        return rooj_class.from_rooj_object(json_obj)

    @classmethod
    def from_rooj_object(cls, rooj_obj):

        inst = cls()
        for prop, value in rooj_obj.items():
            if prop.startswith('_rooj'):
                continue
            setattr(inst, prop, value)
        return inst

    @classmethod
    def rooj_objectify(cls, obj, depth=0, none_on_unroojable=False):
        if isinstance(obj, str) or isinstance(obj, Number):
            return obj

        if isinstance(obj, Roojable):
            if depth == 0:
                return cls.rooj_objectify_as_proxy(obj)

            if depth != cls.INFINITE_DEPTH:
                depth -= 1

            return obj.to_rooj_object(depth=depth)

        if none_on_unroojable:
            return None

        raise UnroojableObjectException(obj)

    @classmethod
    def rooj_objectify_as_proxy(cls, obj):
        prx = proxy.RoojProxy(obj)
        return prx.to_rooj_object()

    @property
    def rooj_class(self):
        return type(self).__name__

    @property
    def rooj_self(self):
        if self._rooj_parent is not None:
            return (
                self._rooj_parent.rooj_self.rstrip('/') + '/' +
                self._rooj_path_in_parent
            )
        return '/'

    def __init__(self):
        super(Roojable, self).__init__()
        self._rooj_parent = None
        self._rooj_path_in_parent = None

    def rooj_maybe_adopt_child(self, child, path):
        if not isinstance(child, Roojable):
            return
        if child._rooj_parent is not None:
            return

        child._rooj_parent = self
        child._rooj_path_in_parent = path

    def to_rooj(self):
        return json.dumps(self.to_rooj_object())

    def to_rooj_object(self, depth=0):

        self_repr = {}

        for attr in dir(self):

            if attr.startswith('_'):
                continue

            if attr.isupper():
                continue

            if attr.startswith('rooj'):
                key = '_' + attr
            else:
                key = attr

            val = getattr(self, attr)
            self.rooj_maybe_adopt_child(val, attr)

            rooj = self.rooj_objectify(
                val, depth=depth, none_on_unroojable=True
            )
            if rooj is None:
                continue
            self_repr[key] = rooj
        return self_repr

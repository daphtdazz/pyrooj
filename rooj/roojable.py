"""Holds the :class:`Roojable` class."""
from collections import namedtuple
import json
from jsonschema import validate
from numbers import Number

from .roojable_type import RoojableType
from .exceptions import UnroojableObjectException


class Roojable(metaclass=RoojableType):  # noqa
    """Mixin class to provide rooj functionality to concrete classes."""

    attr_names = namedtuple(
        'RoojAttributeNames',
        ['class_']
    )('_rooj_class')

    schema = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'type': 'object',
        'properties': {
            '_rooj_class': {'type': 'string'}
        },
        'required': ['_rooj_class']
    }

    @classmethod
    def from_rooj(cls, rooj):
        json_obj = json.loads(rooj)
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
    def rooj_represent_object(cls, obj, none_on_unroojable=False):
        if isinstance(obj, str) or isinstance(obj, Number):
            return obj

        if none_on_unroojable:
            return None

        raise UnroojableObjectException(obj)

    def to_rooj(self):

        self_repr = {}
        self_repr['_rooj_class'] = type(self).__name__

        for attr in dir(self):
            if attr.startswith('_'):
                continue

            rooj = self.rooj_represent_object(
                getattr(self, attr), none_on_unroojable=True
            )
            if rooj is None:
                continue
            self_repr[attr] = rooj

        return json.dumps(self_repr)

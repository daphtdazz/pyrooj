"""Holds the :class:`Roojable` class."""
from collections import namedtuple
import json
from jsonschema import validate

from .roojable_type import RoojableType


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

    def to_rooj(self):

        self_repr = {}
        self_repr[self.attr_names.class_] = type(self).__name__

        return json.dumps(self_repr)

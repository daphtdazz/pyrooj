import json

from jsonschema import ValidationError
from pytest import raises

from rooj import Roojable, UnroojableObjectException


class ARoojable(Roojable):
    def __eq__(self, other):
        return self.__dict__ == other.__dict__


def test_roojify_simplest_class():
    ar = ARoojable()
    ar.a = 5
    ar.b = 'This has a " double quote in it'
    rooj = ar.to_rooj()
    assert json.loads(rooj) == {
        "_rooj_class": "ARoojable",
        '_rooj_self': '/',
        "a": 5,
        "b": 'This has a " double quote in it'
    }

    ar2 = Roojable.from_rooj(rooj)
    assert ar2.a == ar.a
    assert ar2 == ar

    rooj_object = ar2.to_rooj_object()
    ar3 = Roojable.from_rooj(rooj_object)
    assert ar2 == ar3


def test_rooj_represent_unroojable():
    with raises(UnroojableObjectException):
        Roojable.rooj_objectify(test_rooj_represent_unroojable)


def test_bad_rooj():
    for invalid_rooj in [
        '{}',
        '{"_rooj_class": 2}',
        '{"_rooj_class": {}}'
    ]:
        with raises(ValidationError):
            Roojable.from_rooj(invalid_rooj)


def test_rooj_nested_object():
    ar = ARoojable()
    ar2 = ARoojable()
    ar.ar2_attribute = ar2

    rooj_object = ar.to_rooj_object()
    assert rooj_object == {
        '_rooj_class': 'ARoojable',
        '_rooj_self': '/',
        'ar2_attribute': {
            '_rooj_class': 'RoojProxy',
            '_rooj_self': '/ar2_attribute',
            'proxied_class': 'ARoojable'
        }
    }

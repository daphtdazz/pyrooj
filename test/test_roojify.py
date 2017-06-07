import json

from jsonschema import ValidationError
from pytest import raises

from rooj import Roojable


class ARoojable(Roojable):
    def __eq__(self, other):
        return self.__dict__ == other.__dict__


def test_roojify_simplest_class():
    ar = ARoojable()
    assert json.loads(ar.to_rooj()) == {
        "_rooj_class": "ARoojable"
    }

    assert Roojable.from_rooj(ar.to_rooj()) == ar


def test_bad_rooj():
    for invalid_rooj in [
        '{}',
        '{"_rooj_class": 2}',
        '{"_rooj_class": {}}'
    ]:
        with raises(ValidationError):
            Roojable.from_rooj(invalid_rooj)

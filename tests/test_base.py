# -*- coding: utf-8 -*-

import pytest

from datafilter import Text
from datafilter.base import Base


class InvalidBase(Base):
    """
    An invalid base class.
    """

    pass


class InvalidBaseNoPropertyDecorator(Base):
    """
    An invalid base class with no property decorator on the `results` method.
    """

    def results(self):
        pass


class ValidBase(Base):
    """
    A valid base class.
    """

    @property
    def results(self):
        pass


def test_instantiation_with_invalid_base():
    with pytest.raises(TypeError) as exc_info:
        InvalidBase()

    assert exc_info.match(
        "Can't instantiate abstract class InvalidBase with abstract methods results"
    )


def test_instantiation_with_invalid_base_no_property_decorator():
    with pytest.raises(TypeError) as exc_info:
        InvalidBaseNoPropertyDecorator(tokens=["Lorem"])

    assert exc_info.match('"results" must be a property.')


def test_makelower():
    data = "Lorem ipsum"
    obj = ValidBase(tokens=["Lorem"])
    assert obj.makelower(data) == "lorem ipsum"


def test_makelower_caseinsensitive_true():
    data = "Lorem ipsum"
    obj = ValidBase(tokens=["Lorem"], caseinsensitive=True)
    assert obj.makelower(data) == "lorem ipsum"


def test_makelower_caseinsensitive_false():
    data = "Lorem ipsum"
    obj = ValidBase(tokens=["Lorem"], caseinsensitive=False)
    assert obj.makelower(data) == "Lorem ipsum"


def test_maketrans():
    obj = ValidBase(tokens=["Lorem"], translations=["test"])
    z = "".join(obj.translations)
    assert obj.maketrans() == str.maketrans("", "", z)


def test_normalize():
    data = ["Lorem", "Ipsum"]
    obj = ValidBase(tokens=["Lorem"])
    results = obj.normalize(data)
    assert next(results) == {"original": "Lorem", "normalized": "lorem"}
    assert next(results) == {"original": "Ipsum", "normalized": "ipsum"}


def test_normalize_bidirectional_true():
    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit"
    obj = Text(text, tokens=["tile"], bidirectional=True)
    assert next(obj.results)["describe"]["tokens"]["count"] == 1


def test_normalize_bidirectional_false():
    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit"
    data = Text(text, tokens=["tile"], bidirectional=False)
    assert next(data.results)["describe"]["tokens"]["count"] == 0


def test_parse_flagged_false():
    obj = ValidBase(tokens=["Dolor"])
    data = obj.normalize(["Lorem ipsum"])
    assert obj.parse(next(data))["flagged"] is False


def test_parse_flagged_true():
    obj = ValidBase(tokens=["Lorem"])
    data = obj.normalize(["Lorem ipsum"])
    assert obj.parse(next(data))["flagged"] is True


def test_parse_return():
    obj = ValidBase(tokens=["Lorem"])
    data = obj.normalize(["Lorem ipsum"])
    assert obj.parse(next(data)) == {
        "data": "Lorem ipsum",
        "flagged": True,
        "describe": {
            "tokens": {"detected": ["Lorem"], "count": 1, "frequency": {"Lorem": 1}}
        },
    }

# -*- coding: utf-8 -*-

import pytest

from datafilter.base import Base


class InvalidBase(Base):
    """
    An invalid base class.
    """

    pass


class ValidBase(Base):
    """
    A valid base class.
    """

    def results(self):
        pass


def test_instantiation_with_invalid_base():
    with pytest.raises(TypeError) as exc_info:
        InvalidBase()

    assert exc_info.match(
        "Can't instantiate abstract class InvalidBase with abstract methods results"
    )


def test_makelower_caseinsensitive_true():
    data = "Lorem ipsum"
    obj = ValidBase(tokens=["Lorem"], caseinsensitive=True)
    _, results = obj.normalize(data)
    assert results == "lorem ipsum"


def test_makelower_caseinsensitive_false():
    data = "Lorem ipsum"
    obj = ValidBase(tokens=["Lorem"], caseinsensitive=False)
    _, results = obj.normalize(data)
    assert data == results


def test_maketrans():
    obj = ValidBase(tokens=["Lorem"], translations=["test"])
    z = "".join(obj.translations)
    assert obj.maketrans() == str.maketrans("", "", z)
    assert obj.trans == str.maketrans("", "", z)


def test_normalize():
    data = ["Lorem", "Ipsum"]
    obj = ValidBase(tokens=["Lorem"])
    assert obj.normalize(data) == (["Lorem", "Ipsum"], "lorem ipsum")


def test_normalize_bidirectional_true():
    data = "Lorem ipsum dolor sit amet, consectetur adipiscing elit"
    obj = ValidBase(tokens=["tile"], bidirectional=True)
    results = obj.parse(data)
    assert results["describe"]["tokens"]["count"] == 1


def test_normalize_bidirectional_false():
    data = "Lorem ipsum dolor sit amet, consectetur adipiscing elit"
    obj = ValidBase(tokens=["tile"], bidirectional=False)
    results = obj.parse(data)
    assert results["describe"]["tokens"]["count"] == 0


def test_normalized_token_attribute():
    obj = ValidBase(tokens=["Lorem"])
    assert list(obj.normalized_tokens) == [("Lorem", "lorem")]


def test_parse_flagged_true():
    data = "Lorem ipsum"
    obj = ValidBase(tokens=["Lorem"])
    assert obj.parse(data)["flagged"] is True


def test_parse_flagged_false():
    data = "Lorem ipsum"
    obj = ValidBase(tokens=["Dolor"])
    assert obj.parse(data)["flagged"] is False


def test_parse_return():
    data = "Lorem ipsum"
    obj = ValidBase(tokens=["Lorem"])
    assert obj.parse(data) == {
        "data": "Lorem ipsum",
        "flagged": True,
        "describe": {
            "tokens": {"detected": ["Lorem"], "count": 1, "frequency": {"Lorem": 1}}
        },
    }


# def test_save(path):
#     obj = ValidBase(tokens=["Lorem"])
#     data = ["Lorem ipsum", "sit amet"]
#     obj = Valida

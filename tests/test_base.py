# -*- coding: utf-8 -*-

import string

import pytest

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

    expected = (
        "Can't instantiate abstract class InvalidBase with abstract methods results"
    )
    assert exc_info.match(expected)


def test_instantiation_with_invalid_base_no_property_decorator():
    with pytest.raises(TypeError) as exc_info:
        InvalidBaseNoPropertyDecorator()

    expected = '"results" must be a property.'
    assert exc_info.match(expected)


def test_translations():
    expected = [string.punctuation, string.whitespace, string.digits]
    assert Base.TRANSLATIONS == expected


def test_translations_type():
    with pytest.raises(ValueError) as exc_info:
        ValidBase(translations="")

    expected = '"translations must be a list.'
    exc_info.match(expected)


def test_translations_values():
    with pytest.raises(ValueError) as exc_info:
        ValidBase(translations=[1])

    expected = '"translations" must be a list of strings.'
    exc_info.match(expected)


def test_normalize():
    data = ["Lorem", "Ipsum"]
    obj = ValidBase()
    results = obj.normalize(data)
    expected = {"original": "Lorem", "normalized": "lorem"}
    assert next(results) == expected
    expected = {"original": "Ipsum", "normalized": "ipsum"}
    assert next(results) == expected


def test_makelower():
    data = "Lorem ipsum"
    obj = ValidBase()
    expected = "lorem ipsum"
    assert obj.makelower(data) == expected


def test_casesensitive_false():
    data = "Lorem ipsum"
    obj = ValidBase(casesensitive=False)
    expected = "lorem ipsum"
    assert obj.makelower(data) == expected


def test_casesensitive_true():
    data = "Lorem ipsum"
    obj = ValidBase(casesensitive=True)
    expected = "Lorem ipsum"
    assert obj.makelower(data) == expected


def test_maketrans():
    obj = ValidBase(translations=["test"])
    z = "".join(obj.translations)
    expected = str.maketrans("", "", z)
    assert obj.maketrans() == expected

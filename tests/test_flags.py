# -*- coding: utf-8 -*-

import pytest

from datafilter.flags import Flag


def test_tokens_type():
    with pytest.raises(TypeError) as exc_info:
        Flag(tokens="")

    expected = '"tokens" must be a list.'
    exc_info.match(expected)


def test_tokens_values():
    with pytest.raises(ValueError) as exc_info:
        Flag(tokens=[1])

    expected = '"tokens" must be a list of strings.'
    exc_info.match(expected)


def test_results():
    obj = Flag(tokens=["Lorem", "Lorem ipsum"])
    results = obj.results
    expected = {"original": "Lorem", "normalized": "lorem"}
    assert next(results) == expected
    expected = {"original": "Lorem ipsum", "normalized": "loremipsum"}
    assert next(results) == expected

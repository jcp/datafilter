# -*- coding: utf-8 -*-

import os

import pytest

from datafilter.filters import CSV, Filter, Text, TextFile
from datafilter.flags import Flag


class InvalidFilter(Filter):
    """
    An invalid filter
    """

    pass


class ValidFilter(Filter):
    """
    A valid filter
    """

    @property
    def results(self):
        return True


def test_normalize_and_process_abstractmethod_required():
    with pytest.raises(TypeError) as exc_info:
        InvalidFilter()

    expected = (
        "Can't instantiate abstract class InvalidFilter with "
        "abstract methods results"
    )
    assert exc_info.match(expected)


def test_flags_type():
    with pytest.raises(ValueError) as exc_info:
        ValidFilter(flags=[1])

    expected = '"flags" must be a list of Flag objects.'
    exc_info.match(expected)


def test_get_flags():
    words = Flag(tokens=["Lorem"])
    phrases = Flag(tokens=["Lorem ipsum"])
    obj = ValidFilter(flags=[words, phrases])
    results = obj.get_flags()
    expected = {"original": "Lorem", "normalized": "lorem"}
    assert next(results) == expected
    expected = {"original": "Lorem ipsum", "normalized": "loremipsum"}
    assert next(results) == expected


def test_parse_not_flagged():
    words = Flag(tokens=["Dolor"])
    obj = ValidFilter(flags=[words])
    data = obj.normalize(["Lorem ipsum"])
    expected = False
    assert obj.parse(next(data))["flagged"] == expected


def test_parse_flagged():
    words = Flag(tokens=["Lorem"])
    obj = ValidFilter(flags=[words])
    data = obj.normalize(["Lorem ipsum"])
    expected = True
    assert obj.parse(next(data))["flagged"] == expected


def test_parse_return_structure():
    words = Flag(tokens=["Lorem"])
    obj = ValidFilter(flags=[words])
    data = obj.normalize(["Lorem ipsum"])
    expected = {
        "data": "Lorem ipsum",
        "flagged": True,
        "describe": {
            "flags": {"detected": ["Lorem"], "count": 1, "frequency": {"Lorem": 1}}
        },
    }
    assert obj.parse(next(data)) == expected


def test_process_and_bidirectional_true():
    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit"
    words = Flag(tokens=["tile"])
    f = Text(text, flags=[words], bidirectional=True)
    expected = 1
    assert next(f.results)["describe"]["flags"]["count"] == expected


def test_process_and_bidirectional_false():
    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit"
    words = Flag(tokens=["tile"])
    f = Text(text, flags=[words], bidirectional=False)
    expected = 0
    assert next(f.results)["describe"]["flags"]["count"] == expected


def test_csv_path_does_not_exist():
    with pytest.raises(ValueError) as exc_info:
        words = Flag(tokens=["Lorem"])
        CSV("invalid.csv", flags=[words])

    expected = "File does not exist: invalid.csv."
    exc_info.match(expected)


def test_csv_read_csv():
    path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(path, "assets/example.csv")
    words = Flag(tokens=["lorem"])

    with open(filepath, newline="") as stream:
        f = CSV(path=filepath, flags=[words])
        reader = f.read_csv(stream=stream)
        expected = "Lorem ipsum dolor sit amet"
        assert next(reader)[0].startswith(expected)


def test_csv_results():
    path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(path, "assets/example.csv")
    words = Flag(tokens=["lorem"])
    phrases = Flag(tokens=["sit amet"])
    f = CSV(filepath, flags=[words, phrases])
    flagged = []
    counts = []

    for i in f.results:
        flagged.append(i["flagged"])
        counts.append(i["describe"]["flags"]["count"])

    expected = [True, False, False, True, False]
    assert flagged == expected
    expected = [2, 0, 0, 1, 0]
    assert counts == expected


def test_text_text_type():
    with pytest.raises(TypeError) as exc_info:
        words = Flag(tokens=["Lorem"])
        Text(text=1, flags=[words])

    expected = '"text" must be a string.'
    exc_info.match(expected)


def test_text_results():
    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit"
    words = Flag(tokens=["Lorem"])
    f = Text(text=text, flags=[words])
    expected = 1
    assert next(f.results)["describe"]["flags"]["count"] == expected


def test_text_results_re_split():
    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit"
    words = Flag(tokens=["Lorem"])
    f = Text(text=text, flags=[words], re_split=r"\s+")
    expected = len(text.split(" "))
    assert sum(1 for _ in f.results) == expected


def test_textfile_path_does_not_exist():
    with pytest.raises(ValueError) as exc_info:
        words = Flag(tokens=["Lorem"])
        TextFile("invalid.csv", flags=[words])

    expected = "File does not exist: invalid.csv."
    exc_info.match(expected)


def test_textfile_results():
    path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(path, "assets/example.txt")
    words = Flag(tokens=["lorem"])
    phrases = Flag(tokens=["sit amet"])
    f = TextFile(filepath, flags=[words, phrases])
    expected = 2
    assert next(f.results)["describe"]["flags"]["count"] == expected


def test_textfile_results_re_split():
    path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(path, "assets/example.txt")
    words = Flag(tokens=["nation"])
    f = TextFile(filepath, flags=[words], re_split=r"(?<!^)\s*[.\n]+\s*(?!$)")
    expected = 5
    assert sum(1 for _ in f.results) == expected

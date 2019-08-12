# -*- coding: utf-8 -*-

import os

import pytest

from datafilter import CSV, Text, TextFile


def test_csv_path_value_error():
    with pytest.raises(ValueError) as exc_info:
        CSV("invalid.csv", tokens=["Lorem"])

    exc_info.match("File does not exist: invalid.csv.")


def test_csv_read_csv():
    path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(path, "assets/example.csv")

    with open(filepath, newline="") as stream:
        data = CSV(path=filepath, tokens=["Lorem"])
        reader = data.read_csv(stream=stream)
        assert next(reader)[0].startswith("Lorem ipsum dolor")


def test_csv_results():
    path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(path, "assets/example.csv")
    data = CSV(filepath, tokens=["Lorem", "sit amet"])
    flagged = []
    counts = []

    for i in data.results:
        flagged.append(i["flagged"])
        counts.append(i["describe"]["tokens"]["count"])

    assert flagged == [True, False, False, True, False]
    assert counts == [2, 0, 0, 1, 0]


def test_text_text_type_error():
    with pytest.raises(TypeError) as exc_info:
        Text(text=1, tokens=["Lorem"])

    exc_info.match('"text" must be a string.')


def test_text_results():
    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit"
    data = Text(text=text, tokens=["Lorem"])
    assert next(data.results)["describe"]["tokens"]["count"] == 1


def test_text_results_re_split():
    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit"
    data = Text(text=text, tokens=["Lorem"], re_split=r"\s+")
    assert sum(1 for _ in data.results) == len(text.split(" "))


def test_textfile_path_value_error():
    with pytest.raises(ValueError) as exc_info:
        TextFile("invalid.csv", tokens=["Lorem"])

    exc_info.match("File does not exist: invalid.csv.")


def test_textfile_results():
    path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(path, "assets/example.txt")
    data = TextFile(filepath, tokens=["lorem", "sit amet"])
    assert next(data.results)["describe"]["tokens"]["count"] == 2


def test_textfile_results_re_split():
    path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(path, "assets/example.txt")
    data = TextFile(filepath, tokens=["Lorem"], re_split=r"(?<!^)\s*[.\n]+\s*(?!$)")
    assert sum(1 for _ in data.results) == 5

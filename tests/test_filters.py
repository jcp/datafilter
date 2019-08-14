# -*- coding: utf-8 -*-

import os

import pytest

from datafilter import CSV, Text, TextFile


def test_csv_results():
    path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(path, "assets/example.csv")
    obj = CSV(filepath, tokens=["Lorem", "sit amet"])
    assert [x["flagged"] for x in obj.results()] == [True, False, False, True, False]
    assert sum([x["describe"]["tokens"]["count"] for x in obj.results()]) == 3


def test_csv_save(tmpdir):
    tmp = tmpdir.mkdir("tmp")
    tmpfile = f"{tmp}/example.csv"
    tokens = ["Lorem", "sit amet"]
    path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(path, "assets/example.csv")
    obj = CSV(filepath, tokens=["Lorem", "sit amet"])
    obj.save(tmpfile)
    tmp_obj = CSV(tmpfile, tokens=tokens)
    assert [x["flagged"] for x in tmp_obj.results()] == [False, False, False]


def test_text_type_error():
    with pytest.raises(TypeError) as exc_info:
        Text(text=1, tokens=["Lorem"])

    exc_info.match('"text" must be a string.')


def test_text_results():
    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit"
    obj = Text(text, tokens=["Lorem"])
    assert next(obj.results())["describe"]["tokens"]["count"] == 1


def test_text_results_re_split():
    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit"
    obj = Text(text, tokens=["Lorem"], re_split=r"\s+")
    assert sum(1 for _ in obj.results()) == len(text.split(" "))


def test_text_save(tmpdir):
    tmp = tmpdir.mkdir("tmp")
    tmpfile = f"{tmp}/example.txt"
    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit"
    obj = Text(text, tokens=["Lorem"], re_split=r"\s+")
    obj.save(tmpfile)

    with open(tmpfile, newline="") as f:
        text = f.readlines()
        assert text[0].startswith("ipsum dolor sit")


def test_textfile_results():
    path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(path, "assets/example.txt")
    obj = TextFile(filepath, tokens=["lorem", "sit amet"])
    assert next(obj.results())["describe"]["tokens"]["count"] == 2


def test_textfile_results_re_split():
    path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(path, "assets/example.txt")
    obj = TextFile(filepath, tokens=["Lorem"], re_split=r"(?<!^)\s*[.\n]+\s*(?!$)")
    assert sum(1 for _ in obj.results()) == 5


def test_textfile_save(tmpdir):
    tmp = tmpdir.mkdir("tmp")
    tmpfile = f"{tmp}/example.txt"
    tokens = ["Lorem", "sit amet"]
    path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(path, "assets/example.txt")
    obj = TextFile(filepath, tokens=tokens, re_split=r"\s+")
    obj.save(tmpfile)

    with open(tmpfile, newline="") as f:
        text = f.readlines()
        assert text[0].startswith("ipsum dolor sit")

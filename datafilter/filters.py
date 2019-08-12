# -*- coding: utf-8 -*-

import csv
import os
import re
from typing import Dict, Iterator, List, Optional, TextIO, Union

from .base import Base


class CSV(Base):
    """
    A CSV filter.
    """

    def __init__(
        self,
        path: str,
        tokens: List[str],
        translations: Optional[List[str]] = None,
        bidirectional: bool = True,
        caseinsensitive: bool = True,
    ) -> None:
        super().__init__(tokens, translations, bidirectional, caseinsensitive)
        self.path = path

        if not os.path.exists(self.path):
            raise ValueError(f"File does not exist: {self.path}.")

    @staticmethod
    def read_csv(stream: TextIO) -> Iterator[List[str]]:
        """
        Generator that yields CSV rows.
        """
        for row in csv.reader(stream):
            yield row

    @property
    def results(self) -> Iterator[Dict[int, Dict[str, Union[List[str], str, bool]]]]:
        """
        Generator that yields processed data.
        """
        with open(self.path, newline="") as stream:
            reader = self.read_csv(stream)
            for data in self.normalize(reader):
                yield self.parse(data)


class Text(Base):
    """
    A text filter.
    """

    def __init__(
        self,
        text: str,
        tokens: List[str],
        re_split: Optional[str] = None,
        translations: Optional[List[str]] = None,
        bidirectional: bool = True,
        caseinsensitive: bool = True,
    ) -> None:
        super().__init__(tokens, translations, bidirectional, caseinsensitive)
        self.text = text
        self.re_split = re_split

        if not isinstance(self.text, str):
            raise TypeError('"text" must be a string.')

    @property
    def results(self) -> Iterator[Dict[int, Dict[str, Union[List[str], str, bool]]]]:
        """
        Generator that yields processed data.
        """
        text = [self.text]
        if self.re_split:
            text = re.split(self.re_split, self.text)

        for data in self.normalize(text):
            yield self.parse(data)


class TextFile(Base):
    """
    A text file filter.
    """

    def __init__(
        self,
        path: str,
        tokens: List[str],
        re_split: Optional[str] = None,
        translations: Optional[List[str]] = None,
        bidirectional: bool = True,
        caseinsensitive: bool = True,
    ) -> None:
        super().__init__(tokens, translations, bidirectional, caseinsensitive)
        self.path = path
        self.re_split = re_split

        if not os.path.exists(self.path):
            raise ValueError(f"File does not exist: {self.path}.")

    @property
    def results(self) -> Iterator[Dict[int, Dict[str, Union[List[str], str, bool]]]]:
        """
        Generator that yields processed data.
        """
        with open(self.path, newline="") as buffer:
            buffer = buffer.readlines()
            if self.re_split:
                buffer = re.split(self.re_split, buffer[0])

            for data in self.normalize(buffer):
                yield self.parse(data)

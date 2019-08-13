# -*- coding: utf-8 -*-

import csv
import re
from typing import Any, Dict, Iterator, List, Optional, Union

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

        Iterator[Dict[str, Dict[str, Union[List[str], str, bool]]]]

    def results(self) -> Iterator[Dict[str, Union[List[str], bool, Dict[str, Any]]]]:
        """
        Yield processed data.
        """
        with open(self.path, newline="") as stream:
            for row in csv.reader(stream):
                yield self.parse(row)


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

    def results(self) -> Iterator[Dict[str, Union[List[str], bool, Dict[str, Any]]]]:
        """
        Yield processed data.
        """
        text = [self.text]
        if self.re_split:
            text = re.split(self.re_split, text[0])

        for data in text:
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

    def results(self) -> Iterator[Dict[str, Union[List[str], bool, Dict[str, Any]]]]:
        """
        Yield processed data.
        """
        with open(self.path, newline="") as buffer:
            buffer = buffer.readlines()
            if self.re_split:
                buffer = re.split(self.re_split, buffer[0])

            for data in buffer:
                yield self.parse(data)

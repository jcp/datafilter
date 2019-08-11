# -*- coding: utf-8 -*-

import csv
import os
import re
from itertools import chain
from typing import Any, Dict, Iterator, List, Optional, TextIO, Union

from .base import Base
from .flags import Flag


class Filter(Base):
    """
    Abstract filter class.
    """

    def __init__(
        self,
        flags: List[Flag],
        translations: Optional[List[str]] = None,
        casesensitive: bool = False,
        bidirectional: bool = True,
    ) -> None:
        super().__init__(translations, casesensitive)
        self.flags = flags
        self.bidirectional = bidirectional

        for obj in flags:
            if not isinstance(obj, Flag):
                raise ValueError('"flags" must be a list of Flag objects.')

    def get_flags(self) -> chain:
        """
        Return a generator that contains all normalized flags.
        """
        return chain(*[x.results for x in self.flags])

    def parse(self, data: Dict[str, Union[List[str], str]]) -> Dict[str, Any]:
        """
        Return parsed data.
        """
        detected = []
        frequency = {}
        do, dn = data.values()

        for flag in self.get_flags():
            fo, fn = flag.values()
            frequency.update({fo: 0})

            if fn in dn or self.bidirectional and fn in dn[::-1]:
                detected.append(fo)
                frequency[fo] = dn.count(fn)

        return {
            "data": do,
            "flagged": True if detected else False,
            "describe": {
                "flags": {
                    "detected": detected,
                    "count": len(detected),
                    "frequency": frequency,
                }
            },
        }


class CSV(Filter):
    """
    A CSV filter.
    """

    def __init__(
        self,
        path: str,
        flags: List[Flag],
        translations: Optional[List[str]] = None,
        casesensitive: bool = False,
        bidirectional: bool = True,
    ) -> None:
        super().__init__(flags, translations, casesensitive, bidirectional)
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


class Text(Filter):
    """
    A text filter.
    """

    def __init__(
        self,
        text: str,
        flags: List[Flag],
        re_split: Optional[str] = None,
        translations: Optional[List[str]] = None,
        casesensitive: bool = False,
        bidirectional: bool = True,
    ) -> None:
        super().__init__(flags, translations, casesensitive, bidirectional)
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


class TextFile(Filter):
    """
    A text file filter.
    """

    def __init__(
        self,
        path: str,
        flags: List[Flag],
        re_split: Optional[str] = None,
        translations: Optional[List[str]] = None,
        casesensitive: bool = False,
        bidirectional: bool = True,
    ) -> None:
        super().__init__(flags, translations, casesensitive, bidirectional)
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

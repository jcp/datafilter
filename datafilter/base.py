# -*- coding: utf-8 -*-

import string
from abc import ABC, abstractmethod
from typing import Dict, Iterator, List, Optional, Union


class Base(ABC):
    """
    Abstract base class for the `filters.Filter` and `flags.Flag` classes.
    """

    TRANSLATIONS: List[str] = [string.punctuation, string.whitespace, string.digits]

    def __init__(
        self, translations: Optional[List[str]] = None, casesensitive: bool = False
    ) -> None:
        self.translations = self.TRANSLATIONS if translations is None else translations
        self.casesensitive = casesensitive

        if not isinstance(type(self).results, property):
            raise TypeError('"results" must be a property.')

        if not isinstance(self.translations, list):
            raise ValueError('"translations must be a list.')

        if not all(isinstance(x, str) for x in self.translations):
            raise ValueError('"translations" must be a list of strings.')

    @property
    @abstractmethod
    def results(self):
        """
        Abstract method that is used to return processed results.
        """
        pass  # pragma: no cover

    def normalize(
        self, data: Union[List[str], Iterator[List[str]]]
    ) -> Iterator[Dict[str, Union[List[str], str]]]:
        """
        Generator that yields normalized data.
        """
        for i in data:
            val = "".join(i)
            val = val.translate(self.maketrans())
            val = self.makelower(val)
            yield {"original": i, "normalized": val}

    def makelower(self, data: str) -> str:
        """
        Return lowercase data.
        """
        if not self.casesensitive:
            data = data.lower()

        return data

    def maketrans(self) -> Dict[int, Optional[int]]:
        """
        Return translation table.
        """
        z = "".join(self.translations)
        trans = str.maketrans("", "", z)
        return trans

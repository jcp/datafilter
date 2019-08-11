# -*- coding: utf-8 -*-

import string
from abc import ABC, abstractmethod
from typing import Any, Dict, Iterator, List, Optional, Union


class Base(ABC):
    """
    Abstract base class.
    """

    TRANSLATIONS: List[str] = [string.punctuation, string.whitespace, string.digits]

    def __init__(
        self,
        tokens: List[str],
        translations: Optional[List[str]] = None,
        bidirectional: bool = True,
        caseinsensitive: bool = True,
    ) -> None:
        self.tokens = tokens
        self.translations = self.TRANSLATIONS if translations is None else translations
        self.bidirectional = bidirectional
        self.caseinsensitive = caseinsensitive

        if not isinstance(type(self).results, property):
            raise TypeError('"results" must be a property.')

        if not isinstance(self.tokens, list):
            raise TypeError('"tokens" must be a list.')

        if not all(isinstance(x, str) for x in self.tokens):
            raise ValueError('"tokens" must be a list of strings.')

        if not isinstance(self.translations, list):
            raise TypeError('"translations" must be a list.')

        if not all(isinstance(x, str) for x in self.translations):
            raise ValueError('"translations" must be a list of strings.')

    @property
    @abstractmethod
    def results(self):
        """
        Abstract method that is used to return processed results.
        """
        pass  # pragma: no cover

    def makelower(self, data: str) -> str:
        """
        Return lowercase data.
        """
        if self.caseinsensitive:
            data = data.lower()

        return data

    def maketrans(self) -> Dict[int, Optional[int]]:
        """
        Return translation table.
        """
        z = "".join(self.translations)
        trans = str.maketrans("", "", z)
        return trans

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

    def parse(self, data: Dict[str, Union[List[str], str]]) -> Dict[str, Any]:
        """
        Return parsed data.
        """
        detected = []
        frequency = {}
        do, dn = data.values()

        for token in self.normalize(self.tokens):
            to, tn = token.values()
            frequency.update({to: 0})

            if tn in dn or self.bidirectional and tn in dn[::-1]:
                detected.append(to)
                frequency[to] = dn.count(tn) + dn[::-1].count(tn)

        return {
            "data": do,
            "flagged": True if detected else False,
            "describe": {
                "tokens": {
                    "detected": detected,
                    "count": len(detected),
                    "frequency": frequency,
                }
            },
        }

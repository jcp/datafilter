# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Union

from .config import TRANSLATIONS


class Base(ABC):
    """
    Abstract base class.
    """

    def __init__(
        self,
        tokens: List[str],
        translations: Optional[List[str]] = None,
        bidirectional: bool = True,
        caseinsensitive: bool = True,
    ) -> None:
        self.tokens = tokens
        self.translations = TRANSLATIONS if translations is None else translations
        self.bidirectional = bidirectional
        self.caseinsensitive = caseinsensitive
        self.trans = self.maketrans()
        self.normalized_tokens = [self.normalize(x) for x in self.tokens]

    @abstractmethod
    def results(self):
        """
        Abstract method used to return results within a filter.
        """
        pass  # pragma: no cover

    def maketrans(self) -> Dict[int, None]:
        """
        Return translation table.
        """
        z = "".join(self.translations)
        trans = str.maketrans("", "", z)
        return trans

    def normalize(
        self, data: Union[List[str], str]
    ) -> Union[Tuple[List[str], str], Tuple[str, str]]:
        """
        Return normalized data.
        """
        sep = "" if type(data) is str else " "
        val = sep.join(data)
        val = val.translate(self.trans)
        val = val.lower() if self.caseinsensitive else val
        return data, val

    def parse(self, data: Union[List[str], str]) -> Dict[str, Any]:
        """
        Return parsed data.
        """
        detected = []
        frequency = {}
        do, dn = self.normalize(data)

        for to, tn in self.normalized_tokens:
            frequency[to] = 0

            if tn in dn or self.bidirectional and tn in dn[::-1]:
                detected.append(to)
                frequency[to] += dn.count(tn) + dn[::-1].count(tn)

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

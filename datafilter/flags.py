# -*- coding: utf-8 -*-

from typing import Dict, Iterator, List, Optional, Union

from .base import Base


class Flag(Base):
    """
    A list of tokens that will be searched for within a set of data.
    """

    def __init__(
        self,
        tokens: List[str],
        translations: Optional[List[str]] = None,
        casesensitive: bool = False,
    ) -> None:
        super().__init__(translations, casesensitive)
        self.tokens = tokens

        if not isinstance(self.tokens, list):
            raise TypeError('"tokens" must be a list.')

        if not all(isinstance(x, str) for x in self.tokens):
            raise ValueError('"tokens" must be a list of strings.')

    @property
    def results(self) -> Iterator[Dict[str, Union[List[str], str]]]:
        """
        Returns a generator that yields normalized flags.
        """
        return self.normalize(self.tokens)

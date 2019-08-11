# -*- coding: utf-8 -*-

from datafilter.filters import CSV, Text, TextFile

"""
Data Filter
~~~~~~~~~~~
Data Filter is a lightweight data cleansing tool that can be easily extended to support
different data structures or processing requirements.
:copyright: (c) 2019 James C. Palmer.
:license: BSD 3-Clause, see LICENSE.md for more details.
"""

__title__ = "Data Filter"
__description__ = "Quickly find tokens (words, phrases, etc) within your data."
__url__ = "https://github.com/jcp/datafilter"
__package_name__ = "datafilter"
__version__ = "0.2.0"
__author__ = "James C. Palmer"
__author_email__ = "me@jcp.io"
__license__ = "BSD 3-Clause"
__copyright__ = "Copyright (c) 2019 James C. Palmer"

VERSION = __version__


__all__ = ["CSV", "Text", "TextFile"]

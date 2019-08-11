# Data Filter

[![pypi](https://img.shields.io/pypi/v/datafilter.svg?color=brightgreen)](https://pypi.org/project/datafilter/)
[![pypi](https://img.shields.io/pypi/pyversions/datafilter.svg)](https://pypi.org/project/datafilter/)
[![codecov](https://codecov.io/gh/jcp/datafilter/branch/master/graph/badge.svg)](https://codecov.io/gh/jcp/datafilter/)
[![Build Status](https://travis-ci.org/jcp/datafilter.svg?branch=master)](https://travis-ci.org/jcp/datafilter/)

Quickly find flags (words, phrases, etc) within your data.

Data Filter is a lightweight [data cleansing](https://en.wikipedia.org/wiki/Data_cleansing) tool that can be easily extended to support different data structures or processing requirements. It natively supports the following:

* CSV files
* Text files
* Text strings

# Table of Contents

* [Requirements](#requirements)
* [Installation](#installation)
* [Basic Usage](#basic-usage)
* [Features](#features)
    * [Base](#base)
    * [Flag](#flag)
    * [Filter](#filter)
        * [CSV](#csv)
        * [Text](#text)
        * [TextFile](#textfile)

# Requirements

* Python 3.6+

# Installation

To install, simply use [pipenv](http://pipenv.org/) (or pip):

```bash
>>> pipenv install datafilter
```

# Basic Usage

## CSV

```python
from datafilter.filters import CSV
from datafilter.flags import Flag

words = Flag(tokens=["Lorem", "ipsum"])
phrases = Flag(tokens=["Volutpat est", "mi sit amet"])
data = CSV("test.csv", flags=[words, phrases])
```

## Text

```python
from datafilter.filters import Text
from datafilter.flags import Flag

words = Flag(tokens=["Lorem"])
text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit"
data = Text(text, flags=[words])
```

## Text File

```python
from datafilter.filters import TextFile
from datafilter.flags import Flag

words = Flag(tokens=["Lorem", "ipsum"])
data = TextFile("test.txt", flags=[words], re_split=r"(?<=\.)")
```

# Features

Data Filter was designed to be highly extensible. Common or useful flags and filters can be easily reused and shared. A few example use cases include:

* Flags that detect swear words, hate speech or unwanted names / phrases for a specific topic.
* Filters that can handle different data types such as Microsoft Word or Google Docs.
* Filters that can handle incoming data from external APIs.

## Base

Abstract base class that's subclassed by `Filter` and `Flag`.

`Base` includes several methods to ensure data is properly normalized, formatted and returned. The `results` property method is an `@abstractmethod` to enforce its use in subclasses.

### Parameters

#### translations

`type <list>`

A list of strings that will be removed during normalization.

**Default**

```python
['!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~', ' \t\n\r\x0b\x0c', '0123456789']
```

> **Note:**
>
> See, [Flag.TRANSLATIONS](https://github.com/jcp/datafilter/blob/master/datafilter/base.py#L13).

#### casesensitive

`type <bool>`

When `False`, tokens are converted to lowercase during normalization.

**Default**

```python
False
```

### Methods

#### results

Abstract method used to return processed results. This is defined by `Base` subclasses.

#### normalize

A generator that yields normalized data. Normalization includes converting data to [lowercase](#casesensitive) and [removing strings](#translations).

**Yields**

`type <dict>`

> **Note:**
>
> Normalized data is returned in the following  key/value format. While the key will always be a string, the value may be a string, list, dictionary or boolean.
>
> ```python
> {
>     "original": "",
>     "normalized": "",
> }
> ```

#### makelower

Returns lowercase data.

**Returns**

`type <str>`

#### maketrans

Returns a translation table used during normalization.

**Returns**

`type <dict>`

## Flag

`Flag` contains a list of tokens that will be searched for within a set of data. By default, tokens are normalized and case insensitive. Multiple `Flag` objects can be added to a `Filter`. 

### Parameters

`Flag` is a subclass of `Base` and inherits all parameters.

#### tokens

`type <list>`

A list of strings that will be searched for within a set of data.

### Methods

`Flag` is a subclass of `Base` and inherits all methods.

#### results

Property method that returns a generator that yields normalized flags.

**Yields**

`type <dict>`

> **Note:**
>
> See [normalize](#normalize) for data format.

## Filter

Abstract base class used to create filters.

Filters normalize, parse and format data. They accepts one or more `Flag` objects and use them to flag rows of data when a token has been detected.

`Filter` includes several attributes and methods that ensure data is properly parsed and returned. It's meant to be subclassed so you can easily create and share filters that support different data types.

### Parameters

`Filter` is a subclass of `Base` and inherits all parameters.

#### flags

`type <list>`

A list of `Flag` objects used to flag data.

#### bidirectional

`type <bool>`

When true, flag matching will be bidirectional. 

**Default**

```python
True
```

> **Note:**
>
> A common method of obfuscation is to reverse the offending string or phrase. This helps detect that.

### Methods

`Filter` is a subclass of `Base` and inherits all methods.

#### get_flags

A generator that yields normalized flags.

**Yields**

`type <dict>`

#### parse

Returns parsed and property formatted data.

**Returns**

`type <dict>`

> **Example:**
>
> Assume we're searching for the token "Lorem" in a very short string.
>
> ```python
> words = Flag(tokens=["Lorem"])
> data = Text("Lorem ipsum dolor sit amet", flags=[words])
> print(next(data.results))
> ```
>
> The returned result would be formatted as:
>
> ```python
> {
>     "data": "Lorem ipsum dolor sit amet",
>     "flagged": True,
>     "describe": {
>         "flags": {
>             "detected": ["Lorem"],
>             "count": 1,
>             "frequency": {
>                 "Lorem": 1,
>             },
>         }
>     },
> }
> ```

## CSV

### Parameters

`CSV` is a subclass of `Filter` and inherits all parameters.

#### path

`type <str>`

Path to a CSV file.

### Methods

`CSV` is a subclass of `Filter` and inherits all methods.

#### read_csv

Static method that accepts parameter `stream` of type `TextIO` and returns a generator that yields a list of CSV rows.

**Yields**

`type <list>`

## Text

### Parameters

`Text` is a subclass of `Filter` and inherits all parameters.

#### text

`type <str>`

A text string.

#### re_split

`type <str>`

A regular expression pattern or string that will be applied to `text` with `re.split` before normalization.

### Methods

`Text` is a subclass of `Filter` and inherits all methods.

## TextFile

### Parameters

`TextFile` is a subclass of `Filter` and inherits all parameters.

#### path

`type <str>`

Path to a text file.

#### re_split

`type <str>`

A regular expression pattern or string that will be applied to `text` with `re.split` before normalization.

### Methods

`TextFile` is a subclass of `Filter` and inherits all methods.
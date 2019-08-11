# Data Filter

[![pypi](https://img.shields.io/pypi/v/datafilter.svg?color=brightgreen)](https://pypi.org/project/datafilter/)
[![pypi](https://img.shields.io/pypi/pyversions/datafilter.svg)](https://pypi.org/project/datafilter/)
[![codecov](https://codecov.io/gh/jcp/datafilter/branch/master/graph/badge.svg)](https://codecov.io/gh/jcp/datafilter/)
[![Build Status](https://travis-ci.org/jcp/datafilter.svg?branch=master)](https://travis-ci.org/jcp/datafilter/)

Quickly find tokens (words, phrases, etc) within your data.

Data Filter is a lightweight [data cleansing](https://en.wikipedia.org/wiki/Data_cleansing) framework that can be easily extended to support different data types, structures or processing requirements. It natively supports the following data types:

* CSV files
* Text files
* Text strings

# Table of Contents

* [Requirements](#requirements)
* [Installation](#installation)
* [Basic Usage](#basic-usage)
* [Features](#features)
    * [Base](#base)
    * [Filters](#filters)
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

Each example below returns a generator that yields [parsed](#parse) data.

## CSV

```python
from datafilter import CSV

tokens = ["Lorem", "ipsum", "Volutpat est", "mi sit amet"]
data = CSV("test.csv", tokens=tokens)
print(next(data.results))
```

## Text

```python
from datafilter import Text

text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit"
data = Text(text, tokens=["Lorem"])
print(next(data.results))
```

## Text File

```python
from datafilter import TextFile

data = TextFile("test.txt", tokens=["Lorem", "ipsum"], re_split=r"(?<=\.)")
print(next(data.results))
```

# Features

Data Filter was designed to be highly extensible. Common or useful filters can be easily reused and shared. A few example use cases include:

* Filters that can handle different data types such as Microsoft Word, Google Docs, etc.
* Filters that can handle incoming data from external APIs.

## Base

Abstract base class that's subclassed by every filter.

`Base` includes several methods to ensure data is properly normalized, formatted and returned. The `results` property method is an `@abstractmethod` to enforce its use in subclasses.

### Parameters

#### tokens

`type <list>`

A list of strings that will be searched for within a set of data.

#### translations

`type <list>`

A list of strings that will be removed during normalization.

**Default**

```python
['!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~', ' \t\n\r\x0b\x0c', '0123456789']
```

#### bidirectional

`type <bool>`

When `True`, token matching will be bidirectional. 

**Default**

```python
True
```

> **Note:**
>
> A common obfuscation method is to reverse the offending string or phrase. This helps detect those instances.

#### caseinsensitive

`type <bool>`

When `True`, tokens and data are converted to lowercase during normalization.

**Default**

```python
True
```

### Methods

#### results

Abstract method used to return processed results. This is defined within `Base` subclasses.

#### makelower

Returns lowercase data.

**Returns**

`type <str>`

#### maketrans

Returns a translation table used during normalization.

**Returns**

`type <dict>`

#### normalize

A generator that yields normalized data. Normalization includes converting data to [lowercase](#caseinsensitive) and [removing strings](#translations).

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

#### parse

Returns parsed and property formatted data.

**Returns**

`type <dict>`

> **Example:**
>
> Assume we're searching for the token "Lorem" in a very short string.
>
> ```python
> data = Text("Lorem ipsum dolor sit amet", tokens=["Lorem"])
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
>         "tokens": {
>             "detected": ["Lorem"],
>             "count": 1,
>             "frequency": {
>                 "Lorem": 1,
>             },
>         }
>     },
> }
> ```

## Filters

Filters subclass and extend the `Base` class to support various data types and structure. This extensibility allows for the creation of powerful custom filters specifically tailored to a given task, data type or structure.

## CSV

### Parameters

`CSV` is a subclass of `Base` and inherits all parameters.

#### path

`type <str>`

Path to a CSV file.

### Methods

`CSV` is a subclass of `Base` and inherits all methods.

#### read_csv

Static method that accepts parameter `stream` of type `TextIO` and returns a generator that yields a list of CSV rows.

**Yields**

`type <list>`

## Text

### Parameters

`Text` is a subclass of `Base` and inherits all parameters.

#### text

`type <str>`

A text string.

#### re_split

`type <str>`

A regular expression pattern or string that will be applied to `text` with `re.split` before normalization.

### Methods

`Text` is a subclass of `Base` and inherits all methods.

## TextFile

### Parameters

`TextFile` is a subclass of `Base` and inherits all parameters.

#### path

`type <str>`

Path to a text file.

#### re_split

`type <str>`

A regular expression pattern or string that will be applied to `text` with `re.split` before normalization.

### Methods

`TextFile` is a subclass of `Base` and inherits all methods.
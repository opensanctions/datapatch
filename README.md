# datapatch

A Python library for defining rule-based overrides on messy data. Imagine, for example,
trying to import a dataset in each row is associated with a country - which have been 
entered by humans. You might find country names like `Northkorea`, or `Greet Britain`
that you want to normalise. `datapatch` creates a mechanism to build a flexible lookup
table (usually stored as a YAML file) to catch and repair these data issues.

## Installation

You can install `datapatch` from the Python package index:

```bash
pip install datapatch
```

## Example

Given a YAML file like this:

```yaml
countries:
  normalize: true
  lowercase: true
  asciify: true
  options:
    - match: Frankreich
      value: France
    - match:
        - Northkorea
        - Nordkorea
        - Northern Korea
        - NKorea
        - DPRK
      value: North Korea
    - contains: Britain
      value: Great Britain
```

The file can be used to apply the data patches against raw input:

```python
from datapatch import read_lookups, LookupException

lookups = read_lookups("countries.yml")
countries = lookups.get("countries")

# This will apply the patch or default to the original string if none exists:
for row in iter_data():
    raw = row.get("Country")
    row["Country"] = countries.get_value(raw, default=raw)
```

### Extended options

There's a host of options available to configure the application of the data
patches:

```yaml
countries:
  # If you mark a lookup as required, a value that matches no options will
  # throw a `datapatch.exc:LookupException`.
  required: true
  # Normalisation will remove many special characters, remove multiple spaces
  normalize: false
  # By default normalize perform transliteration across alphabets (Путин -> Putin)
  # set asciify to false if you want to keep non-ascii alphabets as is
  asciify: false
  options:
    - match: Francois
      value: France
  # This is a shorthand for defining options that have just one `match` and
  # one `value` defined:
  map:
    Luxemborg: Luxembourg
    Lux: Luxembourg
```

### Result objects

You can also have more details associated with a result and access them:

```yaml
countries:
  options:
    - match: Frankreich
      # These can be arbitrary attributes:
      label: France
      code: FR
```

This can be accessed as a result object with attributes:

```python
from datapatch import read_lookups, LookupException

lookups = read_lookups("countries.yml")
countries = lookups.get("countries")

result = countries.match("Frankreich")
print(result.label, result.code)
assert result.capital is None, result.capital
```

## License

`datapatch` is licensed under the terms of the MIT license, which is included as
`LICENSE`.
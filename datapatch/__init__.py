from os import read
from typing import Any, Dict
from datapatch.lookup import Lookup
from datapatch.util import read_yaml_file, PathLike
from datapatch.exc import LookupException


__version__ = "0.2.1"
__all__ = ["Lookup", "LookupException", "get_lookups", "read_lookups"]


def get_lookups(data: Any) -> Dict[str, Lookup]:
    """Turn a mapping of configs into a dict of Lookups."""
    lookups = {}
    for name, config in data.items():
        lookups[name] = Lookup(name, config)
    return lookups


def read_lookups(path: PathLike) -> Dict[str, Lookup]:
    """Read a set of named lookups from a JSON/YAML file."""
    data = read_yaml_file(path)
    return get_lookups(data)

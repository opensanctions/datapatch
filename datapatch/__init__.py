from os import read
from typing import Any, Dict
from datapatch.lookup import Lookup
from datapatch.result import Result
from datapatch.util import read_yaml_file, PathLike
from datapatch.exc import LookupException


__version__ = "1.2.0"
__all__ = ["Lookup", "Result", "LookupException", "get_lookups", "read_lookups"]


def get_lookups(
    data: Dict[str, Dict[str, Any]],
    debug: bool = False,
) -> Dict[str, Lookup]:
    """Turn a mapping of configs into a dict of Lookups."""
    lookups = {}
    for name, config in data.items():
        lookups[name] = Lookup(name, config, debug=debug)
    return lookups


def read_lookups(path: PathLike, debug: bool = False) -> Dict[str, Lookup]:
    """Read a set of named lookups from a JSON/YAML file."""
    data = read_yaml_file(path)
    return get_lookups(data, debug=debug)

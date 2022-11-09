from typing import Any, Dict, Iterable, List, Optional, Set
from banal import ensure_list, as_bool
from normality import stringify

from datapatch.option import Option
from datapatch.exc import LookupException
from datapatch.result import Result


class Lookup(object):
    """Lookups are ways of patching up broken input data from a source."""

    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.required = as_bool(config.pop("required", False))
        self.normalize = as_bool(config.pop("normalize", False))
        self.lowercase = as_bool(config.pop("lowercase", False))
        self.options: Set[Option] = set()
        for option in ensure_list(config.pop("options", [])):
            self.options.add(Option(self, option))
        map: Dict[str, Any] = dict(config.pop("map", {}))
        for match, value in map.items():
            option = {"match": match, "value": stringify(value)}
            self.options.add(Option(self, option))

    def match(self, value: Optional[str]) -> Optional[Result]:
        results: List[Result] = []
        for option in self.options:
            if option.matches(value):
                results.append(option.result)
        results = sorted(results, key=lambda r: r._weight, reverse=True)
        if len(results) > 1 and results[0]._weight == results[1]._weight:
            msg = "Ambiguous result: %r (set weights to fix)" % results
            raise LookupException(msg, lookup=self, value=value)
        for result in results:
            return result
        if self.required:
            raise LookupException("Missing lookup result", lookup=self, value=value)
        return None

    def get_value(self, value: Optional[str], default: Optional[str] =None) -> Optional[str]:
        res = self.match(value)
        if res is not None:
            return res.value
        return default

    def get_values(self, value: Optional[str], default: Optional[Iterable[str]]=None) -> List[str]:
        res = self.match(value)
        if res is not None:
            return res.values
        return ensure_list(default or [])

    def __repr__(self) -> str:
        return f"<Lookup({self.name!r}, {self.options!r})>"

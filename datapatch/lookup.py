from typing import List, Optional, Set
from banal import ensure_list, ensure_dict

from datapatch.option import Option
from datapatch.exc import LookupException
from datapatch.result import Result


class Lookup(object):
    """Lookups are ways of patching up broken input data from a source."""

    def __init__(self, name, config):
        self.name = name
        self.required = config.pop("required", False)
        self.normalize = config.pop("normalize", False)
        self.lowercase = config.pop("lowercase", False)
        self.options: Set[Option] = set()
        for option in ensure_list(config.pop("options", [])):
            self.options.add(Option(self, option))
        for match, value in ensure_dict(config.pop("map", {})).items():
            option = {"match": match, "value": value}
            self.options.add(Option(self, option))

    def match(self, value) -> Optional[Result]:
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

    def get_value(self, value, default=None):
        res = self.match(value)
        if res is not None:
            return res.value
        return default

    def get_values(self, value, default=None):
        res = self.match(value)
        if res is not None:
            return res.values
        return ensure_list(default)

    def __repr__(self):
        return f"<Lookup({self.name!r}, {self.options!r})>"

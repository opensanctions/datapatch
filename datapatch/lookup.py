import yaml
from normality import stringify
from banal import ensure_list, as_bool
from typing import Any, Dict, Iterable, List, Optional, Set, cast

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
        self.unmatched: Set[Optional[str]] = set()
        for option in ensure_list(config.pop("options", [])):
            self.options.add(Option(self, option))
        map: Dict[str, Any] = dict(config.pop("map", {}))
        for match, value in map.items():
            option = {"match": match, "value": stringify(value)}
            self.options.add(Option(self, option))

    def match(self, value: Optional[str]) -> Optional[Result]:
        matching: List[Option] = []
        for option in self.options:
            if option.matches(value):
                matching.append(option)
        matching = sorted(matching, key=lambda o: o.weight, reverse=True)
        if len(matching) > 1 and matching[0].weight == matching[1].weight:
            msg = "Ambiguous result: %r (set weights to fix)" % matching
            raise LookupException(msg, lookup=self, value=value)
        for option in matching:
            option.ref_count += 1
            return option.result
        self.unmatched.add(value)
        if self.required:
            raise LookupException("Missing lookup result", lookup=self, value=value)
        return None

    def get_value(
        self, value: Optional[str], default: Optional[str] = None
    ) -> Optional[str]:
        res = self.match(value)
        if res is not None:
            return res.value
        return default

    def get_values(
        self, value: Optional[str], default: Optional[Iterable[str]] = None
    ) -> List[str]:
        res = self.match(value)
        if res is not None:
            return res.values
        return ensure_list(default or [])

    def unmatched_options(self, tmpl: Dict[str, Any] = {}) -> List[Dict[str, Any]]:
        options: List[Dict[str, Any]] = []
        for match in self.unmatched:
            data = {"match": match}
            data.update(tmpl.items())
            options.append(data)
        return options

    def unmatched_yaml(self, tmpl: Dict[str, Any] = {}) -> str:
        data = {"options": self.unmatched_options(tmpl=tmpl)}
        yaml_data = yaml.dump(
            data,
            indent=2,
            encoding="utf-8",
            allow_unicode=True,
        )
        return cast(str, yaml_data.decode("utf-8"))

    def __repr__(self) -> str:
        return f"<Lookup({self.name!r}, {self.options!r})>"

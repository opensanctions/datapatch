import re
from functools import cached_property
from typing import TYPE_CHECKING, Any, Dict, List, Optional
from banal import as_bool

from datapatch.result import Result
from datapatch.util import normalize_value, str_list

if TYPE_CHECKING:
    from datapatch.lookup import Lookup


class Option(object):
    """One possible lookup rule that might match a value."""

    def __init__(self, lookup: "Lookup", config: Dict[str, Any]) -> None:
        self.lookup = lookup
        self.normalize = as_bool(config.pop("normalize", lookup.normalize))
        self.lowercase = as_bool(config.pop("lowercase", lookup.lowercase))
        self.weight = int(config.pop("weight", 0))
        _contains = [c for c in str_list(config.pop("contains", []))]
        _contains = [normalize_value(c, self.normalize, self.lowercase) for c in _contains]
        self.contains = set([c for c in _contains if c is not None])
        _match = str_list(config.pop("match", []))
        self.match = set([normalize_value(m, self.normalize, self.lowercase) for m in _match])
        regex = str_list(config.pop("regex", []))
        self.regex = [re.compile(r, re.U | re.M | re.S) for r in regex if r is not None]
        self.result = Result(self.weight, config)

    def matches(self, value: Optional[str]) -> bool:
        if isinstance(value, str):
            for regex in self.regex:
                if regex.match(value):
                    return True
        norm_value = normalize_value(value, self.normalize, self.lowercase)
        if norm_value in self.match:
            return True
        if norm_value is not None:
            for cand in self.contains:
                if cand in norm_value:
                    return True
        return False

    @cached_property
    def criteria(self) -> List[str]:
        criteria = set([str(m) for m in self.match])
        criteria.update((f"c({c})" for c in self.contains))
        criteria.update((f"r({r!r})" for r in self.regex))
        return sorted(criteria)

    def __str__(self) -> str:
        return "|".join(self.criteria)

    def __repr__(self) -> str:
        return "<Option(%r, %r)>" % (str(self), self.result)

    def __hash__(self) -> int:
        return hash(str(self))

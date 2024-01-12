import re
import copy
from typing import TYPE_CHECKING, Any, Dict, Optional, Set
from banal import as_bool
from datapatch.exc import DataPatchException

from datapatch.result import Result
from datapatch.util import normalize_value, str_list

if TYPE_CHECKING:
    from datapatch.lookup import Lookup


class Option(object):
    """One possible lookup rule that might match a value."""

    def __init__(self, lookup: "Lookup", config: Dict[str, Any]) -> None:
        self.config = copy.deepcopy(config)
        self.lookup = lookup
        self.normalize = as_bool(config.pop("normalize", lookup.normalize))
        self.lowercase = as_bool(config.pop("lowercase", lookup.lowercase))
        self.asciify = as_bool(config.pop("asciify", lookup.asciify))
        self.weight = int(config.pop("weight", 0))
        self.ref_count = 0

        self.clauses: Set[str] = set()
        _matches = str_list(config.pop("match", []))
        self.none_matches = None in _matches
        for match in _matches:
            match_norm = normalize_value(match, self.normalize, self.lowercase, self.asciify)
            if match_norm is not None:
                match_re = re.escape(match_norm)
                self.clauses.add(f"^{match_re}$")

        for contain in str_list(config.pop("contains", [])):
            contain_norm = normalize_value(contain, self.normalize, self.lowercase, self.asciify)
            if contain_norm is not None:
                contain_re = re.escape(contain_norm)
                self.clauses.add(f".*{contain_re}.*")

        for regex in str_list(config.pop("regex", [])):
            if regex is not None:
                self.clauses.add(regex)

        pattern = "(%s)" % "|".join(self.clauses)
        self.regex = re.compile(pattern, re.U | re.M | re.S)
        self.result = Result(config)

        if len(self.clauses) == 0 and not self.none_matches:
            raise DataPatchException("Cannot match: %r" % self)

    def matches(self, value: Optional[str]) -> bool:
        norm = normalize_value(value, self.normalize, self.lowercase, self.asciify)
        if norm is None:
            return self.none_matches
        if len(self.clauses) == 0:
            return False
        return self.regex.match(norm) is not None

    def __str__(self) -> str:
        return str(self.regex.pattern)

    def __repr__(self) -> str:
        return "<Option(%r, %r)>" % (self.regex.pattern, self.result)

    def __hash__(self) -> int:
        return hash(self.regex.pattern)

    def __eq__(self, other: Any) -> bool:
        return hash(self) == hash(other)

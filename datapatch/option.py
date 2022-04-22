import re
from banal import ensure_list, as_bool

from datapatch.result import Result
from datapatch.util import normalize_value


class Option(object):
    """One possible lookup rule that might match a value."""

    def __init__(self, lookup, config):
        self.lookup = lookup
        self.normalize = as_bool(config.pop("normalize", lookup.normalize))
        self.lowercase = as_bool(config.pop("lowercase", lookup.lowercase))
        self.clean = lambda x: normalize_value(x, self.normalize, self.lowercase)
        self.weight = int(config.pop("weight", 0))
        contains = ensure_list(config.pop("contains", []))
        self.contains = [self.clean(c) for c in contains]
        match = ensure_list(config.pop("match", []))
        self.match = [self.clean(m) for m in match]
        regex = ensure_list(config.pop("regex", []))
        self.regex = [re.compile(r, re.U | re.M | re.S) for r in regex]
        self.result = Result(self.weight, config)

    def matches(self, value):
        if isinstance(value, str):
            for regex in self.regex:
                if regex.match(value):
                    return True
        norm_value = self.clean(value)
        if norm_value is not None:
            for cand in self.contains:
                if cand in norm_value:
                    return True
        return norm_value in self.match

    @property
    def criteria(self):
        criteria = set([str(m) for m in self.match])
        criteria.update((f"c({c})" for c in self.contains))
        criteria.update((f"r({r!r})" for r in self.regex))
        return sorted(criteria)

    def __str__(self):
        return "|".join(self.criteria)

    def __repr__(self):
        return "<Option(%r, %r)>" % (str(self), self.result)

    def __hash__(self):
        return hash(str(self))

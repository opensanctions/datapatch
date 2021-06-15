import re
from banal import ensure_list, as_bool
from normality import normalize, stringify

from datapatch.result import Result


class Option(object):
    """One possible lookup rule that might match a value."""

    def __init__(self, lookup, config):
        self.lookup = lookup
        self.normalize = as_bool(config.pop("normalize", lookup.normalize))
        self.lowercase = as_bool(config.pop("lowercase", lookup.lowercase))
        contains = ensure_list(config.pop("contains", []))
        self.contains = [self.normalize_value(c) for c in contains]
        match = ensure_list(config.pop("match", []))
        self.match = [self.normalize_value(m) for m in match]
        regex = ensure_list(config.pop("regex", []))
        self.regex = [re.compile(r, re.U | re.M | re.S) for r in regex]
        self.result = Result(config)

    def normalize_value(self, value):
        if self.normalize:
            value = normalize(value, ascii=True, lowercase=False)
        else:
            value = stringify(value)
        if value is None:
            return
        if self.lowercase:
            value = value.lower()
        return value.strip()

    def matches(self, value):
        if isinstance(value, str):
            for regex in self.regex:
                if regex.match(value):
                    return True
        norm_value = self.normalize_value(value)
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

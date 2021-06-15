from banal import ensure_list, ensure_dict

from datapatch.option import Option
from datapatch.exc import LookupException


class Lookup(object):
    """Lookups are ways of patching up broken input data from a source."""

    def __init__(self, name, config):
        self.name = name
        self.required = config.pop("required", False)
        self.normalize = config.pop("normalize", False)
        self.lowercase = config.pop("lowercase", False)
        self.options = set()
        for option in ensure_list(config.pop("options", [])):
            self.options.add(Option(self, option))
        for match, value in ensure_dict(config.pop("map", {})).items():
            option = {"match": match, "value": value}
            self.options.add(Option(self, option))

    def match(self, value):
        results = []
        for option in self.options:
            if option.matches(value):
                results.append(option.result)
        if len(results) > 1:
            raise LookupException("Ambiguous result", lookup=self, value=value)
        for result in results:
            return result
        if self.required:
            raise LookupException("Missing lookup result", lookup=self, value=value)

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

import yaml
import copy
import logging
from normality import stringify
from banal import ensure_list, as_bool
from typing import Any, Dict, Iterable, List, Optional, Set, cast

from datapatch.option import Option
from datapatch.exc import LookupException
from datapatch.result import Result
from datapatch.util import split_options, str_list

log = logging.getLogger(__name__)


class Lookup(object):
    """Lookups are ways of patching up broken input data from a source."""

    def __init__(self, name: str, config: Dict[str, Any], debug: bool = False):
        self.name = name
        self.config = config
        self.required = as_bool(config.get("required", False))
        self.normalize = as_bool(config.get("normalize", False))
        self.lowercase = as_bool(config.get("lowercase", False))
        self.asciify = as_bool(config.get("asciify", True))
        self.options: Set[Option] = set()
        self.unmatched: Set[Optional[str]] = set()
        option_data: List[Any] = []
        for option in ensure_list(config.pop("options", [])):
            option_data.append(option)
        map: Dict[str, Any] = dict(config.pop("map", {}))
        for match, value in map.items():
            option = {"match": match, "value": stringify(value)}
            option_data.append(option)

        if debug:
            option_data = split_options(option_data)
        for option in option_data:
            self.options.add(Option(self, option))

    def match(self, value: Optional[str]) -> Optional[Result]:
        matching: List[Option] = []
        for option in self.options:
            if option.matches(value):
                matching.append(option)
        matching = sorted(matching, key=lambda o: o.weight, reverse=True)
        if len(matching) > 1 and matching[0].weight == matching[1].weight:
            msg = "Ambiguous result: %r -> %r (set weights to fix)" % (value, matching)
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
        yaml_data: bytes = yaml.dump(
            data,
            indent=2,
            encoding="utf-8",
            allow_unicode=True,
        )
        return yaml_data.decode("utf-8")

    def referenced_options(self) -> Optional[Dict[str, Any]]:
        options: Dict[str, List[Option]] = {}
        for option in self.options:
            if option.ref_count > 0:
                if option.result._id not in options:
                    options[option.result._id] = []
                options[option.result._id].append(option)
        keys = ("match", "contains", "regex")
        combined_options = []
        for _, options_ in options.items():
            config = copy.deepcopy(options_[0].config)
            for key in keys:
                config.pop(key, None)
            config = dict(match=[], contains=[], regex=[], **config)
            for opt in options_:
                for key in keys:
                    if key in opt.config:
                        config[key].extend(str_list(opt.config.get(key)))
            for key in keys:
                if len(config[key]) == 0:
                    config.pop(key)
                elif len(config[key]) == 1:
                    config[key] = config[key][0]
                else:
                    try:
                        config[key] = sorted(config[key])
                    except TypeError:
                        pass
            # print(config)
            combined_options.append(config)
        if not len(combined_options):
            return None
        config = copy.deepcopy(self.config)
        config["options"] = combined_options
        return config

    # def propose_consolidations(self) -> None:
    #     result_ids: Dict[str, List[Option]] = {}
    #     for option in self.options:
    #         if option.result._id not in result_ids:
    #             result_ids[option.result._id] = []
    #         result_ids[option.result._id].append(option)

    #     for _, options in result_ids.items():
    #         if len(options) > 1:
    #             log.warning("Duplicate result: %r" % options)

    def __repr__(self) -> str:
        return f"<Lookup({self.name!r}, {self.options!r})>"

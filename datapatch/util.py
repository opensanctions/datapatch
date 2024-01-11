import yaml
import copy
import pathlib
from banal import is_listish
from typing import List, Dict, Optional, Union, Any
from functools import lru_cache
from normality import stringify, normalize

PathLike = Union[str, pathlib.Path]


def read_yaml_file(path: PathLike) -> Any:
    with open(path, "r") as fh:
        return yaml.load(fh, Loader=yaml.SafeLoader)


def str_list(obj: Any) -> List[Optional[str]]:
    if not is_listish(obj):
        obj = [obj]
    return [stringify(o) for o in obj]


def split_options(options: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    splitted: List[Dict[str, Any]] = []
    for option in options:
        matches = str_list(option.pop("match")) if "match" in option else []
        contains = str_list(option.pop("contains")) if "contains" in option else []
        regexes = str_list(option.pop("regex")) if "regex" in option else []
        for match in matches:
            opt = copy.deepcopy(option)
            opt["match"] = match
            splitted.append(opt)
        for contain in contains:
            opt = copy.deepcopy(option)
            opt["contains"] = contain
            splitted.append(opt)
        for regex in regexes:
            opt = copy.deepcopy(option)
            opt["regex"] = regex
            splitted.append(opt)
    return splitted


@lru_cache(maxsize=20000)
def normalize_value(
    value: Any, normalize_: bool = False, lowercase: bool = False, asciify: bool = True
) -> Optional[str]:
    if normalize_:
        return normalize(value, ascii=asciify, lowercase=lowercase)

    text = stringify(value)
    if text is None:
        return None
    if lowercase:
        text = text.lower()
    return text.strip()

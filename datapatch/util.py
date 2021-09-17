import yaml
import pathlib
from typing import Union, Any
from functools import lru_cache
from normality import stringify, normalize

PathLike = Union[str, pathlib.Path]


def read_yaml_file(path: PathLike) -> Any:
    with open(path, "r") as fh:
        return yaml.load(fh, Loader=yaml.SafeLoader)


@lru_cache(maxsize=20000)
def normalize_value(value, normalize_=False, lowercase=False):
    if normalize_:
        return normalize(value, ascii=True, lowercase=lowercase)

    value = stringify(value)
    if value is None:
        return
    if lowercase:
        value = value.lower()
    return value.strip()

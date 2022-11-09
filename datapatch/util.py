import yaml
import pathlib
from typing import Optional, Union, Any
from functools import lru_cache
from normality import stringify, normalize

PathLike = Union[str, pathlib.Path]


def read_yaml_file(path: PathLike) -> Any:
    with open(path, "r") as fh:
        return yaml.load(fh, Loader=yaml.SafeLoader)


@lru_cache(maxsize=20000)
def normalize_value(value: Any, normalize_: bool=False, lowercase: bool=False) -> Optional[str]:
    if normalize_:
        return normalize(value, ascii=True, lowercase=lowercase)

    text = stringify(value)
    if text is None:
        return None
    if lowercase:
        text = text.lower()
    return text.strip()

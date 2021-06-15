import yaml
import pathlib
from typing import Union, Any

PathLike = Union[str, pathlib.Path]


def read_yaml_file(path: PathLike) -> Any:
    with open(path, "r") as fh:
        return yaml.load(fh, Loader=yaml.SafeLoader)

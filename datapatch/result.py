from typing import Any, Dict, List
from banal import hash_data
from normality import stringify


class Result(object):
    def __init__(self, data: Dict[str, Any]):
        self._id = hash_data(data)
        self.value = stringify(data.pop("value", None))
        self.values: List[str] = []
        values = data.pop("values", [])
        if len(values) == 0 and self.value is not None:
            self.values.append(self.value)
        for v in values:
            vn = stringify(v)
            if vn is not None:
                self.values.append(vn)
        self._data = data

    def __getattr__(self, name: str) -> Any:
        try:
            return self._data[name]
        except KeyError:
            return None

    def __repr__(self) -> str:
        return "<Result(%r, %r)>" % (self.values, self._data)

    def __hash__(self) -> int:
        return hash(self._id)

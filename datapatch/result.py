from banal import ensure_list


class Result(object):
    def __init__(self, data):
        self.value = data.pop("value", None)
        if "values" in data:
            self.values = ensure_list(data.pop("values", []))
        else:
            self.values = [self.value]
        self._data = data

    def __getattr__(self, name):
        try:
            return self._data[name]
        except KeyError:
            return None

    def __repr__(self):
        return "<Result(%r, %r)>" % (self.values, self._data)

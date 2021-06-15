from banal import ensure_list


class Result(object):
    def __init__(self, data):
        self._data = data

    @property
    def values(self):
        values = self._data.pop("values", self.value)
        return ensure_list(values)

    def __getattr__(self, name):
        try:
            return self._data[name]
        except KeyError:
            return None

    def __repr__(self):
        return "<Result(%r, %r)>" % (self.values, self._data)

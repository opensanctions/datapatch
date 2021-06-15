class DataPatchException(Exception):
    """Superclass for all exceptions from this package."""

    pass


class LookupException(DataPatchException):
    """Errors that take place during lookup, i.e. when matching a
    value against a `Lookup`."""

    def __init__(self, message: str, lookup, value):
        super(LookupException, self).__init__()
        self.message = message
        self.lookup = lookup
        self.value = value

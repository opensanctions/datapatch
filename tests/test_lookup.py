import yaml
import pytest
from .util import get_fixture_path

from datapatch import Lookup, LookupException

lookups = {}
with open(get_fixture_path("countries.yml"), "r") as fh:
    data = yaml.load(fh, Loader=yaml.SafeLoader)
    for name, config in data.items():
        lookups[name] = Lookup(name, config)


def test_simple():
    simple = lookups.get("simple")
    assert simple.get_value("Panama") == "PA"
    assert simple.get_value("France") == "FR"
    assert simple.get_value("Germany") is None

    assert simple.get_values("Panama") == ["PA"]
    multi = simple.get_values("Artsakh")
    assert "AZ" in multi


def test_required():
    required = lookups.get("required")
    assert required.get_value("France") == "FR"

    with pytest.raises(LookupException):
        assert required.get_value("Germany")

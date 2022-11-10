import pytest
from .util import get_fixture_path

from datapatch import read_lookups, LookupException

path = get_fixture_path("countries.yml")
lookups = read_lookups(path)


def test_simple():
    simple = lookups.get("simple")
    assert simple.get_value("Panama") == "PA"
    assert simple.get_value("France") == "FR"
    assert simple.get_value("Germany") is None

    assert simple.get_value("") == "ZZ"
    assert simple.get_value(None) == "ZZ"
    assert simple.get_value("-") == "DASH"

    assert simple.get_values("Panama") == ["PA"]
    multi = simple.get_values("Artsakh")
    assert "AZ" in multi
    assert len(simple.options), simple.options


def test_required():
    required = lookups.get("required")
    assert required.get_value("France") == "FR"

    with pytest.raises(LookupException):
        assert required.get_value("Germany")


def test_contains():
    contains = lookups.get("contains")
    assert contains.get_value("People's Republic of North Korea") == "KP"
    assert contains.get_value("Republic of North Kapadocia") is None
    assert contains.get_value("foo.bar") == 'FO'
    assert contains.get_value("foo bar") is None

    with pytest.raises(LookupException):
        assert contains.get_value("South Sudan")


def test_weights():
    weights = lookups.get("weights")
    assert weights.get_value("South Sudan") == 'SS'


def test_regex():
    regex = lookups.get("regex")
    assert regex.get_value("2005") == "year"
    assert regex.get_value("222") is None
    assert regex.get_value("22222") is None
    assert regex.get_value("aaaa") is None


def test_normal():
    normal = lookups.get("normal")
    assert normal.get_value("North!Korea!") == "KP"
    assert normal.get_value("NORTH-korea") == "KP"
    assert normal.get_value("korea") is None


def test_result():
    result = lookups.get("result")
    assert result.match("Korea").type == "Dictatorship"
    assert "Dictatorship" in repr(result.match("Korea"))
    assert result.match("Banana") is None

import os


fixtures_path = os.path.dirname(__file__)
fixtures_path = os.path.join(fixtures_path, "fixtures")


def get_fixture_path(file_name):
    return os.path.join(fixtures_path, file_name)

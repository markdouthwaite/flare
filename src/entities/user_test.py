import json

import pytest
from datetime import datetime
from src.entities.user import User


@pytest.fixture
def user():
    return User(name="Jane Smith", slug="jane-smith", email="jane@smith.com")


def test_user_entity_serializes_correctly(user):
    json_blob = user.json()
    assert isinstance(json.loads(json_blob)["createdAt"], str)


def test_user_entity_initializes_correctly_from_json(user):
    json_blob = user.json()

    loaded_user = User.parse_raw(json_blob)
    assert isinstance(loaded_user.createdAt, datetime)

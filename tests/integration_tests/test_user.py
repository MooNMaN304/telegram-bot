from src.user.user_model import UserModel
from unittest.mock import MagicMock
import pytest


@pytest.mark.parametrize("generate_users", [5], indirect=True)
def test_generate_users(generate_users):
    users = generate_users

    assert len(users) == 5
    for user in users:
        assert user.id is not None
        assert user.telegram_id is not None
        assert user.username is not None


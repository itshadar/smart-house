import pytest
from pytest_mock_resources import PostgresConfig


@pytest.fixture(scope="session")
def pmr_postgres_config() -> PostgresConfig:
    return PostgresConfig(image="postgres:13")  # production postgres version

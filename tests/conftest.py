from pytest import fixture
from pytest_mock_resources import PostgresConfig


@fixture(scope='session')
def pmr_postgres_config() -> PostgresConfig:
    return PostgresConfig(image='postgres:13')  # production postgres version

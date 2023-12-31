import os

from dotenv import load_dotenv

load_dotenv()

env_vars: list[str] = [
    "POSTGRES_HOST",
    "POSTGRES_PORT",
    "POSTGRES_USER",
    "POSTGRES_PASSWORD",
    "POSTGRES_DB",
]
db_config = {env_var: os.environ.get(env_var) for env_var in env_vars}

if None in db_config.values():
    raise ValueError(
        f"Environment variables "
        f"{','.join([repr(env_var) for env_var in db_config if not db_config[env_var]])} "
        f"not properly set."
    )

env = os.environ.get("PYTHON_ENV", "prod")

database_uri = (
    f"postgresql://"
    f"{db_config['POSTGRES_USER']}:{db_config['POSTGRES_PASSWORD']}"
    f"@{db_config['POSTGRES_HOST']}:{db_config['POSTGRES_PORT']}/{db_config['POSTGRES_DB']}"
)


async_database_uri = database_uri.replace("postgresql://", "postgresql+asyncpg://")

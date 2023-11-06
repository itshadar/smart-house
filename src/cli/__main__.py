from src.cli.configure_apps import build_app
from src.core.db_operations import AsyncUnitOfWork, get_async_uow

if __name__ == "__main__":
    async_uow: AsyncUnitOfWork = get_async_uow()
    app = build_app(async_uow)
    app()

from src.core.db_operations import get_async_uow, AsyncUnitOfWork
from .configure_apps import build_app


if __name__ == "__main__":

    async_uow: AsyncUnitOfWork = get_async_uow()
    app = build_app(async_uow)
    app()

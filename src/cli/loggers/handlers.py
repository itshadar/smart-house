from typer import echo
from logging import Handler, LogRecord, Formatter


class TyperLoggerHandler(Handler):

    def emit(self, record: LogRecord):
        echo(self.format(record))


def get_typer_handler() -> Handler:

    formatter = Formatter(f'[%(levelname)s] %(message)s')
    handler = TyperLoggerHandler()
    handler.setFormatter(formatter)
    return handler

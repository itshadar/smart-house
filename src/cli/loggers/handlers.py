from logging import Formatter, Handler, LogRecord

from typer import echo


class TyperLoggerHandler(Handler):
    def emit(self, record: LogRecord) -> None:
        echo(self.format(record))


def get_typer_handler() -> Handler:
    formatter = Formatter("[%(levelname)s] %(message)s")
    handler = TyperLoggerHandler()
    handler.setFormatter(formatter)
    return handler

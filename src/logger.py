from datetime import datetime
from enum import Enum
from io import FileIO
from typing import Final

from rich.console import Console
from rich.text import Text

__all__ = ["LOGGER"]

LOG_INFO_SPACE: Final[int] = 25


class Severity(Enum):
    ERROR = "red"
    DEBUG = "white"
    INFO = "cyan"
    SUCCESS = "green"


class Logger:
    def __init__(self, log_to_console: bool = True, log_to_file: bool = True):
        self._console: Console | None = Console() if log_to_console else None
        self._file: FileIO | None = None
        if log_to_file:
            log_file_path: str = f"py_midi_{datetime.now().strftime('%H_%M_%S')}.log"
            self._file = open(log_file_path, "a")

    def __del__(self):
        if self._file:
            self._file.close()

    def _log(self, message: str, severity: Severity) -> None:
        if not self._console and not self._file:
            return
        current_time: str = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        prefix: str = f"[{current_time}][{severity.name}]"
        whitespaces_length: int = LOG_INFO_SPACE - len(prefix)
        log: str = f"{prefix}{' ' * whitespaces_length}{message}"
        if self._console:
            self._console.print(Text(log, style=severity.value))
        if self._file:
            self._file.write(log)

    def error(self, message: str) -> None:
        self._log(message, Severity.ERROR)

    def debug(self, message: str) -> None:
        self._log(message, Severity.DEBUG)

    def info(self, message: str) -> None:
        self._log(message, Severity.INFO)

    def success(self, message: str) -> None:
        self._log(message, Severity.SUCCESS)


LOGGER: Logger = Logger()

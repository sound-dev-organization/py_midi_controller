from logger import LOGGER


class LoggedException(Exception):
    """Exception that logs with 'ERROR' severity when raised."""

    def __init__(self, message: str):
        LOGGER.error(message)
        super().__init__()


class ControllerNotFound(LoggedException):
    """Raised when MIDI controller not found."""

    def __init__(self, controller_name: str):
        super().__init__(f"MIDI Controller '{controller_name}' not found!")


class ReadingInterrupted(LoggedException):
    """Raised when MIDI reading interrupted."""

    def __init__(self):
        super().__init__("MIDI reading interrupted!")


class UnhandledException(LoggedException):
    """Raised when not specified 'Exception' caught."""

    def __init__(self, exception: Exception):
        super().__init__(f"Unhandled exception: {exception}")

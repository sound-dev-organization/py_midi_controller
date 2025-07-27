from threading import Thread
from typing import Final

import mido
from mido.backends.rtmidi import Input
from mido.messages.messages import Message

from exceptions import ControllerNotFound, ReadingInterrupted, UnhandledException
from logger import LOGGER


class Controller:
    """Interface between hardware and developer."""

    NAME: Final[str] = "MPK mini 3"

    def __init__(self):
        self._midi_port: str | None = next(
            (name for name in mido.get_input_names() if self.NAME in name), None
        )
        if not self._midi_port:
            raise ControllerNotFound(self.NAME)
        LOGGER.success(f"Connected to '{self.NAME}' successfully.")
        self._midi_queue: Input | None = None
        self._running: bool = False

    def __del__(self):
        """Log controller destruction."""
        LOGGER.info(f"Disconnected from '{self.NAME}'.")

    def _read_midi_input(self) -> None:
        """Read event messages from MIDI device."""
        try:
            while self._running:
                message: Message = next(iter(self._midi_queue))
                LOGGER.debug(message)
                # TODO: handle message
        except KeyboardInterrupt:
            raise ReadingInterrupted()
        except Exception:
            raise UnhandledException()

    def start(self) -> None:
        """Start thread for reading event messages from MIDI device."""
        LOGGER.info(f"Starting reading from '{self.NAME}'...")
        self._midi_queue = mido.open_input(self._midi_port)
        self._running = True
        Thread(target=self._read_midi_input, daemon=True).start()
        LOGGER.info(f"Started reading from '{self.NAME}'.")

    def stop(self) -> None:
        """Stop reading event messages from MIDI device."""
        self._running = False
        self._midi_queue.close()
        LOGGER.info(f"Stopped reading from '{self.NAME}'.")


if __name__ == "__main__":
    controller = Controller()
    controller.start()
    # time.sleep(...)
    controller.stop()

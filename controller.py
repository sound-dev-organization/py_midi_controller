from threading import Thread
from time import sleep
from typing import Final

import mido
from mido.backends.rtmidi import Input
from mido.messages.messages import Message


class Controller:
    NAME: Final[str] = "MPK mini 3"

    def __init__(self):
        self._midi_port: str | None = next(
            (name for name in mido.get_input_names() if "MPK mini 3" in name),
            None
        )
        if not self._midi_port:
            raise RuntimeError("MPK mini MIDI port not found.")
        self._midi_queue: Input | None = None
        self._running: bool = False

    def _read_midi_input(self):
        while self._running:
            message: Message = next(iter(self._midi_queue))
            # TODO: handle message

    def start(self):
        self._midi_queue = mido.open_input(self._midi_port)
        self._running = True
        Thread(target=self._read_midi_input, daemon=True).start()

    def stop(self):
        self._running = False
        self._midi_queue.close()

    
if __name__ == "__main__":
    controller = Controller()
    controller.start()
    # time.sleep(...)
    controller.stop()

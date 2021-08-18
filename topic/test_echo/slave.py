import time
from enum import Enum

from transceiver import Transceiver
from utils import hex_str


class State(Enum):
    idle = "idle"
    work = "work"


class TestEchoLossSlave:
    def __init__(self, local: tuple[str, int]):
        self.__transport = Transceiver(local)
        self.state = State.idle

    def start(self, remote: tuple[str, int]):
        """echo for certain address"""
        while True:
            data = self.__transport.recv(remote)
            self.__transport.send(remote, data)
            print(f"echo {hex_str(data)}")

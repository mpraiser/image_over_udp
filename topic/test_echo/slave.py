from common.transceiver import Transceiver
from common.utils import hex_str


class TestEchoLossSlave:
    def __init__(self, local: tuple[str, int]):
        self.__transport = Transceiver(local)

    def start(self, remote: tuple[str, int]):
        """receive from whichever address, echo to certain address"""
        while True:
            data = self.__transport.recv(None)
            self.__transport.send(remote, data)
            print(f"echo {hex_str(data)}")

import time
import random
import socket

from net_test_tools.transceiver import Transceiver
from net_test_tools.utils import hex_str
from .frame_def import frame


class Slave:
    def __init__(self):
        self.__result = []

    def run(
        self,
        local: tuple[str, int],
        remote: tuple[str, int],
        *,
        echo: bool,
        simulate_delay: bool = False
    ):
        """receive from whichever address, echo to certain address"""
        transport = Transceiver(local)
        transport.set_timeout(0.5)

        while True:
            try:
                data_recv = transport.recv(None)
                seq, eof, t_master, _, payload = frame.deserialize(data_recv).values()
                if simulate_delay:
                    time.sleep(random.random() * 0.02)
                t_slave = time.time()
                if echo:
                    data_send = frame.serialize(seq, eof, t_master, t_slave, payload)
                    transport.send(remote, data_send)
                t_ul = (t_slave - t_master) * 1000
                self.__result.append((seq, t_ul))
                print(f"seq = {seq}, ul = {t_ul:.2f} ms, echo: {hex_str(payload)}")
                if eof:
                    print(f"receive EOF!")
                    break
            except socket.timeout:
                continue
            except KeyboardInterrupt:
                break

    @property
    def result(self):
        return self.__result

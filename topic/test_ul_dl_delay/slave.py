import time
import random

from common.transceiver import Transceiver
from common.utils import hex_str
from .frame_def import frame


def run_slave(
    local: tuple[str, int],
    remote: tuple[str, int],
    *,
    echo: bool,
    simulate_delay: bool = False
) -> list[tuple[int, float]]:
    """receive from whichever address, echo to certain address"""
    transport = Transceiver(local)

    result = []

    while True:
        data_recv = transport.recv(None)
        seq, eof, t_master, _, payload = frame.deserialize(data_recv).values()
        if simulate_delay:
            time.sleep(random.random() * 0.02)
        t_slave = time.time()
        if echo:
            data_send = frame.serialize(seq, eof, t_master, t_slave, payload)
            transport.send(remote, data_send)
        t_ul = (t_slave - t_master) * 1000
        result.append((seq, t_ul))
        print(f"seq = {seq}, ul = {t_ul:.2f} ms, echo: {hex_str(payload)}")
        if eof:
            print(f"receive EOF!")
            break

    return result

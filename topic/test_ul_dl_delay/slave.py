import time

from transceiver import Transceiver
from utils import hex_str
from topic.test_ul_dl_delay import frame


def run_slave(
    local: tuple[str, int],
    remote: tuple[str, int]
):
    """receive from whichever address, echo to certain address"""
    transport = Transceiver(local)

    while True:
        data_recv = transport.recv(None)
        seq, t_master, _, payload = frame.deserialize(data_recv)
        t_slave = time.time()
        data_send = frame.serialize(seq, t_master, t_slave, payload)
        transport.send(remote, data_send)
        t_ul = (t_slave - t_master) * 1000
        print(f"seq = {seq}, ul = {t_ul:.2f} ms, echo: {hex_str(payload)}")

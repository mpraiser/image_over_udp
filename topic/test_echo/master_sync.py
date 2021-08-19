import socket
import time
from typing import Optional

from topic.test_loss import generate
from transceiver import Transceiver

from utils import hex_str


def prepare_dataset(max_packet_size: int, n_packet: int, *, random_size: bool):
    ret = {}
    for packet in generate(max_packet_size, n_packet, random_size=random_size):
        ret[packet] = {
            "t_send": -1,
            "delay": -1
        }
    return ret


class TestEchoLossMasterSync:
    def __init__(
            self,
            local: tuple[str, int],
            max_packet_size: int,
            n_packet: int,
            *,
            random_size: bool = True,
            timeout: Optional[float] = None
    ):
        self.transport = Transceiver(local)
        self.transport.set_timeout(timeout)
        self.dataset: dict = prepare_dataset(max_packet_size, n_packet, random_size=random_size)

    def start(self, remote: tuple[str, int], interval: float = 0):
        """echo for certain address"""
        for p_send in self.dataset:
            self.dataset[p_send]["t_send"] = time.time()
            self.transport.send(remote, p_send)
            try:
                p_recv = self.transport.recv(remote)
                t_recv = time.time()
                if self.dataset[p_recv]["t_send"]:
                    delay = t_recv - self.dataset[p_recv]["t_send"]
                    self.dataset[p_recv]["delay"] = delay
                    print(f"receive echo, delay = {delay * 1000:.2f} ms, {hex_str(p_recv)}")
                else:
                    print(f"receive unknown packet.")
                time.sleep(interval)
            except socket.timeout:
                continue

        count_send = 0
        count_recv = 0
        for packet in self.dataset:
            if self.dataset[packet]["t_send"]:
                count_send += 1
            if self.dataset[packet]["delay"] >= 0:
                count_recv += 1
        loss = (count_send - count_recv) / count_send * 100
        print(f"loss: {loss:.2f} %")

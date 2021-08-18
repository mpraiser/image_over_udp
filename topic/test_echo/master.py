import time
import socket
import asyncio
from enum import Enum
from typing import Optional

from transceiver import Transceiver
from topic.test_loss.dataset import generate
from utils import hex_str


class State(Enum):
    idle = "idle"
    syn_sent = "sync_sent"
    work = "work"


class TestEchoMasterProtocol(asyncio.DatagramProtocol):
    def __init__(self, dataset: dict):
        self.transport = None
        self.dataset = dataset

    def connection_made(self, transport: asyncio.DatagramTransport):
        self.transport = transport

    def datagram_received(self, data, addr):
        # ignore addr
        t_recv = time.time()
        if data not in self.dataset:
            print(f"Receive unknown packet. Errors may occur in transmission.")
            return
        if self.dataset[data]["t_send"]:
            delay = t_recv - self.dataset[data]["t_send"]
            self.dataset[data]["delay"] = delay
            print(f"Receive echo, delay = {delay}: {hex_str(data)}")
        else:
            print(f"Receive unsent packet. WTF?")


async def main(
        local: tuple[str, int],
        remote: tuple[str, int],
        max_packet_size: int,
        n_packet: int,
        *,
        random_size: bool = True,
        timeout: Optional[float] = None,
        interval: float = 0
):
    # prepare dataset
    dataset: dict = {}
    for packet in generate(max_packet_size, n_packet, random_size=random_size):
        dataset[packet] = {
            "t_send": -1,
            "delay": -1
        }
    loop = asyncio.get_running_loop()
    transport: asyncio.DatagramTransport
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: TestEchoMasterProtocol(dataset),
        local_addr=local,
        remote_addr=remote
    )

    for packet in dataset:
        await transport.sendto(packet, remote)


class TestEchoLossMaster:
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
        self.state = State.idle
        self.dataset: dict = {}
        for packet in generate(max_packet_size, n_packet, random_size=random_size):
            self.dataset[packet] = {
                "t_send": -1,
                "delay": -1
            }

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

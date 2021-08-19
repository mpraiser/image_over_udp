import asyncio
import time

from .master_sync import prepare_dataset
from utils import hex_str


async def main(
        local: tuple[str, int],
        remote: tuple[str, int],
        max_packet_size: int,
        n_packet: int,
        *,
        random_size: bool = True,
        interval: float = 0
):
    # prepare dataset
    dataset: dict = prepare_dataset(max_packet_size, n_packet, random_size=random_size)
    loop = asyncio.get_running_loop()
    transport: asyncio.DatagramTransport
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: TestEchoMasterProtocol(dataset),
        local_addr=local,
        remote_addr=remote
    )

    for packet in dataset:
        t_send = time.time()
        transport.sendto(packet, remote)
        dataset[packet]["t_send"] = t_send
        await asyncio.sleep(interval)

    await asyncio.sleep(5)
    transport.close()

    count_send = 0
    count_recv = 0
    avg_delay = 0
    for packet in dataset:
        if dataset[packet]["t_send"] >= 0:
            count_send += 1
        if (delay := dataset[packet]["delay"]) >= 0:
            count_recv += 1
            avg_delay += delay
    avg_delay /= count_recv
    loss = (count_send - count_recv) / count_send
    print(f"packet send = {count_send}, recv = {count_recv}, "
          f"loss = {loss:.2%}, average delay = {avg_delay:.2f} ms")


def master_async(
        local: tuple[str, int],
        remote: tuple[str, int],
        max_packet_size: int,
        n_packet: int,
        *,
        random_size: bool = True,
        interval: float = 0
):
    asyncio.run(main(
        local, remote, max_packet_size, n_packet,
        random_size=random_size, interval=interval
    ))


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

        if self.dataset[data]["t_send"] >= 0:
            delay = (t_recv - self.dataset[data]["t_send"]) * 1000
            self.dataset[data]["delay"] = delay
            print(f"Receive echo, delay = {delay:.2f} ms: {hex_str(data)}")
        else:
            print(f"Receive unsent packet. WTF?")

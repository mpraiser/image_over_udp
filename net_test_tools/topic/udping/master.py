import time
import asyncio
from typing import Optional
from collections.abc import Callable, Iterable

from net_test_tools.topic.interface import Topic
from net_test_tools.dataset import generate
from net_test_tools.utils import hex_str, delay_ns
from net_test_tools.transceiver import Transceiver
from .utils import frame, Entry


class UdpingMaster(Topic):
    def __init__(
            self,
            local: tuple[str, int],
            remote: tuple[str, int],
            max_packet_size: int,
            n_packet: Optional[int],
            *,
            random_size: bool,
            interval: tuple[tuple[int, float]] = (1, 1),
            preprocess: bool,
            tx_only: bool = False,
            runner: str,
    ):
        super().__init__()
        # result
        self.__result = []

        # configure address
        self.local = local
        self.remote = remote

        # interval control
        self.__iv_ptr = 0
        self.__iv_cnt = 0
        self.interval = interval

        # configure dataset
        max_payload_size = max_packet_size - frame.PREFIX_SIZE
        self.payloads = generate(
            max_payload_size, n_packet, random_size=random_size
        )
        self.n_packet = n_packet
        if n_packet is None:
            print("Preprocess disabled due to infinite transmission.")
            preprocess = False  # disable preprocess because packets are infinite
        if preprocess:
            print("Preparing dataset.")
            self.payloads = list(self.payloads)
        self.packets = self.__packets()

        # configure runner
        self.runner = runner
        self.tx_only = tx_only

    def next_interval(self) -> float:
        ret = self.interval[self.__iv_ptr][1]
        self.__iv_cnt += 1
        if self.__iv_cnt >= self.interval[self.__iv_ptr][0]:
            self.__iv_ptr = (self.__iv_ptr + 1) % len(self.interval)
            self.__iv_cnt = 0
        return ret

    def __packets(self):
        """generator of packets"""
        for seq, packet in enumerate(self.payloads):
            # in infinite mode, total will be seq + 1
            total = seq + 1 if self.n_packet is None else self.n_packet
            infinite = self.n_packet is None
            data = frame.serialize(infinite, seq, total, time.time(), 0, packet)
            yield data

    def run(self):
        super().run()
        t_start = time.time()
        print(f"udping-master starts: {t_start}")
        if self.runner == "async":
            asyncio.run(
                async_master_main(
                    self.local, self.remote,
                    self.packets, self.next_interval, self.add_result,
                    tx_only=self.tx_only
                )
            )
        elif self.runner == "sync":
            print("Warning: in sync mode, receiving is disabled.")
            self.tx_only = True
            sync_master_main(
                self.local, self.remote,
                self.packets, self.next_interval
            )
        else:
            raise Exception(f"Invalid runner: {self.runner}.")
        t_end = time.time()
        print(f"udping-master ends: {t_end}")

    def handle_packet(self, packet: bytes, t_recv: float) -> bool:
        """handle received packet, returns whether is last packet."""
        params = frame.deserialize(packet)
        seq = params["seq"]
        total = params["total"]
        t_master = params["t_master"]
        t_slave = params["t_slave"]
        payload = params["payload"]
        t_ul = (t_slave - t_master) * 1000
        t_dl = (t_recv - t_slave) * 1000
        self.add_result(Entry(seq, total, t_ul, 0))
        print(f"seq = {seq}, ul = {t_ul:.2f} ms, dl = {t_dl:.2f} ms: {hex_str(payload)}")
        if frame.is_end(params):
            print(f"receive last packet!")
            return True
        return False

    def add_result(self, entry: Entry):
        self.__result.append(entry)

    def result(self):
        return self.__result


class Protocol(asyncio.DatagramProtocol):
    def __init__(self, buffer: asyncio.Queue):
        self.transport = None
        self.buffer = buffer

    def connection_made(self, transport: asyncio.DatagramTransport):
        self.transport = transport

    def datagram_received(self, data, addr):
        # ignore addr
        t_recv = time.time()
        asyncio.ensure_future(self.buffer.put(
            (t_recv, data)
        ))


async def async_master_main(
        local: tuple[str, int],
        remote: tuple[str, int],
        packets: Iterable[bytes],
        next_interval: Callable,
        handle_packet: Callable,
        *,
        tx_only: bool = False
):
    # asyncio preparation
    last_packet = asyncio.Future()
    buffer = asyncio.Queue()
    # create transport
    loop = asyncio.get_running_loop()
    transport: asyncio.DatagramTransport
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: Protocol(buffer),
        local_addr=local
    )

    print("Start transmitting.")
    tx = asyncio.create_task(
        async_master_tx(
            last_packet,
            transport, remote,
            packets, next_interval
        )
    )
    tasks = [tx]
    if not tx_only:
        rx = asyncio.create_task(
            async_master_rx(
                last_packet, buffer,
                handle_packet
            )
        )
        tasks.append(rx)
    await asyncio.gather(*tasks)


async def async_master_tx(
        last_packet: asyncio.Future,
        transport: asyncio.DatagramTransport,
        remote: tuple[str, int],
        packets: Iterable[bytes],
        next_interval: Callable,
):
    for packet in packets:
        transport.sendto(packet, remote)
        await asyncio.sleep(next_interval())

    await last_packet
    transport.close()


async def async_master_rx(
        last_packet: asyncio.Future,
        buffer: asyncio.Queue,
        handle_packet: Callable,
):
    while True:
        t_recv, data = await buffer.get()
        is_end = handle_packet(data, t_recv)
        if is_end:
            last_packet.set_result(True)


def sync_master_main(
        local: tuple[str, int],
        remote: tuple[str, int],
        packets: Iterable[bytes],
        next_interval: Callable
):
    transport = Transceiver(local)
    for packet in packets:
        transport.send(remote, packet)
        delay_ns(next_interval() * 1e9)

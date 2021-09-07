import time
import random
import socket

from net_test_tools.plot import plot_line_chart, plot_histogram
from net_test_tools.transceiver import Transceiver
from net_test_tools.utils import hex_str
from .utils import frame, Entry


class Slave:
    def __init__(self):
        self.__result: list[Entry] = []

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
        self.__result: list[Entry] = []

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
                self.__result.append(Entry(seq, eof, t_ul, 0))
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

    def __check_result(self):
        self.__result.sort(key=lambda x: x.seq)
        if not self.__result[-1].eof:
            print("Warning: last packet is not EOF!")
        seqs = set()
        for entry in self.__result:
            if entry.seq in seqs:
                print("Warning: A seq exists multiple times!"
                      "Maybe Slave is not closed while Master runs twice?")

    @property
    def loss(self):
        if len(self.__result) == 0:
            return 0
        self.__check_result()
        max_seq = self.__result[-1].seq
        total = max_seq + 1
        return len(self.__result) / total

    def plot_line_chart(self):
        if len(self.__result) == 0:
            plot_line_chart([])

        self.__check_result()
        data = [(entry.seq, entry.t_ul) for entry in self.__result]
        plot_line_chart(data)

    def plot_histogram(self):
        if len(self.__result) == 0:
            plot_line_chart([])

        self.__check_result()
        data = [(entry.seq, entry.t_ul) for entry in self.__result]
        plot_histogram(data)

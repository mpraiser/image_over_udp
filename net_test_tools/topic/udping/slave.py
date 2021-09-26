import time
import socket

from net_test_tools.topic.interface import Topic
from net_test_tools.plot import plot_line_chart, plot_histogram
from net_test_tools.transceiver import Transceiver
from net_test_tools.utils import hex_str
from .utils import frame, Entry


class UdpingSlave(Topic):
    def __init__(
            self,
            local: tuple[str, int],
            remote: tuple[str, int],
            *,
            echo: bool = True,
    ):
        super().__init__()
        self.__result: list[Entry] = []
        self.__is_result_checked = True

        # configure address
        self.local = local
        self.remote = remote
        self.echo = echo

    def run(self):
        """receive from whichever address, echo to certain address"""
        super().run()
        echo = self.echo
        local = self.local
        remote = self.remote
        transport = Transceiver(local)
        transport.set_timeout(0.5)
        self.__result: list[Entry] = []

        while True:
            try:
                packet = transport.recv(None)
                params = frame.deserialize(packet)
                seq = params["seq"]
                total = params["total"]
                t_master = params["t_master"]
                infinite = params["infinite"]
                payload = params["payload"]

                t_slave = time.time()
                if echo:
                    data_send = frame.serialize(infinite, seq, total, t_master, t_slave, payload)
                    transport.send(remote, data_send)
                t_ul = (t_slave - t_master) * 1000
                self.add_result(Entry(seq, total, t_ul, 0))
                print(f"seq = {seq}, ul = {t_ul:.2f} ms, payload: {hex_str(payload)}")
                if frame.is_end(params):
                    print(f"receive last packet!")
                    break
            except socket.timeout:
                continue
            except KeyboardInterrupt:
                break

    def add_result(self, entry: Entry):
        self.__result.append(entry)
        self.__is_result_checked = False

    @property
    def result(self):
        self.__check_result()
        return self.__result

    def __check_result(self):
        if not self.__is_result_checked:
            self.__result.sort(key=lambda x: x.seq)
            seqs = set()
            for entry in self.__result:
                if entry.seq in seqs:
                    raise Exception("A seq exists multiple times! "
                                    "Maybe Slave is not closed while Master runs twice?")
                else:
                    seqs.add(entry.seq)
            self.__is_result_checked = True
        # if not self.__result[-1].eof:
        #     print("Warning: last packet is not EOF!")

    @property
    def loss(self):
        if len(self.__result) == 0:
            return 0
        self.__check_result()
        total = max(self.__result[-1].total, 1)
        return 1 - len(self.__result) / total

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

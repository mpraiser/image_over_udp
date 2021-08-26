import time
import random
import matplotlib.pyplot as plt

from transceiver import Transceiver
from utils import hex_str
from topic.test_ul_dl_delay import frame


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
        seq, eof, t_master, _, payload = frame.deserialize(data_recv)
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


def plot_t_ul(data: list[tuple[int, float]]):
    max_seq = max(data, key=lambda arg: arg[0])[0]
    t_map = dict(data)

    x = [i for i in range(max_seq + 1)]
    t = []
    for i in x:
        if i in t_map:
            t.append(t_map[i])
        else:
            t.append(0)
            plt.scatter(i, 0, marker="x", c="red")

    plt.xlabel("packet no.")
    plt.ylabel("UL delay / ms")
    plt.plot(x, t)
    plt.show()


def plot_t_ul_hist(data: list[tuple[int, float]]):
    """上行时间直方图"""
    t = []
    for seq, t_ul in data:
        t.append(t_ul)

    plt.hist(t, bins=20, edgecolor="black")
    plt.xlabel("UL delay / ms")
    plt.ylabel("frequency")
    plt.show()

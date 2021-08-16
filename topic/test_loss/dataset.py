import random
import matplotlib.pyplot as plt
from typing import List

from utils import Multiset


def generate(path: str,
             packet_size: int,
             n_packet: int,
             *,
             random_size=False):
    """
    Args:
        path: filename
        packet_size: (max) packet_size of each packet
        n_packet: number of packet to generate
        random_size: if packet size ranges from 1 to packet_size
    """
    assert 1 <= packet_size <= 4096
    assert 1 <= n_packet <= 256 ** 256

    with open(path, "w") as fp:
        for i in range(n_packet):
            packet = []
            seq = i
            count = 0
            while seq > 0:
                seq, tmp = divmod(seq, 256)
                packet = [tmp] + packet
                count += 1
            packet = [count] + packet
            size = random.randint(1, packet_size) if random_size else packet_size
            packet += [random.randint(0, 255) for _ in range(size - 1)]
            fp.write(" ".join((f"{item:02x}".upper() for item in packet)))
            fp.write("\n")


def loaded(path: str):
    """simple generator function to load packets"""
    with open(path, "r") as fp:
        for line in fp:
            packet: bytes = bytes.fromhex(line)
            yield packet


def load(path: str) -> List[bytes]:
    return list(loaded(path))


def preprocess_dataset(path: str, repeat: int) -> Multiset:
    dataset = Multiset()
    cases = load(path)
    for _ in range(repeat):
        for packet in cases:
            dataset.add(packet)
    return dataset


def plot_received(sent: Multiset, lost: Multiset):
    y = [sent[item] - lost[item] for item in sent]
    x = [i for i in range(sent.n_items())]
    for i in range(len(x)):
        if y[i] > 0:
            plt.scatter(x[i], y[i], s=1, c='black', marker='o')
        else:
            plt.scatter(x[i], y[i], s=1, c='red', marker='x')
    # plt.plot(x, y)
    plt.ylim([-1, max(y) + 1])
    plt.xlabel("Index")
    plt.ylabel("Packet received")
    plt.show()

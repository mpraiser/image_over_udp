import random
from typing import List


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

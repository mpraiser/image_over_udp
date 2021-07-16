import random
from collections import Counter


PATH = "loss_cases.txt"  # hex-string
PACKET_SIZE: int = 128  # <= 4096
N_PACKET: int = 153  # <= 153
REPEAT: int = 2  # >= 1
RX_ADDR = ("127.0.0.1", 8001)
TX_ADDR = ("127.0.0.1", 8000)
RX_TIMEOUT = 10


class Multiset(Counter):
    def remove(self, item):
        if item in self:
            self[item] -= 1
            if self[item] == 0:
                del self[item]
        else:
            raise ValueError

    def add(self, item):
        self[item] += 1

    def __len__(self):
        return sum(self.values())


def generate_cases(path=PATH):
    with open(path, "w") as fp:
        for i in range(N_PACKET):
            packet = [random.randint(0, 255) for _ in range(PACKET_SIZE-1)]
            packet = [i] + packet
            fp.write(" ".join((f"{item:02x}".upper() for item in packet)))
            fp.write("\n")


def loaded_cases(path=PATH):
    with open(path, "r") as fp:
        for line in fp:
            packet: bytes = bytes.fromhex(line)
            yield packet


def hex_str(packet: bytes) -> str:
    """convert bytes into hex-string"""
    return packet.hex(sep=" ").upper()


if __name__ == "__main__":
    generate_cases()
    for p in loaded_cases():
        # print(p)
        print(p.hex(sep=" ").upper())

import time
import platform
from collections import Counter


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


def hex_str(packet: bytes) -> str:
    """convert bytes into hex-string"""
    return packet.hex(sep=" ").upper()


if platform.system() != "Linux":
    print("Warning: delay_ns() is only accurate under Linux.")


def delay_ns(t: int):
    """
    accurate delay, only works under Linux
    about 10% inaccuracy under t = 10 us
    """
    t_start = time.time_ns()
    while time.time_ns() - t_start < t:
        pass

import time
import platform
from collections import Counter
from typing import Optional


class Multiset(Counter):
    def __init__(self):
        super().__init__()

    def remove(self, item):
        if item in self and self[item] > 0:
            self[item] -= 1
        else:
            raise ValueError

    def add(self, item):
        self[item] += 1

    def __len__(self):
        """sum of total count"""
        return sum(self.values())

    def n_items(self):
        """number of different items"""
        count = 0
        for _ in self:
            count += 1
        return count

    def __sub__(self, other):
        for item in other:
            self.remove(item)
        return self


def hex_str(packet: bytes, display_limit: Optional[int] = 16) -> str:
    """
    convert bytes into hex-string
    :param packet: packet to convert
    :param display_limit: limit of number of bytes to display, None to set it infinite.
    """
    if display_limit is None:
        return packet.hex(sep=" ").upper()
    else:
        display_limit = min(display_limit, len(packet))
        ret = packet[:display_limit].hex(sep=" ").upper()
        ret += f"... ({len(packet) - display_limit} bytes left)"
        return ret


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

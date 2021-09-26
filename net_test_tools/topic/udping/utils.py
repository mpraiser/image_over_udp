import struct
from collections import namedtuple

from net_test_tools.frame import LinearFrame


class UdpingFrame(LinearFrame):
    def __init__(self):
        super().__init__(
            {
                "infinite": "?",
                "seq": "I",
                "total": "I",
                "t_master": "d",
                "t_slave": "d",
                "payload": "s"
            }
        )
        self.PREFIX_SIZE = struct.calcsize(
            "".join(
                item for key, item in self.spec.items() if key != "payload"
            )
        )
        self.properties = None

    @staticmethod
    def is_end(properties: dict):
        return (not properties["infinite"]) and properties["seq"] >= properties["total"] - 1


frame = UdpingFrame()

Entry = namedtuple("Entry", ["seq", "total", "t_ul", "t_dl"])

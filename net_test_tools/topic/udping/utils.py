import struct
from collections import namedtuple

from net_test_tools.frame import LinearFrame


frame = LinearFrame(
    {
        "seq": "H",
        "eof": "?",
        "t_master": "d",
        "t_slave": "d",
        "payload": "s"
    }
)
frame.PREFIX_SIZE = struct.calcsize("H?dd")

Entry = namedtuple("Entry", ["seq", "eof", "t_ul", "t_dl"])
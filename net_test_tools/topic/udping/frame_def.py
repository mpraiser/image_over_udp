import struct
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

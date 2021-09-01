"""
简易的帧解析和生成，仅支持线性帧结构
"""

import struct
from typing import Any


class LinearFrame:
    """
    basic use format string in struct, expect bare 's' means greedy bytes.
    """
    def __init__(self, spec: dict[str, str]):
        self.spec = spec

    def serialize(self, *args) -> bytes:
        if len(args) != len(self.spec):
            raise Exception

        frame = b""
        # for each section
        for i, fc in enumerate(self.spec.values()):
            arg = args[i]
            if fc == "s":
                fmt = str(len(arg)) + "s"
            else:
                fmt = fc
            section = struct.pack(fmt, arg)
            frame += section
        return frame

    def deserialize(self, frame: bytes) -> dict[Any]:
        ret = {}
        ptr = 0
        # for each section
        for i, item in enumerate(self.spec.items()):
            label, fc = item[0], item[1]
            if fc == "s":
                fmt = str(len(frame) - ptr) + "s"
            else:
                fmt = fc
            size = struct.calcsize(fmt)
            value = struct.unpack(fmt, frame[ptr:ptr+size])[0]
            ptr += size
            ret[label] = value
        return ret

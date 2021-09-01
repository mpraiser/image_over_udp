from enum import IntEnum
from typing import Dict


class FragFlag(IntEnum):
    NOT = 0
    START = 1
    CONTINUE = 2
    END = 3

    @staticmethod
    def check(value: int):
        type_dict = {
            0: FragFlag.NOT,
            1: FragFlag.START,
            2: FragFlag.CONTINUE,
            3: FragFlag.END
        }
        if value in type_dict:
            return type_dict[value]
        else:
            raise ValueError("Invalid fragment flag value.")


class Frame:
    BYTE_ORDER = 'big'
    HEADER_COST = 1 + 2 + 2 + 1
    MAX_PAYLOAD_LEN = 2048 - HEADER_COST

    def __init__(self, frame_type: int, payload_len: int, seq: int, frag_flag: FragFlag, data: bytes):
        assert frame_type == 0xff
        assert 2 <= payload_len <= Frame.MAX_PAYLOAD_LEN
        assert 0 <= seq < 2 ** 16
        assert frag_flag in FragFlag
        assert 0 <= len(data) <= Frame.MAX_PAYLOAD_LEN

        self.frame_type = frame_type  # 0xff
        self.payload_len = payload_len
        self.seq = seq
        self.frag_flag = frag_flag
        self.data = data

    @staticmethod
    def from_dict(data: Dict):
        return Frame(**data)

    @staticmethod
    def from_bytes(data: bytes):
        frame_type = int(data[0])
        payload_len = int(data[1:1+2].hex(), base=16)
        if len(data) < Frame.HEADER_COST + payload_len:
            raise ValueError("Invalid length of payload")
        seq = int(data[3:3+2].hex(), base=16)
        frag_flag = FragFlag.check(data[5])
        data = data[6:6+payload_len]
        return Frame(frame_type, payload_len, seq, frag_flag, data)

    def to_bytes(self):
        result = self.frame_type.to_bytes(1, self.BYTE_ORDER) \
                 + self.payload_len.to_bytes(2, self.BYTE_ORDER) \
                 + self.seq.to_bytes(2, self.BYTE_ORDER) \
                 + self.frag_flag.value.to_bytes(1, self.BYTE_ORDER) \
                 + self.data

        return result

    def to_dict(self):
        return {
            "frame_type": self.frame_type,
            "payload_len": self.payload_len,
            "seq": self.seq,
            "frag_flag": self.frag_flag,
            "data": self.data
        }


if __name__ == "__main__":
    f1 = Frame.from_bytes(b"\xff\x00\x03\x00\x00\x00\x01\x02\x03")
    print(f1.to_dict())
    print(f1.to_bytes())

    f2 = Frame.from_dict(f1.to_dict())
    print(f2.to_dict())
    print(f2.to_bytes())

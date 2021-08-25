import struct


fmt = "H?dd"
prefix_size = int(struct.calcsize(fmt))


def serialize(seq: int, eof: bool, t_master: float, t_slave: float, payload: bytes):
    return struct.pack(fmt, seq, eof, t_master, t_slave) + payload


def deserialize(frame: bytes) -> tuple[int, bool, float, float, bytes]:
    seq, eof, t_master, t_slave = struct.unpack(fmt, frame[0:prefix_size])
    payload = frame[prefix_size:]
    return seq, eof, t_master, t_slave, payload


if __name__ == "__main__":
    f = serialize(1234, False, 1629357753.8914032, 0, b"\x00\x01\x02\x03\x04")
    print(f)
    print(deserialize(f))

import socket
from enum import IntEnum
from typing import Optional, Callable, Dict

from net_test_tools.utils import delay_ns


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


class FragFailure(Exception):
    pass


class Transceiver:
    """
    使用UDP对图片进行分片传输
    内置私有分片传输协议
    """
    def __init__(self, local: tuple[str, int], *, bufsize=4096):
        self.local = local
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket.bind(local)
        self.bufsize = bufsize

    def set_timeout(self, t: Optional[float]):
        self.__socket.settimeout(t)

    def set_blocking(self, flag: Optional[bool]):
        self.set_blocking(flag)

    def send(self, remote: tuple[str, int], data: bytes):
        self.__socket.sendto(data, remote)

    def recv(self, remote: Optional[tuple[str, int]]):
        """
        blocking receive
        :param remote: if None, will receive from whichever address
        """
        while True:
            data, addr = self.__socket.recvfrom(self.bufsize)
            if remote is None or addr == remote:
                return data

    def send_protocol(self, remote: tuple[str, int], data: bytes, *, interval=0):
        """send with fragmentation according to protocol"""
        if len(data) > Frame.MAX_PAYLOAD_LEN:
            frames = self.fragmentation(data)
        else:
            frames = [Frame(0xff, len(data), 0, FragFlag.NOT, data)]
        # send
        frames = [_.to_bytes() for _ in frames]

        # print("Frames:")
        # for frame in frames:
        #     print(frame.hex(" ").upper())

        print("Start transmitting.")
        interval_ns = int(interval * 1e9)
        for frame in frames:
            if interval > 0:
                delay_ns(interval_ns)
            self.__socket.sendto(frame, remote)
        print("End of transmitting.")

    @staticmethod
    def fragmentation(data: bytes) -> list[Frame]:
        """分片"""
        step = Frame.MAX_PAYLOAD_LEN
        fragments = [data[i:i+step] for i in range(0, len(data), step)]
        frames = []
        for seq in range(len(fragments)):
            data = fragments[seq]
            if seq == 0:
                frag_flag = FragFlag.START
            elif seq == len(fragments) - 1:
                frag_flag = FragFlag.END
            else:
                frag_flag = FragFlag.CONTINUE
            frame = Frame(0xff, len(data), seq, frag_flag, data)
            frames.append(frame)
        return frames

    @staticmethod
    def reassembly(buffer: list[Frame]) -> bytes:
        encoded = b""
        state = 'start'
        buffer = iter(buffer)
        while state != 'end':
            try:
                frame = next(buffer)
            except StopIteration:
                raise FragFailure

            if state == "start":
                if frame.frag_flag is FragFlag.NOT:
                    encoded = frame.data
                    state = 'end'
                elif frame.frag_flag is FragFlag.START:
                    encoded += frame.data
                    state = 'continue'
                else:
                    continue  # 如果不是起始帧，跳过

            elif state == "continue":
                if frame.frag_flag is FragFlag.CONTINUE:
                    encoded += frame.data
                elif frame.frag_flag is FragFlag.END:
                    encoded += frame.data
                    state = 'end'
                else:
                    raise FragFailure

        return encoded

    def listen_protocol(
            self,
            remote: tuple[str, int],
            *,
            callback: Callable[[int, bytes], None],
            timeout=50):
        self.set_timeout(timeout)

        buffer = []
        count = 0
        n_frag = None

        def init_buffer():
            nonlocal buffer, n_frag
            buffer = []
            n_frag = None

        def callback_warp(buf: list[Frame]):
            nonlocal count
            full_data = self.reassembly(buf)
            callback(count, full_data)

        while True:
            try:
                data, addr = self.__socket.recvfrom(self.bufsize)
                if addr != remote:
                    continue

                frame = Frame.from_bytes(data)
                # if non-frag, directly callback
                if frame.frag_flag is FragFlag.NOT:
                    callback_warp([frame])
                    count += 1
                else:
                    buffer.append(frame)
                    if frame.frag_flag is FragFlag.END:
                        n_frag = frame.seq + 1

                if n_frag and len(buffer) >= n_frag:
                    buffer.sort(key=lambda x: x.seq)
                    callback_warp(buffer)
                    count += 1
                    init_buffer()

            except socket.timeout:
                return

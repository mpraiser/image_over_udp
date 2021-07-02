import socket
import cv2
import numpy as np
from typing import Tuple, List
from frame import Frame, FragFlag


class FragFailure(Exception):
    pass


class Transceiver:
    """
    使用UDP对图片进行分片传输
    """
    def __init__(self, local: Tuple[str, int], *, bufsize=1024):
        self.local = local
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.bind(local)
        self.bufsize = bufsize

    def send_image(self, remote: Tuple[str, int], image_path: str):
        # encode image
        image = cv2.imread(image_path)
        flag, content = cv2.imencode(".jpg", image)
        if not flag:
            raise Exception
        data = content.tostring()
        # fragmentation or not
        if len(data) > Frame.MAX_PAYLOAD_LEN:
            frames = self.fragmentation(data)
        else:
            frames = [Frame(0xff, len(data), 0, FragFlag.NOT, data)]
        # send
        for frame in frames:
            self._socket.sendto(frame.to_bytes(), remote)

    @staticmethod
    def fragmentation(data: bytes) -> List[Frame]:
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
            frame = Frame(0xff, len(data), 0, frag_flag, data)
            frames.append(frame)
        return frames

    def recv_image(self, remote: Tuple[str, int]) -> np.array:
        encoded = b""
        state = 'start'
        while state != 'end':
            data, addr = self._socket.recvfrom(self.bufsize)
            # skip data from other address
            if addr != remote:
                continue
            # print("received:", data)
            frame = Frame.from_bytes(data)
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

        arr = np.frombuffer(encoded, dtype=np.uint8)
        image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        return image

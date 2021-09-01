import cv2
import numpy as np
from net_test_tools.transceiver import Transceiver, FragFailure
from typing import Tuple


def decode_image(encoded: bytes) -> np.array:
    arr = np.frombuffer(encoded, dtype=np.uint8)
    image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return image


def show(title: str, image: np.array):
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def callback(count: int, data: bytes):
    show(str(count), decode_image(data))


def listen_until_timeout(
        local: Tuple[str, int],
        remote: Tuple[str, int],
        *,
        timeout: int = 10
):
    transport = Transceiver(local)
    try:
        transport.listen_protocol(
            remote,
            callback=callback,
            timeout=timeout
        )
    except FragFailure:
        print("组包或接收失败")

import cv2
import numpy as np
from transceiver import Transceiver, FragFailure


def show(title: str, image: np.array):
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def callback(count: int, data: bytes):
    show(str(count), Transceiver.decode_image(data))


if __name__ == "__main__":
    rx = Transceiver(("127.0.0.1", 8001))
    try:
        rx.listen_protocol(
            ("127.0.0.1", 8000),
            callback=callback,
            timeout=10
        )
    except FragFailure:
        print("组包或接收失败")

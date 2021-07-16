import cv2
import threading
from transceiver import Transceiver, FragFailure


def show(c, i):
    cv2.imshow(str(c), i)
    cv2.waitKey(0)


if __name__ == "__main__":
    rx = Transceiver(("127.0.0.1", 8001))
    counter = 0
    while True:
        try:
            image = rx.recv_image(("127.0.0.1", 8000))
            threading.Thread(target=show, args=(counter, image), daemon=True).start()
            counter += 1
        except FragFailure:
            print("组包或接收失败")

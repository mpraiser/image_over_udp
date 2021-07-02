import cv2
from transceiver import Transceiver, FragFailure


if __name__ == "__main__":
    rx = Transceiver(("127.0.0.1", 8001))
    counter = 0
    while True:
        try:
            image = rx.recv_image(("127.0.0.1", 8000))
            cv2.imshow(str(counter), image)
            cv2.waitKey(0)
            counter += 1
        except FragFailure:
            print("组包或接收失败")

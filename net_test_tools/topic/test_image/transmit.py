import cv2
from typing import Tuple
from net_test_tools.transceiver import Transceiver


def transmit_image(local: Tuple[str, int], remote: Tuple[str, int], path: str, *, interval=0):
    transport = Transceiver(local)

    # encode image
    image = cv2.imread(path)
    flag, content = cv2.imencode(".jpg", image)
    if not flag:
        raise Exception
    data = content.tostring()
    # fragmentation or not
    transport.send_protocol(remote, data, interval=interval)

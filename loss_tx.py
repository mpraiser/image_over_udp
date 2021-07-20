import random
import time
from typing import Tuple

import loss
from loss import loaded_cases
from utils import delay_ns
from transceiver import Transceiver


def loss_tx(
        local: Tuple[str, int],
        remote: Tuple[str, int],
        path: str,
        *,
        interval: float = 0,
        repeat: int = 1,
        random_tx: bool = False
        ):
    # prepare sending data
    packets = []
    for packet in loaded_cases(path):
        for _ in range(repeat):
            if (not random_tx) or random.randint(0, 1) == 1:
                packets.append(packet)
    interval_ns = int(interval * 1e9)
    tx = Transceiver(local)

    t_start = time.time()
    for packet in packets:
        tx.send(remote, packet)
        if interval > 0:
            delay_ns(interval_ns)
    t_total = time.time() - t_start
    print(f"total time: {t_total} sec, each transmit takes {t_total / len(packets)} sec")


if __name__ == "__main__":
    INTERVAL = 0  # seconds
    RANDOM_TX = False  # whether randomly send packets
    LOCAL = ("127.0.0.1", 8000)
    REMOTE = ("127.0.0.1", 8001)
    PATH = loss.PATH
    REPEAT = loss.REPEAT

    loss_tx(LOCAL, REMOTE, PATH, interval=INTERVAL, repeat=REPEAT, random_tx=RANDOM_TX)

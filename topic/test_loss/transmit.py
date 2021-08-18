import random
import time
from typing import Tuple, List

from .dataset import load
from transceiver import Transceiver
from utils import delay_ns


def transmit_dataset(
        local: Tuple[str, int],
        remote: Tuple[str, int],
        path: str,
        *,
        interval: float = 0,
        repeat: int = 1,
        random_tx: bool = False
        ):

    # prepare sending data
    dataset: List[bytes] = []
    for _ in range(repeat):
        for packet in load(path):
            if (not random_tx) or random.randint(0, 1) == 1:
                dataset.append(packet)
    interval_ns = int(interval * 1e9)
    transport = Transceiver(local)

    # start transmitting
    print("Start transmitting.")
    t_start = time.time()
    for packet in dataset:
        transport.send(remote, packet)
        if interval > 0:
            delay_ns(interval_ns)
    t_total = time.time() - t_start
    print(f"total time: {t_total} sec, each transmit takes {t_total / len(dataset)} sec")

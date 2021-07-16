import random
import time
from loss import loaded_cases, TX_ADDR, RX_ADDR
from transceiver import Transceiver


INTERVAL = 1  # seconds
RANDOM_TX = True  # whether randomly send packets


tx = Transceiver(TX_ADDR)
for packet in loaded_cases():
    if (not RANDOM_TX) or random.randint(0, 1) == 1:
        tx.send(RX_ADDR, packet)
        time.sleep(INTERVAL)

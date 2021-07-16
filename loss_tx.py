import random
import time
from loss import loaded_cases, hex_str
from loss import TX_ADDR, RX_ADDR, REPEAT
from transceiver import Transceiver


INTERVAL = 1  # seconds
RANDOM_TX = True  # whether randomly send packets


tx = Transceiver(TX_ADDR)
for _ in range(REPEAT):
    for packet in loaded_cases():
        if (not RANDOM_TX) or random.randint(0, 1) == 1:
            print(f"send: {hex_str(packet)}")
            tx.send(RX_ADDR, packet)
            if INTERVAL > 0:
                time.sleep(INTERVAL)

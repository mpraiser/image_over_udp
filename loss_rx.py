"""
Test packet loss for 1-way transmission.
Start loss_rx.py first, then loss_tx.py.
"""

from loss import loaded_cases, TX_ADDR, RX_ADDR, hex_str
from transceiver import Transceiver
from collections import deque


rx = Transceiver(RX_ADDR)
packets_send = deque()
count_send = 0

for p_send in loaded_cases():
    packets_send.append(p_send)
    count_send += 1

count_recv = 0
for i in range(count_send):
    p_recv = rx.recv(TX_ADDR)
    while p_recv[0] > packets_send[0][0]:
        p_loss = packets_send.popleft()
        print(f"loss: {hex_str(p_loss)}")
    if p_recv == packets_send[0]:
        count_recv += 1
        print(f"receive: {hex_str(p_recv)}")
    else:
        print(f"receive but incorrect: {hex_str(p_recv)}")
    packets_send.popleft()
    recv_rate = count_recv/count_send * 100
    print(f"recv = {recv_rate:.2f} %")




"""
Test packet loss for 1-way transmission.
Start loss_rx.py first, then loss_tx.py.
"""

from loss import loaded_cases, hex_str, Multiset
from loss import TX_ADDR, RX_ADDR, RX_TIMEOUT, REPEAT
from transceiver import Transceiver
from socket import timeout


rx = Transceiver(RX_ADDR)
rx.set_timeout(RX_TIMEOUT)

packets_send = Multiset()
for _ in range(REPEAT):
    for packet in loaded_cases():
        packets_send.add(packet)
count_send = len(packets_send)

count_recv = 0
count_correct = 0
for i in range(count_send):
    try:
        p_recv = rx.recv(TX_ADDR)
    except timeout:
        print(f"timeout")
        break

    count_recv += 1

    if p_recv not in packets_send:
        print(f"receive but incorrect: {hex_str(p_recv)}")
    else:
        print(f"receive: {hex_str(p_recv)}")
        packets_send.remove(p_recv)
        count_correct += 1

    recv_rate = count_recv/count_send * 100  # may > 100% when lots of incorrect packets are received.
    print(f"recv = {recv_rate:.2f} %")

loss_rate = (count_send - count_correct) / count_send * 100
print(f"packet send = {count_send}, packet received = {count_recv}, correct packet = {count_correct}, loss = {loss_rate:.2f} %")

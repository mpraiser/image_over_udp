"""
Test packet loss for 1-way transmission.
Start loss_rx.py first, then loss_tx.py.
"""
import socket
from typing import Tuple

import loss
from loss import load_cases
from utils import Multiset, hex_str
from transceiver import Transceiver


def loss_rx(
        local: Tuple[str, int],
        remote: Tuple[str, int],
        path: str,
        *,
        timeout: float = 0,
        repeat: int = 1,
        ):
    rx = Transceiver(local)
    rx.set_timeout(timeout)

    # expected sent packets
    packets_send = Multiset()
    cases = load_cases(path)
    for _ in range(repeat):
        for packet in cases:
            packets_send.add(packet)
    count_send = len(packets_send)

    count_recv = 0
    count_correct = 0
    for i in range(count_send):
        try:
            p_recv = rx.recv(remote)
        except socket.timeout:
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
    print(f"packet send = {count_send}, packet received = {count_recv}, "
          f"correct packet = {count_correct}, loss = {loss_rate:.2f} %")


if __name__ == "__main__":
    TIMEOUT = 10
    LOCAL = ("127.0.0.1", 8001)
    REMOTE = ("127.0.0.1", 8000)
    PATH = loss.PATH
    REPEAT = loss.REPEAT

    loss_rx(LOCAL, REMOTE, PATH, timeout=TIMEOUT, repeat=REPEAT)

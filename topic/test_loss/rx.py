import socket
from typing import Tuple

from topic.test_loss.dataset import load
from transceiver import Transceiver
from utils import Multiset, hex_str


def receive_for_dataset(
        local: Tuple[str, int],
        remote: Tuple[str, int],
        path: str,
        *,
        timeout: float = 0,
        repeat: int = 1,
        ):
    """receive expected data in dataset"""
    transport = Transceiver(local)
    transport.set_timeout(timeout)

    # expected sent packets
    dataset = Multiset()
    cases = load(path)
    for _ in range(repeat):
        for packet in cases:
            dataset.add(packet)
    count_send = len(dataset)

    count_recv = 0
    count_correct = 0
    for i in range(count_send):
        try:
            p_recv = transport.recv(remote)
        except socket.timeout:
            print(f"timeout")
            break

        count_recv += 1

        if p_recv not in dataset:
            print(f"receive but incorrect: {hex_str(p_recv)}")
        else:
            print(f"receive: {hex_str(p_recv)}")
            dataset.remove(p_recv)
            count_correct += 1

        recv_rate = count_recv/count_send * 100  # may > 100% when lots of incorrect packets are received.
        print(f"recv = {recv_rate:.2f} %")

    loss_rate = (count_send - count_correct) / count_send * 100
    print(f"packet send = {count_send}, packet received = {count_recv}, "
          f"correct packet = {count_correct}, loss = {loss_rate:.2f} %")

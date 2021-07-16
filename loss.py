import random


PATH = "loss_cases.txt"  # hex-string
PACKET_SIZE = 128
N_PACKET = 100
RX_ADDR = ("127.0.0.1", 8001)
TX_ADDR = ("127.0.0.1", 8000)


def generate_cases(path=PATH):
    with open(path, "w") as fp:
        for i in range(N_PACKET):
            packet = [random.randint(0, 255) for _ in range(PACKET_SIZE-1)]
            packet = [i] + packet
            fp.write(" ".join((f"{item:02x}".upper() for item in packet)))
            fp.write("\n")


def loaded_cases(path=PATH):
    with open(path, "r") as fp:
        for line in fp:
            packet: bytes = bytes.fromhex(line)
            yield packet


def hex_str(packet: bytes) -> str:
    """convert bytes into hex-string"""
    return packet.hex(sep=" ").upper()


if __name__ == "__main__":
    generate_cases()
    for p in loaded_cases():
        # print(p)
        print(p.hex(sep=" ").upper())

from transceiver import Transceiver


if __name__ == "__main__":
    tx = Transceiver(("127.0.0.1", 8000))
    tx.send_image(("127.0.0.1", 8001), "lena.jpg")

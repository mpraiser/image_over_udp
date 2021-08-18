from topic import test_image


if __name__ == "__main__":
    LOCAL = ("127.0.0.1", 8000)
    REMOTE = ("127.0.0.1", 8001)
    PATH = "lena.jpg"
    INTERVAL = 0

    test_image.transmit_image(LOCAL, REMOTE, PATH, interval=INTERVAL)

from topic import test_image


if __name__ == "__main__":
    LOCAL = ("127.0.0.1", 8001)
    REMOTE = ("127.0.0.1", 8000)
    TIMEOUT = 3600  # seconds

    test_image.listen_until_timeout(LOCAL, REMOTE, timeout=TIMEOUT)

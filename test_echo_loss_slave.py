from topic import test_echo


if __name__ == "__main__":
    LOCAL = ("127.0.0.1", 8001)
    REMOTE = ("127.0.0.1", 8000)

    slave = test_echo.TestEchoLossSlave(LOCAL)
    slave.start(REMOTE)

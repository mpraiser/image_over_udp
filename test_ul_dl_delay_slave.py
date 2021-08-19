from topic import test_ul_dl_delay


if __name__ == "__main__":
    LOCAL = ("127.0.0.1", 8001)
    REMOTE = ("127.0.0.1", 8000)

    slave = test_ul_dl_delay.run_slave(LOCAL, REMOTE)

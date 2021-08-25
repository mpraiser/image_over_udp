from topic import test_ul_dl_delay


if __name__ == "__main__":
    LOCAL = ("127.0.0.1", 8001)
    REMOTE = ("127.0.0.1", 8000)
    PLOT = True  # 是否进行绘图
    ECHO = True  # slave是否进行回复

    data = test_ul_dl_delay.run_slave(LOCAL, REMOTE, echo=ECHO)
    if PLOT:
        test_ul_dl_delay.plot_t_ul(data)

from topic import test_ul_dl_delay


if __name__ == "__main__":
    LOCAL = ("127.0.0.1", 8001)
    REMOTE = ("127.0.0.1", 8000)
    PLOT = False  # 是否绘制上行时延图
    PLOT_HIST = True  # 是否绘制上行时延直方图
    ECHO = True  # slave是否进行回复

    data = test_ul_dl_delay.run_slave(LOCAL, REMOTE, echo=ECHO)
    if PLOT:
        test_ul_dl_delay.plot_t_ul(data)
    if PLOT_HIST:
        test_ul_dl_delay.plot_t_ul_hist(data)

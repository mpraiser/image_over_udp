from net_test_tools.topic import udping


if __name__ == "__main__":
    LOCAL = ("127.0.0.1", 8001)
    REMOTE = ("127.0.0.1", 8000)
    PLOT_LINE_CHART = True  # 是否绘制上行时延图
    PLOT_HISTOGRAM = False  # 是否绘制上行时延直方图
    ECHO = False  # slave是否进行回复

    slave = udping.slave.Slave()
    slave.run(LOCAL, REMOTE, echo=ECHO)
    print(f"total = {slave.result[-1].seq + 1}, loss = {slave.loss:.2%}")
    if PLOT_LINE_CHART:
        slave.plot_line_chart()
    if PLOT_HISTOGRAM:
        slave.plot_histogram()

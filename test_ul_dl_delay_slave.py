import net_test_tools
from net_test_tools.topic import udping


if __name__ == "__main__":
    LOCAL = ("127.0.0.1", 8001)
    REMOTE = ("127.0.0.1", 8000)
    PLOT_LINE_CHART = False  # 是否绘制上行时延图
    PLOT_HISTOGRAM = True  # 是否绘制上行时延直方图
    ECHO = True  # slave是否进行回复

    slave = udping.slave.Slave()
    slave.run(LOCAL, REMOTE, echo=ECHO)
    data = slave.result
    if PLOT_LINE_CHART:
        net_test_tools.plot.plot_t_ul(data)
    if PLOT_HISTOGRAM:
        net_test_tools.plot.plot_t_ul_hist(data)

import matplotlib.pyplot as plt

from net_test_tools.utils import Multiset


def plot_line_chart(data: list[tuple[int, float]]):
    """
    上行时间折线图

    :param data: list of (seq, t_ul), must be sorted.
    :return:
    """
    max_seq = max(data, key=lambda arg: arg[0])[0]
    t_map = dict(data)
    # precess data
    x = [item[0] for item in data]
    t = [item[1] for item in data]
    for i in range(max_seq + 1):
        if i not in t_map:
            plt.scatter(i, 0, marker="x", c="red")
    # x = [i for i in range(max_seq + 1)]
    # t = []
    # for i in x:
    #     if i in t_map:
    #         t.append(t_map[i])
    #     else:
    #         t.append(0)
    #         plt.scatter(i, 0, marker="x", c="red")

    plt.xlabel("packet no.")
    plt.ylabel("UL delay / ms")
    plt.plot(x, t)
    plt.show()


def plot_histogram(data: list[tuple[int, float]]):
    """
    上行时间直方图

    :param data: list of (seq, t_ul), must be sorted.
    :return:
    """
    t = []
    for _, t_ul in data:
        t.append(t_ul)

    plt.hist(t, bins=20, edgecolor="black")
    plt.xlabel("UL delay / ms")
    plt.ylabel("frequency")
    plt.show()


def plot_loss(sent: Multiset, lost: Multiset):
    y = [sent[item] - lost[item] for item in sent]
    x = [i for i in range(sent.n_items())]
    for i in range(len(x)):
        if y[i] > 0:
            plt.scatter(x[i], y[i], s=1, c='black', marker='o')
        else:
            plt.scatter(x[i], y[i], s=1, c='red', marker='x')
    # plt.plot(x, y)
    plt.ylim([-1, max(y) + 1])
    plt.xlabel("Index")
    plt.ylabel("Packet received")
    plt.show()

from matplotlib import pyplot as plt

from net_test_tools.common.utils import Multiset


def plot_t_ul(data: list[tuple[int, float]]):
    """
    上行时间折线图

    :param data:
    :return:
    """
    max_seq = max(data, key=lambda arg: arg[0])[0]
    t_map = dict(data)

    x = [i for i in range(max_seq + 1)]
    t = []
    for i in x:
        if i in t_map:
            t.append(t_map[i])
        else:
            t.append(0)
            plt.scatter(i, 0, marker="x", c="red")

    plt.xlabel("packet no.")
    plt.ylabel("UL delay / ms")
    plt.plot(x, t)
    plt.show()


def plot_t_ul_hist(data: list[tuple[int, float]]):
    """上行时间直方图"""
    t = []
    for seq, t_ul in data:
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

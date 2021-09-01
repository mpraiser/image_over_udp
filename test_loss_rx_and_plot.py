from net_test_tools.topic import test_loss
from net_test_tools.dataset import preprocess
from net_test_tools.plot import plot_loss


if __name__ == "__main__":
    LOCAL = ("127.0.0.1", 8001)
    REMOTE = ("127.0.0.1", 8000)
    PATH = "dataset.txt"  # dataset的路径，务必保证与另一端一致
    REPEAT = 1  # 将整个dataset循环发送，务必保证与另一端一致
    TIMEOUT = 5  # 接收超时等待时间, None或者一个数，但不能为0；None表示会一直阻塞

    lost = test_loss.receive_for_dataset(LOCAL, REMOTE, PATH, timeout=TIMEOUT, repeat=REPEAT)
    sent = preprocess(PATH, REPEAT)
    plot_loss(sent, lost)

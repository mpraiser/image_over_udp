from topic import test_loss


if __name__ == "__main__":
    LOCAL = ("127.0.0.1", 8000)
    REMOTE = ("127.0.0.1", 8001)
    PATH = "dataset.txt"  # dataset的路径，务必保证与另一端一致
    REPEAT = 1  # 将整个dataset循环发送，务必保证与另一端一致
    INTERVAL = 0.01  # seconds
    RANDOM_TX = False  # 是否主动随机丢弃一些包（50%概率）

    lost_dataset = test_loss.transmit_dataset(
        LOCAL, REMOTE, PATH, interval=INTERVAL, repeat=REPEAT, random_tx=RANDOM_TX
    )

import topic.test_echo.master_async
from topic import test_echo


if __name__ == "__main__":
    LOCAL = ("127.0.0.1", 8000)
    REMOTE = ("127.0.0.1", 8001)
    PACKET_SIZE: int = 1280  # 每个包的（最大）长度，[1, 4096] bytes
    N_PACKET: int = 100  # 总共生成多少个包，[1, 256^256)个
    RANDOM_SIZE: bool = True  # 是否随机长度，如果为True，每个包的长度范围是 [1, PACKET_SIZE]
    TIMEOUT = 5  # 接收超时等待时间, None或者一个数，但不能为0；None表示会一直阻塞
    INTERVAL = 0.1  # seconds

    master = topic.test_echo.master_async.TestEchoLossMasterSync(
        LOCAL, PACKET_SIZE, N_PACKET, random_size=RANDOM_SIZE, timeout=TIMEOUT)
    master.start(REMOTE, interval=INTERVAL)

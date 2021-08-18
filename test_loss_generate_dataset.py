import topic.test_loss.dataset as dataset
from utils import hex_str


if __name__ == "__main__":
    PATH: str = "dataset.txt"  # 生成文件的目标路径
    PACKET_SIZE: int = 128  # 每个包的（最大）长度，[1, 4096] bytes
    N_PACKET: int = 999  # 总共生成多少个包，[1, 256^256)个
    RANDOM_SIZE: bool = True  # 是否随机长度，如果为True，每个包的长度范围是 [1, PACKET_SIZE]

    dataset.generate_file(PATH, PACKET_SIZE, N_PACKET, random_size=RANDOM_SIZE)
    for p in dataset.loaded(PATH):
        print(hex_str(p))
    print(f"Dataset generated in {PATH}")

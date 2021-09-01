from net_test_tools.transceiver import Frame


if __name__ == "__main__":
    f1 = Frame.from_bytes(b"\xff\x00\x03\x00\x00\x00\x01\x02\x03")
    print(f1.to_dict())
    print(f1.to_bytes())

    f2 = Frame.from_dict(f1.to_dict())
    print(f2.to_dict())
    print(f2.to_bytes())

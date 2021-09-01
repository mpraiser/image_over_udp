from common.frame import LinearFrame


def test_reverse():
    spec = {
        "seq": "H",
        "eof": "?",
        "t_master": "d",
        "t_slave": "d",
        "payload": "s"
    }
    lf = LinearFrame(spec)
    f1 = lf.serialize(1234, False, 1629357753.8914032, 0, b"\x00\x01\x02\x03\x04")
    p1 = lf.deserialize(f1)
    f2 = lf.serialize(*p1.values())
    assert f1 == f2
    p2 = lf.deserialize(f2)
    assert p1 == p2

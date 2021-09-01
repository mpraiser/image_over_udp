# net_test_tools

- Test network on transport level, calculate metrics like *packet loss*, *UL/DL delay*, etc.
- Implemented by pure Python, cross-platform.

## Install

Simply use `pip` to install:

```bash
pip install git+git://github.com/mpraiser/net_test_tools
```

Or clone the source code and use `setuptools` to install:

```bash
git clone git://github.com/mpraiser/net_test_tools

cd net_test_tools
python setup.py install
```

## Usage

### udping

Test UL/DL delay (master -> slave -> master) on UDP. Some plot functions are implemented.

The topic udping includes `udping-master` and `udping-slave`, which should be used together.

- `udping-master`

```
Options:
    --local <TEXT INTEGER>...   Address of local.  [required]
    --remote <TEXT INTEGER>...  Address of remote.  [required]
    -ps, --packet_size INTEGER  Max size of each packet.  [required]
    -n, --n_packet INTEGER      Number of packets to transmit.  [required]
    -r, --random_size BOOLEAN   Whether size of each packet is random.
                                [default: True]
    -i, --interval FLOAT        Interval of transmit.  [default: 1.0]
    -ne, --no_echo              Whether only to transmit, meaning lower interval
                                is acceptable.  [default: False]
    --help                      Show this message and exit.
```

- `udping-slave`

```
Options:
    --local <TEXT INTEGER>...   Address of local.  [required]
    --remote <TEXT INTEGER>...  Address of remote.
    -pl, --plot_line_chart      Plot line chart of UL delay.  [default: False]
    -ph, --plot_histogram       Plot histogram of UL delay.  [default: False]
    -ne, --no_echo              Whether to echo.  [default: False]
    --help                      Show this message and exit.
```

Note that master and slave should have same `--no_echo`/`-ne` option.
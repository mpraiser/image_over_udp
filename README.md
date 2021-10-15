# net_test_tools

- Test network on transport level, calculate metrics like *packet loss*, *UL/DL delay*, etc.
- Implemented by pure Python, cross-platform.

## Requirements

- Python 3.9

> `miniconda` is recommended to build a `Python` environment.

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
    Usage: udping-master [OPTIONS]

    Options:
    --local <TEXT INTEGER>...       Address of local.  [required]
    --remote <TEXT INTEGER>...      Address of remote.  [required]
    -ps, --packet_size INTEGER      Max size of each packet.  [required]
    -n, --n_packet INTEGER          Number of packets to transmit.  [required]
    -r, --random_size               Whether size of each packet is random.
                                    [default: False]
    -i, --interval FLOAT            Interval after transmit. Note that this
                                    option has lower priority than
                                    --complex_interval.  [default: 1.0]
    -ci, --complex_interval <INTEGER FLOAT>...
                                    Complex interval, implying how many packets
                                    sent in which interval. This option allows
                                    multiple value, makes transmission in
                                    circulation of each mode.If this option is
                                    set, --interval will not work.
    -ne, --no_echo                  Only to transmit, not to deal with receive.
                                    If set, interval lower than 0.1 is
                                    acceptable.  [default: False]
    --help                          Show this message and exit.
    ```

    1. If `-ci` is set, `-i` will have no effect.
    2. If `-ne` is not set, minimum interval should be around 0.1 sec. 

- `udping-slave`

    ```
    Usage: udping-slave [OPTIONS]

    Options:
    --local <TEXT INTEGER>...   Address of local.  [required]
    --remote <TEXT INTEGER>...  Address of remote.
    -pl, --plot_line_chart      Plot line chart of UL delay.  [default: False]
    -ph, --plot_histogram       Plot histogram of UL delay.  [default: False]
    -ne, --no_echo              Not to echo.  [default: False]
    --help                      Show this message and exit.
    ```

    1. If `-ne` is not set, `--remote` must be set. It's where slave relays to.

Note that master and slave should have same `--no_echo`/`-ne` option.

## Known issues

- aync mode (udping-master with -ne) doesn't work properly with very short intervals under Powershell.
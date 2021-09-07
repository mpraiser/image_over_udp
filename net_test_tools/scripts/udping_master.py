import click

from net_test_tools.topic import udping


@click.command()
@click.option(
    "--local",
    type=(str, int),
    help="Address of local.",
    required=True
)
@click.option(
    "--remote",
    type=(str, int),
    help="Address of remote.",
    required=True
)
@click.option(
    "--packet_size", "-ps",
    type=int,
    help="Max size of each packet.",
    required=True
)
@click.option(
    "--n_packet", "-n",
    type=int,
    help="Number of packets to transmit.",
    required=True
)
@click.option(
    "--random_size", "-r",
    type=bool,
    help="Whether size of each packet is random.",
    default=True,
    show_default=True
)
@click.option(
    "--interval", "-i",
    type=float,
    help="Interval of transmit. Note that this option has lower priority than --complex_interval",
    default=1,
    show_default=True
)
@click.option(
    "--complex_interval", "-ci",
    type=(int, float),
    help="Complex interval, implying how many packets sent in which interval. "
         "If this option is set, --interval will not work.",
    multiple=True
)
@click.option(
    "--no_echo", "-ne",
    type=bool,
    help="Whether only to transmit, meaning lower interval is acceptable.",
    default=False,
    show_default=True,
    is_flag=True
)
def udping_master(
        local: tuple[str, int], remote: tuple[str, int],
        packet_size: int, n_packet: int, random_size: bool,
        interval: float, complex_interval: tuple[int, float], no_echo: bool
):
    tx_only = no_echo
    if len(complex_interval) > 0:
        interval = complex_interval
    print(f"interval is: {interval}")
    udping.run_master(
        local, remote, packet_size, n_packet, random_size=random_size, interval=interval, tx_only=tx_only
    )


if __name__ == "__main__":
    udping_master()

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
    help="Number of packets to transmit. 0 or negative number means infinity.",
    required=True
)
@click.option(
    "--random_size", "-r",
    type=bool,
    help="Whether size of each packet is random.",
    is_flag=True,
    default=False,
    show_default=True
)
@click.option(
    "--interval", "-i",
    type=float,
    help="Interval after transmit. Note that this option has lower priority than --complex_interval.",
    default=1,
    show_default=True
)
@click.option(
    "--complex_interval", "-ci",
    type=(int, float),
    help="Complex interval, implying how many packets sent in which interval. "
         "This option allows multiple value, makes transmission in circulation of each mode."
         "If this option is set, --interval will not work.",
    multiple=True
)
@click.option(
    "--no_echo", "-ne",
    type=bool,
    help="Only to transmit, not to deal with receive. If set, interval lower than 0.1 is acceptable.",
    default=False,
    show_default=True,
    is_flag=True
)
@click.option(
    "--sync", "-s",
    type=bool,
    help="Synchronous transmission. it will disable receiving.",
    default=False,
    show_default=True,
    is_flag=True
)
def udping_master(
        local: tuple[str, int], remote: tuple[str, int],
        packet_size: int, n_packet: int, random_size: bool,
        interval: float, complex_interval: tuple[int, float], no_echo: bool,
        sync: bool
):
    tx_only = no_echo
    interval = complex_interval if len(complex_interval) > 0 else ((1, interval),)
    print(f"interval is: {interval}")
    if n_packet <= 0:
        n_packet = None
    runner = "sync" if sync else "async"
    master = udping.master.UdpingMaster(
        local, remote,
        packet_size, n_packet,
        random_size=random_size, interval=interval, tx_only=tx_only,
        runner=runner
    )
    master.run()


if __name__ == "__main__":
    udping_master()

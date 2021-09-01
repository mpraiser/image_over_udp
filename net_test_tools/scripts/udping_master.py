import click
# from typing import Optional

from net_test_tools.topic import test_ul_dl_delay


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
    default=True
)
@click.option(
    "--interval", "-i",
    type=float,
    help="Interval of transmit.",
    default=1
)
@click.option(
    "--tx_only",
    type=bool,
    help="Whether only to transmit, meaning lower interval is acceptable.",
    default=False
)
def udping_master(
        local: tuple[str, int], remote: tuple[str, int],
        packet_size: int, n_packet: int, random_size: bool,
        interval: float, tx_only: bool
):
    test_ul_dl_delay.run_master(
        local, remote, packet_size, n_packet, random_size=random_size, interval=interval, tx_only=tx_only
    )


if __name__ == "__main__":
    udping_master()

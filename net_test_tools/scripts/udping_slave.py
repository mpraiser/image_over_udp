import click
from typing import Optional

from net_test_tools.topic import udping
from net_test_tools.plot import plot_t_ul, plot_t_ul_hist


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
    default=None,
    show_default=True
)
@click.option(
    "--plot_line_chart", "-pl",
    type=bool,
    help="Plot line chart of UL delay.",
    is_flag=True,
    default=False,
    show_default=True
)
@click.option(
    "--plot_histogram", "-ph",
    type=bool,
    help="Plot histogram of UL delay.",
    is_flag=True,
    default=False,
    show_default=True
)
@click.option(
    "--no_echo", "-ne",
    type=bool,
    help="Whether to echo.",
    is_flag=True,
    default=False,
    show_default=True,
)
def udping_slave(
        local: tuple[str, int], remote: Optional[tuple[str, int]],
        plot_line_chart: bool, plot_histogram: bool,
        no_echo: bool
):
    echo = not no_echo
    slave = udping.slave.Slave()
    try:
        slave.run(
            local, remote, echo=echo
        )
    except KeyboardInterrupt:
        pass

    data = slave.result
    if plot_line_chart:
        plot_t_ul(data)
    if plot_histogram:
        plot_t_ul_hist(data)


if __name__ == "__main__":
    udping_slave()

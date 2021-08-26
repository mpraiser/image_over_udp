"""
test up-link and down-link delay from master -> slave -> master
"""

from .master import run_master
from .slave import run_slave, plot_t_ul, plot_t_ul_hist

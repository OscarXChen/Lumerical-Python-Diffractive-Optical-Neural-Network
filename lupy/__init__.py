import sys, os
from collections import OrderedDict 
from .fdtd_manager import get_fdtd_instance
from .fdtd_manager import setup_paths
from .fdtd_manager import get_existing_fdtd_instance
from .version import version
from .rect import add_rect
from .rect import add_slab
from .source import add_source_plane
from .eri import set_neff_monitor
from .monitor import add_power_monitor

from .simulation import add_simulation_fdtd
from .simulation import add_simulation_fde

def hello():
	print("\t欢迎使用LuPy库"
		  "\n\t这是一个为了方便调用而二次包装Lumerical Python API的库")


def min_span(min, max):
	return (min + max) / 2, max - min


def span_min(pos, span):
	return pos - span / 2, pos + span / 2

def cal_neff(L,Delta_phi):
	pi = 3.1415927
	wavelength = 1.55e-6
	k0 = 2 * pi / wavelength
	neff=wavelength/2/pi/L*Delta_phi
	return neff

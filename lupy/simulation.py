from .fdtd_manager import get_fdtd_instance
from collections import OrderedDict


def add_simulation_fdtd(x=0, y=0, z=0, x_min=0, x_max=0, y_min=0, y_max=0, z_min=0, z_max=0,
						background_material="SiO2 (Glass) - Palik",
						x_min_bc="metal", x_max_bc="metal",
						y_min_bc="metal", y_max_bc="metal",
						z_min_bc="metal", z_max_bc="metal",
						):
	FD = get_fdtd_instance()
	props = OrderedDict([
		("x min", x_min),
		("x max", x_max),
		("y min", y_min),
		("y max", y_max),
		("z min", z_min),
		("z max", z_max),
		("background material", background_material),
		("x min bc", x_min_bc),
		("x max bc", x_max_bc),
		("y min bc", y_min_bc),
		("y max bc", y_max_bc),
		("z min bc", z_min_bc),
		("z max bc", z_max_bc),
	])
	ob_fdtd = FD.addfdtd(properties=props)

	return ob_fdtd


def add_simulation_fde(x=0, y=0, z=0, x_min=0, x_max=0, y_min=0, y_max=0, z_min=0, z_max=0,
					   solver_type="2D Z normal", background_material="SiO2 (Glass) - Palik",
					   x_min_bc="metal", x_max_bc="metal",
					   y_min_bc="metal", y_max_bc="metal",
					   z_min_bc="metal", z_max_bc="metal", ):
	FD = get_fdtd_instance()

	if solver_type == "2D X normal":
		if x_min != x_max:
			print("对待放置的2D X normal仿真，输入的x_min和x_max不相等，这将是其x坐标，请检查！")
		props = OrderedDict([
			("solver type", solver_type),
			("y min", y_min),
			("y max", y_max),
			("z min", z_min),
			("z max", z_max),
			("x", x_min),
			("background material", background_material)])
		ob_mode = FD.addfde(properties=props)
		FD.set("y min bc", y_min_bc)  # 吐槽：奇葩逻辑，设置了y min bc为periodic以后，再设置y max bc就会出错，明明bloch条件都不会
		if y_min_bc != "periodic":
			FD.set("y max bc", y_max_bc)
		FD.set("z min bc", z_min_bc)
		if z_min_bc != "periodic":
			FD.set("z max bc", z_max_bc)
	elif solver_type == "2D Y normal":
		if y_min != y_max:
			print("对待放置的2D Y normal仿真，输入的y_min和y_max不相等，这将是其y坐标，请检查！")
		props = OrderedDict([
			("solver type", solver_type),
			("x min", x_min),
			("x max", x_max),
			("z min", z_min),
			("z max", z_max),
			("y", y_min),
			("background material", background_material),
			("x min bc", x_min_bc),
			("x max bc", x_max_bc),
			("z min bc", z_min_bc),
			("z max bc", z_max_bc)
		])
		ob_mode = FD.addfde(properties=props)
		FD.set("x min bc", x_min_bc)  # 吐槽：奇葩逻辑，设置了y min bc为periodic以后，再设置y max bc就会出错，明明bloch条件都不会
		if x_min_bc != "periodic":
			FD.set("x max bc", x_max_bc)
		FD.set("z min bc", z_min_bc)
		if z_min_bc != "periodic":
			FD.set("z max bc", z_max_bc)
	elif solver_type == "2D Z normal":
		if z_min != z_max:
			print("对待放置的2D Z normal仿真，输入的z_min和z_max不相等，这将是其z坐标，请检查！")
		props = OrderedDict([
			("solver type", solver_type),
			("x min", x_min),
			("x max", x_max),
			("y min", y_min),
			("y max", y_max),
			("z", z_min),
			("background material", background_material),
			("x min bc", x_min_bc),
			("x max bc", x_max_bc),
			("y min bc", y_min_bc),
			("y max bc", y_max_bc)
		])
		ob_mode = FD.addfde(properties=props)
		FD.set("x min bc", x_min_bc)  # 吐槽：奇葩逻辑，设置了y min bc为periodic以后，再设置y max bc就会出错，明明bloch条件都不会
		if x_min_bc != "periodic":
			FD.set("x max bc", x_max_bc)
		FD.set("y min bc", y_min_bc)
		if y_min_bc != "periodic":
			FD.set("y max bc", y_max_bc)
	else:
		print("传入参数simulation_type设置错误，必须为"
			  "\n\t【2D X normal】【2D Y normal】【2D Z normal】"
			  "\n中的一个")
		props = OrderedDict()
		ob_mode = None
	return ob_mode

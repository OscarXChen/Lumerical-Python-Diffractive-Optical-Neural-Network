from .fdtd_manager import get_fdtd_instance


def set_neff_monitor(pre_name="", direction="x", x1_min=0, x1_max=0, y1_min=0, y1_max=0, z1_min=0, z1_max=0, x2_min=0,
					 x2_max=0, y2_min=0, y2_max=0, z2_min=0, z2_max=0):
	FD = get_fdtd_instance()
	if direction == "x":
		ob_moni_1 = FD.addpower()
		FD.set("name", pre_name + "_front")
		FD.set("monitor type", "2D X-normal")
		FD.set("x", x1_min)
		FD.set("y min", y1_min)
		FD.set("y max", y1_max)
		FD.set("z min", z1_min)
		FD.set("z max", z1_max)

		ob_moni_2 = FD.addpower()
		FD.set("name", pre_name + "_back")
		FD.set("monitor type", "2D X-normal")
		FD.set("x", x2_min)
		FD.set("y min", y2_min)
		FD.set("y max", y2_max)
		FD.set("z min", z2_min)
		FD.set("z max", z2_max)
	elif direction == "y":
		ob_moni_1 = FD.addpower()
		FD.set("name", pre_name + "_front")
		FD.set("monitor type", "2D Y-normal")
		FD.set("y", y1_min)
		FD.set("x min", x1_min)
		FD.set("x max", x1_max)
		FD.set("z min", z1_min)
		FD.set("z max", z1_max)

		ob_moni_2 = FD.addpower()
		FD.set("name", pre_name + "_back")
		FD.set("monitor type", "2D Y-normal")
		FD.set("y", y2_min)
		FD.set("x min", x2_min)
		FD.set("x max", x2_max)
		FD.set("z min", z2_min)
		FD.set("z max", z2_max)
	elif direction == "z":
		ob_moni_1 = FD.addpower()
		FD.set("name", pre_name + "_front")
		FD.set("monitor type", "2D Z-normal")
		FD.set("z", z1_min)
		FD.set("x min", x1_min)
		FD.set("x max", x1_max)
		FD.set("y min", y1_min)
		FD.set("y max", y1_max)

		ob_moni_2 = FD.addpower()
		FD.set("name", pre_name + "_back")
		FD.set("monitor type", "2D Z-normal")
		FD.set("z", z2_min)
		FD.set("x min", x2_min)
		FD.set("x max", x2_max)
		FD.set("y min", y2_min)
		FD.set("y max", y2_max)
	else:
		print("输入的计算方向错误")
		ob_moni_1, ob_moni_2 = False, False
	return ob_moni_1, ob_moni_2

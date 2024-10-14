from .fdtd_manager import get_fdtd_instance

u = 1e-6


def add_power_monitor(name="phase", x_min=0, x_max=0, y_min=0, y_max=0, z_min=0, z_max=0,
					  monitor_type="2D Z-normal"):
	FD = get_fdtd_instance()
	ob_power_monitor = FD.addpower()
	FD.set("name", name)

	if monitor_type == "2D X-normal":
		if x_min != x_max:
			print("对待放置的2D X-normal监视器，输入的x_min和x_max不相等，这将是其x坐标，请检查！")
		else:
			FD.set("monitor type", monitor_type)
			FD.set("x", x_min)
			FD.set("y min", y_min)
			FD.set("y max", y_max)
			FD.set("z min", z_min)
			FD.set("z max", z_max)
	elif monitor_type == "2D Y-normal":
		if y_min != y_max:
			print("对待放置的2D Y-normal监视器，输入的y_min和y_max不相等，这将是其y坐标，请检查！")
		else:
			FD.set("monitor type", monitor_type)
			FD.set("y", y_min)
			FD.set("x min", x_min)
			FD.set("x max", x_max)
			FD.set("z min", z_min)
			FD.set("z max", z_max)
	elif monitor_type == "2D Z-normal":
		if z_min != z_max:
			print("对待放置的2D Z-normal监视器，输入的z_min和z_max不相等，这将是其z坐标，请检查！")
		else:
			FD.set("monitor type", monitor_type)
			FD.set("x min", x_min)
			FD.set("x max", x_max)
			FD.set("y min", y_min)
			FD.set("y max", y_max)
			FD.set("z", z_min)
	elif monitor_type == "Linear X":
		if y_min != y_max or z_min != z_max:
			print("对待放置的Linear X监视器，输入的y_min和y_max，和（或）z_min和z_max不相等，这将是其y，z坐标，请检查！")
		else:
			FD.set("monitor type", monitor_type)
			FD.set("x min", x_min)
			FD.set("x max", x_max)
			FD.set("y", y_min)
			FD.set("z", z_min)
	elif monitor_type == "Linear Y":
		if x_min != x_max or z_min != z_max:
			print("对待放置的Linear Y监视器，输入的x_min和x_max，和（或）z_min和z_max不相等，这将是其x，z坐标，请检查！")
		else:
			FD.set("monitor type", monitor_type)
			FD.set("y min", y_min)
			FD.set("y max", y_max)
			FD.set("x", x_min)
			FD.set("z", z_min)
	elif monitor_type == "Linear Z":
		if x_min != x_max or y_min != y_max:
			print("对待放置的Linear Z监视器，输入的x_min和x_max，和（或）y_min和y_max不相等，这将是其x，y坐标，请检查！")
		else:
			FD.set("monitor type", monitor_type)
			FD.set("z min", z_min)
			FD.set("z max", z_max)
			FD.set("x", x_min)
			FD.set("y", y_min)
	else:
		print("传入参数monitor_type设置错误，必须为"
			  "\n\t【2D X-normal】【2D Y-normal】【2D Z-normal】"
			  "\n\t【Linear X】【Linear Y】【Linear Z】\n中的一个")
	return ob_power_monitor

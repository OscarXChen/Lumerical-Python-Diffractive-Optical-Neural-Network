from .fdtd_manager import get_fdtd_instance

u = 1e-6


def add_source_plane(x, z=0 * u, z_span=5 * u, y=0, y_span=1 * u):
	FD = get_fdtd_instance()
	ob_plane = FD.addplane()
	FD.set("injection axis", "x")
	FD.set("direction", "forward")
	FD.set("x", x)
	FD.set("z", z)
	FD.set("z span", z_span)
	FD.set("y", y)
	FD.set("y span", y_span)
	FD.set("wavelength start", 1.55 * u)
	FD.set("wavelength stop", 1.55 * u)
	FD.set("angle phi", 90)
	return ob_plane

def add_source_mode(x_min=0, x_max=0, y_min=0, y_max=0, z_min=0, z_max=0, injection_axis="x", direction="forward"):
	FD = get_fdtd_instance()
	ob_source_mode_plane = FD.addmode()
	if injection_axis == "x":
		FD.set("x", x_min)
		FD.set("y min", y_min)
		FD.set("y max", y_max)
		FD.set("z min", z_min)
		FD.set("z max", z_max)
	if injection_axis == "y":
		FD.set("y", y_min)
		FD.set("x min", x_min)
		FD.set("x max", x_max)
		FD.set("z min", z_min)
		FD.set("z max", z_max)
	if injection_axis == "z":
		FD.set("z", y_min)
		FD.set("x min", x_min)
		FD.set("x max", x_max)
		FD.set("y min", y_min)
		FD.set("y max", y_max)
	FD.set("injection axis", injection_axis)
	FD.set("direction", direction)
	FD.set("wavelength start", 1.55 * u)
	FD.set("wavelength stop", 1.55 * u)
	# FD.set("angle phi", 90)
	return ob_source_mode_plane
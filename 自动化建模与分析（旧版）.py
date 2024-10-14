import sys, os
from collections import OrderedDict  # 这种写法要手动引入，也很烦

api_path = r"C:\Program Files\Lumerical\v241\api\python".replace("\\", "/")
file_path = r"E:\0_Work_Documents\Simulation\05_single_slot".replace("\\", "/")
file_name = r"5.3_slot_structure_single.fsp"
# file_name = r"5.5._mode_single_slot.lms"
sys.path.append(os.path.normpath(api_path))  # 添加Win默认路径
sys.path.append(os.path.dirname(__file__))
import lumapi  # 该行必须在路径添加下面


def u_print(*args, **kwargs):
	'''
	把1e-6变为μ，输出更美观
	:param args:
	:param kwargs:
	:return:
	'''

	def format_scientific_notation(value):
		# 将科学计数法转换为浮点数
		if isinstance(value, str):
			value = float(value)
		if isinstance(value, float):
			# 检查是否为1e-06数量级的值
			if 1e-07 < abs(value) < 1e-05:
				return f"{value * 1e6:.3f} μ"
		return value

	# 将args中的每个元素进行格式化
	formatted_args = [format_scientific_notation(str(arg)) for arg in args]
	# 调用原生的print函数
	print(*formatted_args, **kwargs)


u = 1 * 10 ** -6  # micron
pi = 3.1415927
# import math
# import sympy
width = 0.2 * u
height = 0.22 * u
period = 0.5 * u
distance = 5 * u
wavelength = 1.55 * u
source_x_min = -0.5 * u
length_ls = [1 * u, 2 * u, 1.5 * u,
			 1.7 * u, 1 * u, 2 * u]
			# 0.862 * u, 1.437 * u, 0.287 * u]
# length_ls = [1 * u]
# length_ls = [1.437 * u,0.862 * u ,0.287 * u]
# length_ls = [0.287 * u]
# length_ls = [1.437 * u]
# L_pi_fu14 = 0.287 * u
# L_pi_fu34 = 0.862 * u
# L_pi_fu54 = 1.437 * u
group_num = 2  # 单槽组的槽数
layer_num = 2  # 衍射网络的层数
k0 = 2 * pi / wavelength
neff = 2.166
nslab = 2.84

with lumapi.FDTD(filename=os.path.join(file_path, file_name), hide=False) as FD:  # 打开仿真工程文件，PP=Patent Picture
	# fdtd = lumapi.FDTD()  #开启FDTD会话
	print("开始建模")


	def new_slot(name="", x_min=0, x_max=0, y=0, y_span=width, z_min=0, z_max=0, material="SiO2 (Glass) - Palik"):
		props = OrderedDict([
			("name", name),
			("x min", x_min),
			("x max", x_max),
			("y", y),
			("y span", y_span),
			("z min", z_min),
			# ("z min", 0),
			("z max", z_max),
		])
		ob_slot = FD.addrect(properties=props)
		FD.set("material", material)  # 吐槽：addrect()函数居然没有材料属性
		return ob_slot


	def add_slots():
		FD.addstructuregroup(name="slots")
		FD.set("x", 0)
		FD.set("y", 0)
		FD.set("z", 0)
		x = 0  # 从x=0开始放槽
		y = 0  # 从y=0开始放槽
		length_pin = 0  # 用于位移槽长列表的指针
		name_series_slot = "slot"
		name_series_phase = "phase"
		for j in range(layer_num):  # 放完一层放下一层
			y = width / 2
			name_layer_slot = name_series_slot + f"{j}"
			name_layer_phase = name_series_phase + f"{j}"
			group_count = 0  # 用于辅助计数槽组是否放置完毕的中间变量
			for i in range(int(group_num * len(length_ls) / layer_num)):  # 放完一个放下一个
				name_slot = name_layer_slot + f"{i}"
				name_phase = name_layer_phase + f"{i}"
				new_slot(name_slot,
						 x_min=x, x_max=x + length_ls[length_pin],
						 y=y, y_span=width,
						 z_min=0, z_max=height+0.1*u,
						 material="SiO2 (Glass) - Palik")
				FD.addtogroup("slots")
				add_power_monitor(name_phase + "_front", monitor_type="2D X-normal", x_min=x, x_max=x,
								  y_min=y - width / 2, y_max=y + width / 2, z_min=0, z_max=height)
				# FD.addtogroup("slots")
				add_power_monitor(name_phase + "_back", monitor_type="2D X-normal", x_min=x + length_ls[length_pin],
								  x_max=x + length_ls[length_pin], y_min=y - width / 2, y_max=y + width / 2, z_min=0,
								  z_max=height)
				# FD.addtogroup("slots")
				add_power_monitor(name_phase + "_oversee", monitor_type="2D Z-normal", x_min=x,
								  x_max=x + length_ls[length_pin], y_min=y - width / 2, y_max=y + width / 2,
								  z_min=height / 2,
								  z_max=height / 2)
				# FD.addtogroup("slots")
				add_linear_monitor(name=name_phase + "_middle", x_min=x, x_max=x + length_ls[length_pin], y_min=y,
								   y_max=y,
								   z_min=height / 2, z_max=height / 2)
				group_count = group_count + 1
				if group_count % group_num == 0:
					length_pin = length_pin + 1
				y = y + period  # 向z正方向放置下一个槽
			x = x + distance  # 向x正方形放置下一个层
		return x, y  # 返回此时的x和y，便于后续设定仿真区域大小和自动放监视器


	def add_plane(x, z=0 * u, z_span=5 * u, y=0, y_span=1 * u):
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


	def add_fdtd(name="", x=0, y=0, z=0, x_min=0, x_max=0, y_min=0, y_max=0, z_min=0, z_max=0):
		props = OrderedDict([
			# ("name", name),
			# ("x", x),
			("x min", x_min),
			("x max", x_max),
			# ("y", y),
			("y min", y_min),
			("y max", y_max),
			# ("z", z),
			("z min", z_min),
			("z max", z_max),
			("background material", "Si (Silicon) - Palik"),
			("z min bc", "metal"),
			("z max bc", "metal"),
			("y min bc", "period"),
			("y max bc", "period")
		])
		ob_fdtd = FD.addfdtd(properties=props)
		return ob_fdtd


	def add_mode(name="", x=0, y=0, z=0, x_min=0, x_max=0, y_min=0, y_max=0, z_min=0, z_max=0):
		props = OrderedDict([
			("name", name),
			# ("x", x),
			("x min", x_min),
			("x max", x_max),
			# ("y", y),
			("y min", y_min),
			("y max", y_max),
			# ("z", z),
			("z min", z_min),
			("z max", z_max),
			("background material", "Si (Silicon) - Palik"),
			("z min bc", "metal"),
			("z max bc", "metal"),
			("y min bc", "period"),
			("y max bc", "period")
		])
		ob_fdtd = FD.addmode(properties=props)
		FD.set("solver type", "2D X normal")
		return ob_fdtd


	def add_monitors():
		# 添加全局监视器，看场俯视图
		ob_moni_glo = FD.addpower()
		FD.set("name", "global")
		FD.set("monitor type", "2D Z-normal")
		FD.set("x min", fdtd_x_min)
		FD.set("x max", fdtd_x_max)
		FD.set("y min", fdtd_y_min)
		FD.set("y max", fdtd_y_max)
		FD.set("z", (fdtd_z_max + fdtd_z_min) / 2)
		# 添加前监视器，看场相位图
		ob_moni_fro = FD.addpower()
		FD.set("name", "front")
		FD.set("monitor type", "2D X-normal")
		FD.set("x", 0)
		FD.set("y min", fdtd_y_min)
		FD.set("y max", fdtd_y_max)
		FD.set("z min", fdtd_z_min)
		FD.set("z max", fdtd_z_max)
		# 添加后监视器，看场相位图
		ob_moni_bac = FD.addpower()
		FD.set("name", "back")
		FD.set("monitor type", "2D X-normal")
		FD.set("x", length_ls[0])
		FD.set("y min", fdtd_y_min)
		FD.set("y max", fdtd_y_max)
		FD.set("z min", fdtd_z_min)
		FD.set("z max", fdtd_z_max)

		return ob_moni_glo, ob_moni_fro, ob_moni_bac


	# return ob_moni_glo
	def add_linear_monitor(name="", monitor_type="Linear X", x_min=0, x_max=0, y_min=0, y_max=0, z_min=0, z_max=0):
		# 添加中轴监视器，看相位变化
		ob_moni_midd = FD.addpower()
		FD.set("name", name)
		FD.set("monitor type", monitor_type)
		FD.set("x min", x_min)
		FD.set("x max", x_max)
		FD.set("y min", y_min)
		FD.set("y max", y_max)
		FD.set("z min", z_min)
		FD.set("z max", z_max)
		# FD.set("y", (fdtd_y_min + fdtd_y_max) / 2)
		# FD.set("y", width/2)
		# FD.set("z", (fdtd_z_max + fdtd_z_min) / 2)
		return ob_moni_midd


	def add_power_monitor(name="phase", x_min=0, x_max=0, y_min=0, y_max=0, z_min=0, z_max=0,
						  monitor_type="2D Z-normal"):
		ob_power_phase = FD.addpower()
		FD.set("name", name)
		FD.set("monitor type", monitor_type)
		FD.set("x min", x_min)
		FD.set("x max", x_max)
		FD.set("y min", y_min)
		FD.set("y max", y_max)
		FD.set("z min", z_min)
		FD.set("z max", z_max)
		return ob_power_phase


	def add_buried_and_substrate(buried_width=0.1 * u, substrate_width=5 * u):
		FD.addstructuregroup(name="buried layer")
		FD.set("x", 0)
		FD.set("y", 0)
		FD.set("z", 0)
		props = OrderedDict([
			("name", "buried layer"),
			("x min", fdtd_x_min),
			("x max", fdtd_x_max),
			("y min", fdtd_y_min),
			("y max", fdtd_y_max),
			("z min", -buried_width),
			("z max", fdtd_z_min),
		])
		ob_barried = FD.addrect(properties=props)
		FD.set("material", "SiO2 (Glass) - Palik")  # 吐槽：addrect()函数居然没有材料属性
		FD.addtogroup("buried layer")

		FD.addstructuregroup(name="substrate layer")
		props = OrderedDict([
			("name", "substrate layer"),
			("x min", fdtd_x_min),
			("x max", fdtd_x_max),
			("y min", fdtd_y_min),
			("y max", fdtd_y_max),
			("z min", -substrate_width),
			("z max", -buried_width),
		])
		ob_substrate = FD.addrect(properties=props)
		FD.set("material", "Si (Silicon) - Palik")  # 吐槽：addrect()函数居然没有材料属性
		FD.addtogroup("substrate layer")
		return ob_barried, ob_substrate


	def add_slab():
		FD.addstructuregroup(name="slab")
		FD.set("x", 0)
		FD.set("y", 0)
		FD.set("z", 0)
		props = OrderedDict([
			("name", "slab layer"),
			("x min", fdtd_x_min),
			("x max", fdtd_x_max),
			("y min", fdtd_y_min),
			("y max", fdtd_y_max),
			("z min", fdtd_z_min),
			("z max", fdtd_z_max),
		])
		ob_slab = FD.addrect(properties=props)
		FD.set("material", "Si (Silicon) - Palik")  # 吐槽：addrect()函数居然没有材料属性
		FD.set("override mesh order from material database", 1)
		FD.set("mesh order", 3)
		FD.addtogroup("slab")
		return ob_slab


	fdtd_x_min = source_x_min - 1 * u
	# fdtd_x_max = 5 * u
	fdtd_y_min = 0 * u
	# fdtd_y_max = 0.22 * u
	fdtd_z_min = 0 * u
	fdtd_z_max = 0.22 * u

	FD.switchtolayout()
	FD.deleteall()

	x_slot_max, y_slot_max = add_slots()  # 添加槽，参数过多直接用全局变量好了

	fdtd_x_max = x_slot_max
	fdtd_y_max = y_slot_max
	add_plane(x=-0.5 * u,
			  z=(fdtd_z_min + fdtd_z_max) / 2, z_span=(fdtd_z_max - fdtd_z_min) * 2,
			  y=(fdtd_y_min + fdtd_y_max) / 2, y_span=(fdtd_y_max - fdtd_y_min) * 2)  # 添加平面波光源
	add_fdtd(x_min=fdtd_x_min, x_max=fdtd_x_max,
			 y_min=fdtd_y_min, y_max=fdtd_y_max,
			 z_min=fdtd_z_min, z_max=fdtd_z_max)  # 添加fdtd仿真区域
	add_monitors()
	add_buried_and_substrate(buried_width=0.1 * u, substrate_width=5 * u)  # 为了避免仿真文件尺寸太大，衬底就5μ意思一下
	add_slab()  # 根据仿真区域生成Si板
	print("\n\n")
	FD.run()
	FD.save()


	# input("程序执行完毕，输入回车后结束")
	# # ---------------画图看结果结束---------------
	# input("程序执行完毕，输入回车后结束")

	# 注意！该文件的gds导出文件有问题，z轴不知道写多少，同时掩埋层似乎导出失败了

	# 3个slot映射为1个神经元，一共6个slot
	# 尝试varFDTD

	print("\n\n\n【自动建模结束，开始自动分析】\n\n\n")

	import sys, os
	import numpy as np

	# api_path = r"C:\Program Files\Lumerical\v241\api\python".replace("\\", "/")
	# file_path = r"E:\0_Work_Documents\Simulation\05_single_slot\saved_data".replace("\\", "/")
	# file_name = r"5.3_slot_structure_single.fsp"
	# sys.path.append(os.path.normpath(api_path))  # 添加Win默认路径
	# sys.path.append(os.path.dirname(__file__))
	# import lumapi  # 该行必须在路径添加下面

	# ---------------画图用---------------
	import matplotlib.pyplot as plt
	from matplotlib.ticker import FuncFormatter

	plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用 SimHei 字体
	plt.rcParams['axes.unicode_minus'] = False  # 解决坐标轴负号显示问题


	def drawplot(data, ax=[], extent=[], micron=False, title="", xlabel="", ylabel="", colorbar_name="", cmap='jet',
				 interpolation='none'):
		'''
		:param ax: 子图轴
		:param data:默认二维数据
		:param extent: 范围，接收一个列表，[xmin,xmax,ymin,ymax]
		:param title: 标题名
		:colorbar_name: 颜色条名字
		:param cmap: 颜色映射方案
		:param interpolation: 是否插值
		:return: 画图
		'''
		if ax != []:
			if extent != []:
				im = ax.imshow(data, cmap=cmap, interpolation=interpolation, extent=extent)
			else:
				im = ax.imshow(data, cmap=cmap, interpolation=interpolation)
			cbar = plt.colorbar(im, ax=ax, label=colorbar_name)  # 添加颜色条
			ax.set_title(title)
			ax.set_xlabel(xlabel)
			ax.set_ylabel(ylabel)
			if micron:
				# 设置轴刻度格式为1e-6
				formatter = FuncFormatter(lambda x, _: f'{x * 1e6:.2f}')
				ax.xaxis.set_major_formatter(formatter)
				ax.yaxis.set_major_formatter(formatter)
		else:
			if extent != []:
				print(extent)
				plt.imshow(data, cmap=cmap, interpolation=interpolation,
						   extent=extent)
			else:
				plt.imshow(data, cmap=cmap, interpolation=interpolation,
						   )
			plt.colorbar(label=colorbar_name)  # 添加颜色条
			plt.title(title)
			plt.xlabel(xlabel)
			plt.ylabel(ylabel)
			if micron == True:
				# 设置轴刻度格式为1e-6
				formatter = FuncFormatter(lambda x, _: f'{x * 1e6:.2f}')
				plt.gca().xaxis.set_major_formatter(formatter)
				plt.gca().yaxis.set_major_formatter(formatter)


	# ---------------画图用结束---------------

	# ---------------使用api读取仿真结果开始---------------
	# with lumapi.FDTD(filename=os.path.join(file_path, file_name), hide=True) as FD:  # 打开仿真工程文件
	# fdtd = lumapi.FDTD()  #开启FDTD会话
	group_name = "slot"
	num_slot = 3
	name = ""
	name_ls = []
	layer_num = 2
	slots_num = 3
	y_ticks_ls = []
	z_ticks_ls = []
	Ez_front_ls = []
	Ez_back_ls = []
	for i in range(layer_num):
		for j in range(slots_num):
			# slot_name_temp = group_name + "::" + "phase" + f"{i}{j}"
			slot_name_temp = "phase" + f"{i}{j}"
			y_ticks_ls.append(
				FD.getresult(slot_name_temp + "_front", "y"))  # 从组slot中选择监视器phase_11的y数据
			z_ticks_ls.append(
				FD.getresult(slot_name_temp + "_front", "z"))  # 从组slot中选择监视器phase_11的y数据
			Ez_front_ls.append(FD.getresult(slot_name_temp + "_front", "Ez"))  # 从组slot1中选择监视器phase_11的Ey数据
			Ez_back_ls.append(FD.getresult(slot_name_temp + "_back", "Ez"))  # 从组slot1中选择监视器phase_11的Ey数据
# input("输入回车关闭Lumerical GUI\n")
# input("输入回车以继续")
# ---------------使用api读取仿真结果结束---------------

# print(Ez11_ls[0].shape[1])
# print(Ez11_ls[0].shape[2])
#
# # ---------------提取相位部分开始---------------
# # 旋转是为了使得图的横纵坐标轴和仿真程序里保持一致
# # 使用np.angle()计算Ey复振幅的相位角
# # reshape是为了将(1,6,6,1)的原始高维数组转换为便于绘图的(6,6)二维数组
Phase_front_ls = []
Phase_back_ls = []
Delta_ls = []
pin_temp = 0  # 使用临时指针pin_temp，便于在排成了一维列表的数据中找到特定的那个数据
for i in range(layer_num):
	for j in range(slots_num):
		pin_temp = i * slots_num + j
		Phase_front_ls.append(np.rot90(np.angle(Ez_front_ls[pin_temp])
									   .reshape(Ez_front_ls[pin_temp].shape[1],
												Ez_front_ls[pin_temp].shape[2])))
		Phase_back_ls.append(np.rot90(np.angle(Ez_back_ls[pin_temp])
									  .reshape(Ez_back_ls[pin_temp].shape[1],
											   Ez_back_ls[pin_temp].shape[2])))
		Delta_ls.append(Phase_back_ls[pin_temp] - Phase_front_ls[pin_temp])

# # ---------------提取相位部分结束---------------
#
#
# # print(Phase11) # 可见，和原始仿真结果一致
#
# ---------------画图看结果开始---------------
# 第一张图测试用
# drawplot(data=Phase_front_ls[0],ax=[], extent=[y_ticks_ls[0].min(), y_ticks_ls[0].max(), z_ticks_ls[0].min(), z_ticks_ls[0].max()],
# title="第1个硅槽波导\n相位分布（前）", xlabel='Y 轴(μm)', ylabel='Z 轴(μm)', micron=True)
# drawplot(Delta_ls[0], extent=[y_ticks_ls[0].min(), y_ticks_ls[0].max(), z_ticks_ls[0].min(), z_ticks_ls[0].max()],
# 		 title="第1个硅槽波导\n相位分布（前）", xlabel='Y 轴(μm)', ylabel='Z 轴(μm)', micron=True)

# # 创建一个3x2的子图布局
fig, axs = plt.subplots(3, 2, figsize=(12, 8))
# print(len(Delta_ls))
#
# 绘制每个子图
# for i in range(len(Delta_ls)):
for i in range(3):
	for j in range(2):
		if j % 2 == 0:
			drawplot(Phase_front_ls[i], ax=axs[i, j],
					 extent=[y_ticks_ls[i].min(), y_ticks_ls[i].max(), z_ticks_ls[i].min(),
							 z_ticks_ls[i].max()],
					 title=f"第{i}个硅槽波导\n相位分布（前）",
					 xlabel='Y 轴(μm)', ylabel='Z 轴(μm)', micron=True)
		else:
			drawplot(Delta_ls[i], ax=axs[i, j],
					 extent=[y_ticks_ls[i].min(), y_ticks_ls[i].max(), z_ticks_ls[i].min(),
							 z_ticks_ls[i].max()],
					 title=f"第{i}个硅槽波导\n相位差分布",
					 xlabel='Y 轴(μm)', ylabel='Z 轴(μm)', micron=True)

# drawplot(Phase11, ax=axs[0, 0], extent=[y_ticks.min(), y_ticks.max(), z_ticks.min(), z_ticks.max()],
# 		 title="第2个硅槽波导\n相位分布（前）", xlabel='Y 轴(μm)', ylabel='Z 轴(μm)', micron=True)
#
# drawplot(Delta1, ax=axs[0, 1], extent=[y_ticks.min(), y_ticks.max(), z_ticks.min(), z_ticks.max()],
# 		 title="第2个硅槽波导\n相位差分布（参考值：π/2=1.57）", xlabel='Y 轴(μm)', ylabel='Z 轴(μm)', micron=True)
#
# drawplot(Phase21, ax=axs[1, 0], extent=[y_ticks.min(), y_ticks.max(), z_ticks.min(), z_ticks.max()],
# 		 title="第3个硅槽波导\n相位分布（前）", xlabel='Y 轴(μm)', ylabel='Z 轴(μm)', micron=True)
#
# drawplot(Delta2, ax=axs[1, 1], extent=[y_ticks.min(), y_ticks.max(), z_ticks.min(), z_ticks.max()],
# 		 title="第3个硅槽波导\n相位差分布（参考值：π/2=1.57）", xlabel='Y 轴(μm)', ylabel='Z 轴(μm)', micron=True)
#
# drawplot(Phase31, ax=axs[2, 0], extent=[y_ticks.min(), y_ticks.max(), z_ticks.min(), z_ticks.max()],
# 		 title="第4个硅槽波导\n相位分布（前）", xlabel='Y 轴(μm)', ylabel='Z 轴(μm)', micron=True)
#
# drawplot(Delta3, ax=axs[2, 1], extent=[y_ticks.min(), y_ticks.max(), z_ticks.min(), z_ticks.max()],
# 		 title="第4个硅槽波导\n相位差分布（参考值：π/2=1.57）", xlabel='Y 轴(μm)', ylabel='Z 轴(μm)', micron=True)
#
plt.tight_layout()  # 调整布局以避免重叠
#
plt.show()
# ---------------画图看结果结束---------------
# input("程序执行完毕，输入回车后结束")

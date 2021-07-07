import numpy as np
from copy import deepcopy
from matplotlib import pyplot as plt

from Code import PointProcess as PP
from Code import InIReaWri

np.warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)

# zdt_loc = r"Data\Sample\Resp\ZP0EBD1119121701RIA_223.zdt"
zdt_loc = InIReaWri.ConfigR("FileTestRoute", "WaveRead_zdt", conf=None)

info_list = PP.PointProcessing(zdt_loc)

wave_data = np.array([[0], [], []])

# TODO 更改array下的每一个元素的地址

start_index = info_list[0]
F = info_list[2]
P = info_list[3]
V = info_list[4]

for i in range(start_index[2], start_index[8]):
    wave_data[0] = np.append(wave_data[0], F[i])
    wave_data[1] = np.append(wave_data[1], P[i])
    wave_data[2] = np.append(wave_data[2], V[i])

fig, axs = plt.subplots(3)
fig.suptitle("F & P & V")
axs[0].plot(wave_data[0])
axs[1].plot(wave_data[1])
axs[2].plot(wave_data[2])
plt.show()
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.animation import FuncAnimation

# 建立畫布和坐標軸
fig, ax = plt.subplots()

# 設定坐標軸範圍
ax.set_xlim(0, 2 * np.pi)
ax.set_ylim(-1.5, 1.5)

# 建立正弦波形
x = np.linspace(0, 2 * np.pi, 1000)
y = np.sin(x)

# 繪製正弦波形
ax.plot(x, y, color="blue")

# 建立紅色球
circle = Circle((0, 0), radius=0.1, color="red")

# 添加紅色球到圖形中
ax.add_patch(circle)


# 更新紅色球的位置
def update(frame):
    # 以 2π 為單位重複移動紅色球，np.sin函數會自動將角度映射到 -1 到 1 的範圍
    circle.center = (2 * np.pi * (frame / 100), np.sin(2 * np.pi * (frame / 100)))
    return (circle,)


# 建立動畫
ani = FuncAnimation(fig, update, frames=100, blit=True)

# 顯示動畫
plt.show()
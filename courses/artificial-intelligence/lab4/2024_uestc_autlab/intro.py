import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(15, 7))
ax.axis('off')

x_shift = 1.6
modules = [
    (0 + x_shift, 2, 'Sensors\n(RealSense D430,\nIMU)', '#E3F2FD'),
    (2.5 + x_shift, 2, 'Stereo-Inertial\nState Estimation\n(VINS-Fusion)', '#BBDEFB'),
    (5 + x_shift, 2, 'Environment Mapping\n(Voxel Grid)', '#C8E6C9'),
    (7.5 + x_shift, 2, 'Local Trajectory\nPlanning\n(EGO-Planner)', '#FFECB3'),
    (10 + x_shift, 2, 'Flight Control\n(PX4, MAVROS,\nPX4ctrl Node)', '#FFE0B2'),
    (12.5 + x_shift, 2, 'UAV Actions\n(Vortex Edge.py)', '#B2DFDB'),
    (7.5 + x_shift, 0.2, 'Visualization\n(RViz)', '#D1C4E9'),
]

box_w, box_h = 2.0, 1.2

# Draw modules
for x, y, label, color in modules:
    rect = patches.FancyBboxPatch(
        (x - box_w/2, y - box_h/2), box_w, box_h,
        boxstyle="round,pad=0.07", edgecolor='#222', facecolor=color, lw=2)
    ax.add_patch(rect)
    ax.text(x, y, label, ha='center', va='center', fontsize=12, fontweight='bold', color="#111")

# 主流程箭头（横向）
for i in range(6-1):
    x0, y0, *_ = modules[i]
    x1, y1, *_ = modules[i+1]
    ax.annotate('', xy=(x1-box_w/2, y1), xytext=(x0+box_w/2, y0),
                arrowprops=dict(arrowstyle="->", lw=2.1, color='#222'))

# RViz虚线箭头
for idx in [2, 3, 4]:
    x, y, *_ = modules[idx]
    ax.annotate('', xy=(modules[6][0], modules[6][1]+box_h/2),
                xytext=(x, y-box_h/2),
                arrowprops=dict(arrowstyle="->", lw=1.7, color='#555', linestyle='dashed'))


plt.xlim(-1, 17)
plt.ylim(-1, 3.7)
plt.tight_layout()
plt.savefig("uav_navigation_system_final_with_script.png", dpi=200)
plt.show()

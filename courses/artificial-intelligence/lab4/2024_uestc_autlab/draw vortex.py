import matplotlib.pyplot as plt
import matplotlib.patches as patches

steps = [
    "Start", "Initialize ROS Node", "Takeoff",
    "Read Waypoints File", "Send Waypoint 1", "Send Waypoint 2",
    "Send Waypoint 3", "Land", "Finish"
]
row_length = 3
colors = ["#E3F2FD", "#E3F2FD", "#E3F2FD", "#FFECB3", "#FFECB3", "#FFECB3", "#FFECB3", "#C8E6C9", "#C8E6C9"]

fig, ax = plt.subplots(figsize=(13, 6))
ax.axis('off')

box_w, box_h = 2.2, 0.95
vspace = 1.7
hspace = 2.6
x_offset = 1.2

positions = []
arrows = []
direction = 1
row, col = 0, 0

for idx, step in enumerate(steps):
    if direction == 1:
        x = col * hspace + x_offset
    else:
        x = (row_length - 1 - col) * hspace + x_offset
    y = -row * vspace
    positions.append((x, y, step, row, idx))

    if idx > 0:
        prev_x, prev_y, _, prev_row, prev_idx = positions[idx - 1]
        if row == prev_row:  # 横向箭头
            if direction == 1:
                # 行内左到右
                arrows.append(((prev_x + box_w / 2, prev_y), (x - box_w / 2, y)))
            else:
                # 行内右到左
                arrows.append(((prev_x - box_w / 2, prev_y), (x + box_w / 2, y)))
        else:  # 跨行用竖直箭头
            arrows.append(((prev_x, prev_y - box_h / 2), (x, y + box_h / 2)))

    col += 1
    if col == row_length:
        row += 1
        col = 0
        direction *= -1

# 绘制节点
for x, y, text, row, idx in positions:
    rect = patches.FancyBboxPatch(
        (x - box_w / 2, y - box_h / 2), box_w, box_h,
        boxstyle="round,pad=0.07", edgecolor='#222', facecolor=colors[idx], lw=2)
    ax.add_patch(rect)
    ax.text(x, y, text, ha='center', va='center', fontsize=13, fontweight='bold', color="#111")

# 绘制箭头
for (x0, y0), (x1, y1) in arrows:
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="->", lw=2.1, color='#222'))

ax.set_xlim(-0.5, row_length * hspace + x_offset + 1.5)
ax.set_ylim(-vspace * (len(steps) // row_length + 0.5), 1)
plt.tight_layout()
plt.savefig("snake_flowchart_final_perfect.png", dpi=200)
plt.show()

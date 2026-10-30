import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

print("Generating Gantt chart with detailed future plan...")

# --- 1. Define Your Task Data (Detailed Future Plan) ---
# Status: 'done' (已完成), 'active' (进行中), 'crit' (计划中)
tasks_data = [
    # === Phase 1: Foundation & Baseline (Completed in Oct) ===
    ("PyTorch & CNN Basics", "2024-10-01", "2024-10-07", "done"),
    ("U-Net Paper & Architecture Study", "2024-10-09", "2024-10-17", "done"),
    ("Research U-Net Variants & Select nnU-Net", "2024-10-17", "2024-10-24", "done"),
    ("Setup nnU-Net v2 Environment & Debug", "2024-10-24", "2024-10-24", "done"),
    ("Experiment 1: Establish Baseline (150 epochs)", "2024-10-25", "2024-10-26", "done"),
    ("Experiment 2: Test CLAHE-enhanced Dataset", "2024-10-27", "2024-10-27", "done"),

    # === Phase 2: Core Innovation (Detailed & Dense Plan) ===
    # (Assuming today is Oct 30, this is the 'active' phase)
    ("Literature Review on Loss Functions (Dice, Focal, Tversky...)", "2024-10-29", "2024-11-08", "active"),
    ("Propose Novel/Hybrid Loss Function (Hypothesis)", "2024-11-09", "2024-11-15", "crit"),
    ("Implementation: Code New Loss in nnU-Net Framework", "2024-11-16", "2024-11-22", "crit"),
    ("Experiment 3: Initial Training & Debugging (Iteration 1)", "2024-11-23", "2024-12-01", "crit"),
    ("Hyperparameter Tuning (Adjusting loss weights, LR)", "2024-12-02", "2024-12-15", "crit"),
    ("Analyze Iteration 1 Results vs. Baseline", "2024-12-16", "2024-12-22", "crit"),

    # === Phase 3: Ablation Studies & Optimization (More Credible) ===
    ("Ablation Study 1: Compare Baseline vs. Dice vs. NewLoss", "2025-01-02", "2025-01-15", "crit"),
    ("Ablation Study 2: Test Impact of Data Augmentation", "2025-01-16", "2025-01-31", "crit"),
    ("(Optional) Architecture Tweak (e.g., add Attention)", "2025-02-01", "2025-02-07", "crit"),
    ("Final Model Training & Validation", "2025-02-08", "2025-02-28", "crit"),

    # === Phase 4: Thesis Writing & Defense (Detailed) ===
    ("Final Evaluation on Test Set", "2025-03-01", "2025-03-07", "crit"),
    ("Result Analysis & Visualization (Generate Figures/Tables)", "2025-03-08", "2025-03-21", "crit"),
    ("Write Thesis (Draft 1: Methods & Results)", "2025-03-22", "2025-04-11", "crit"),
    ("Write Thesis (Draft 2: Intro, Lit Review, Conclusion)", "2025-04-12", "2025-04-30", "crit"),
    ("Submit to Supervisor & Get Feedback", "2025-05-01", "2025-05-15", "crit"),
    ("Final Revisions & Thesis Submission", "2025-05-16", "2025-05-31", "crit"),
    ("Prepare Defense Slides & Practice", "2025-06-01", "2025-06-15", "crit"),
    ("Final Defense", "2025-06-16", "2025-06-25", "crit"),  # Window for defense
]

# --- 2. Data Processing ---
tasks = [t[0] for t in tasks_data]
status = [t[3] for t in tasks_data]
start_dates = [datetime.strptime(t[1], "%Y-%m-%d") for t in tasks_data]
end_dates = [datetime.strptime(t[2], "%Y-%m-%d") for t in tasks_data]
durations_days = [(end - start).days + 1 for start, end in zip(start_dates, end_dates)]

# Color mapping
colors = {'done': '#4CAF50', 'active': '#2196F3', 'crit': '#F44336'}
bar_colors = [colors[s] for s in status]

# --- 3. Create the Gantt Chart ---
fig, ax = plt.subplots(figsize=(16, 10))  # Increased size for more tasks

# Invert y-axis
tasks_y = range(len(tasks) - 1, -1, -1)

# Plot the horizontal bars
ax.barh(tasks_y, durations_days, left=start_dates, color=bar_colors, align='center', height=0.5)

# --- 4. Format the Chart ---
ax.set_yticks(tasks_y)
ax.set_yticklabels(tasks, fontsize=9)  # Slightly smaller font for more tasks
ax.set_ylabel("Project Tasks", fontsize=12)
ax.set_xlabel("Date", fontsize=12)
ax.set_title("FYP Gantt Chart", fontsize=16, pad=20)

# Format the x-axis as dates
ax.xaxis_date()
date_format = mdates.DateFormatter('%Y-%m-%d')
ax.xaxis.set_major_formatter(date_format)
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=mdates.MO, interval=1))
fig.autofmt_xdate(rotation=30, ha='right')

# Add gridlines
ax.grid(axis='x', linestyle='--', alpha=0.7)
ax.grid(axis='y', linestyle=':', alpha=0.3)

# Add Legend
legend_elements = [
    plt.Rectangle((0, 0), 1, 1, color=colors['done'], label='Done'),
    plt.Rectangle((0, 0), 1, 1, color=colors['active'], label='Active'),
    plt.Rectangle((0, 0), 1, 1, color=colors['crit'], label='Planned / Critical')
]
ax.legend(handles=legend_elements, loc='upper right', fontsize=10)

plt.tight_layout()

# --- 5. Display or Save the Chart ---
print("Chart generated. Displaying...")
plt.show()

# To save the file, uncomment the lines below
# save_filename = "fyp_gantt_chart_detailed_en.png"
# plt.savefig(save_filename, dpi=300)
# print(f"Chart saved as '{save_filename}'")
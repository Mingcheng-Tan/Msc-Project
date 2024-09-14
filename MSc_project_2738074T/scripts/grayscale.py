import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os
import sys
import matplotlib.colors as mcolors
from matplotlib.cm import ScalarMappable

file_path_default = sys.argv[1]
#file_path_default = 'C:/users/alfie/Unity Projects/Repo Format/data/runs/Participant N/EYE: Left||right/raw/'
file_path = os.path.join(file_path_default, "stimulus_results.txt")

data = []
with open(file_path, 'r') as file:
    for i,line in enumerate(file):
        if i==0:
            continue
        fields = line.strip().split(',')
        fields[1], fields[3] = fields[1].strip('('), fields[3].strip(' )')
        del fields[2]
        data.append(fields)

valid_points = {}
for index, x, y, seen_stimulus, time_since_test_start, reaction_time, was_looking_at_centre in data:
    if was_looking_at_centre != None:
        key = (float(x), float(y))
        if key not in valid_points:
            valid_points[key] = 0
        if seen_stimulus == 'True':
            valid_points[key] += 1
x_vals, y_vals, colors = [], [], []
for (x, y), count in valid_points.items():
    x_vals.append(x)
    y_vals.append(y)
    if count == 3:
        colors.append('white')
    elif count == 2:
        colors.append('lightgray')
    elif count == 1:
        colors.append('darkgray')
    else:
        colors.append('black')
        
plt.figure(figsize=(8, 6))

square_half_width = 0.7 / 2


for x, y, color in zip(x_vals, y_vals, colors):
    square = patches.Rectangle((x - square_half_width, y - square_half_width), 0.68, 0.68,
                               color=color, zorder=2)
    plt.gca().add_patch(square)


plt.axhline(y=0, color='black', linewidth=1, zorder=3)
plt.axvline(x=0, color='black', linewidth=1, zorder=3)

x_min, x_max = min(x_vals), max(x_vals)
y_min, y_max = min(y_vals), max(y_vals)
for y in np.arange(np.floor(y_min), np.ceil(y_max) + 1):
    plt.plot([-0.1, 0.1], [y, y], color='black', linewidth=1, zorder=4)
for x in np.arange(np.floor(x_min), np.ceil(x_max) + 1):
    plt.plot([x, x], [-0.1, 0.1], color='black', linewidth=1, zorder=4)
    

plt.xticks(np.arange(np.floor(x_min), np.ceil(x_max)+1, 1.0))
plt.yticks(np.arange(np.floor(y_min), np.ceil(y_max)+1, 1.0))

plt.gca().set_facecolor((0.95, 0.95, 0.95))
plt.title('Grayscale Graph of Observations')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.xlim(x_min - 1, x_max + 1)
plt.ylim(y_min - 1, y_max + 1)
plt.grid(True, which='both', linestyle='--', linewidth=0.4, zorder=1)

output_dir_path = os.path.join(os.path.dirname(file_path_default), "processed")
output_file_path = os.path.join(output_dir_path, "grayscale.png")

plt.savefig(output_file_path, dpi=300)

plt.close()

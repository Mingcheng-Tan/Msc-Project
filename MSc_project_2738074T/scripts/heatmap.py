import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

file_path_default = sys.argv[1]

file_path = os.path.join(file_path_default, "EyeTrackingData.txt")

data = pd.read_csv(file_path, header=None, names=['Time', 'X', 'Y', 'LookingAtStim'], skiprows=1)
data['LookingAtStim'] = data['LookingAtStim'].astype(bool)

plt.figure(figsize=(8, 6))
sns.kdeplot(data=data, x='X', y='Y', fill=True, cmap="plasma", cbar=True)
plt.xlim(-5, 5)
plt.ylim(-5, 5)
plt.title('Heatmap of Gaze Points')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')


output_dir_path = os.path.join(os.path.dirname(file_path_default), "processed")
output_file_path = os.path.join(output_dir_path, "heatmap.png")

plt.savefig(output_file_path, dpi=300)

plt.close()

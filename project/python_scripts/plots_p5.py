import numpy as np
import matplotlib.pyplot as plt

file_path = './server_implementation/service_times.csv'
plots_path = "./plots"
file_extension = "pdf"
service_times = np.loadtxt(file_path,skiprows=1)
values, counts = np.unique(service_times, return_counts=True)
bar_width = max(np.min(np.diff(np.unique(values))) / 2, 0.1)

plt.figure(figsize=(12, 8))
plt.bar(values, counts, width=bar_width, color='blue', alpha=0.7, edgecolor='black')

plt.title('Service Time Distribution')
plt.xlabel('Service Time (ms)')
plt.ylabel('Frequency')
plt.grid(True)
plt.tight_layout()
plt.savefig(f"{plots_path}/service_time.{file_extension}")


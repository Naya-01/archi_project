import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

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





data_directory = './data/'
file_pattern = 'results__rate_{}.csv'

data = {'Rate': [], 'Latency': []}

for rate in range(2, 10, 1):
    file_path = os.path.join(data_directory, file_pattern.format(rate))
    df = pd.read_csv(file_path)
    average_latency = df['LATENCY'].mean()

    data['Rate'].append(rate)
    data['Latency'].append(average_latency)


df_data = pd.DataFrame(data)

plt.figure(figsize=(10, 6))
plt.plot(df_data['Rate'], df_data['Latency'], marker='o', label='Measured Response Time')
plt.title('Measured Response Time vs. Number of Requests per Second')
plt.xlabel('Number of Requests per Second')
plt.ylabel('Response Time (seconds)')
plt.grid(True)
plt.legend()
plt.tight_layout()

output_filename = f"{plots_path}/measured_response_time_plot.{file_extension}"
plt.savefig(output_filename)
plt.close()



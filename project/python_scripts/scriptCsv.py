import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


datas = pd.read_csv("./data/results.csv")
datas['LATENCY'] = datas['LATENCY'] * 1000
grouped_debits = datas.groupby('debits')

plots_path = "./plots"
file_extension = "pdf"
markers = ['o', 's', '^', 'D', '*']
colors = ['blue', 'green', 'purple', 'orange', 'red']



def plot_data(grouped_data_param, x_column, y_column, ylabel, title, file_name):
    grouped_data = datas.groupby(grouped_data_param)
    plt.figure(figsize=(10, 6))
    for (index, (label, group_data)) in enumerate(grouped_data):
        mean_values = group_data.groupby(x_column)[y_column].mean()
        error = group_data.groupby(x_column)[y_column].std()

        mean_values.plot(kind='line', label=f'{grouped_data_param}: {label}', color=colors[index], linewidth=2)
        plt.scatter(mean_values.index, mean_values.values, marker=markers[index], color=colors[index], s=50)
        plt.errorbar(mean_values.index, mean_values.values, yerr=error.values, fmt=markers[index], elinewidth=2, capsize=5, color=colors[index])

    plt.xlabel(x_column.capitalize().replace("_", " ") + ' (bytes)')
    plt.ylabel(f'{ylabel}')
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.savefig(os.path.join(plots_path, f"{file_name}.{file_extension}"))
    plt.close()


def generate_plot(datas, x_col, y_col, secondary_col, y_label, file_prefix, title_prefix):

    for debits, group_data in grouped_debits:
        plt.figure(figsize=(10, 6))
        grouped = group_data.groupby([x_col, secondary_col])[y_col].mean().reset_index()

        for unique_val in grouped[secondary_col].unique():
            subset = grouped[grouped[secondary_col] == unique_val]
            plt.plot(subset[x_col], subset[y_col], label=f"{secondary_col.capitalize()}: {unique_val}", marker='o')
        
        plt.legend()
        plt.xlabel(f"{x_col.capitalize().replace('_', ' ')} (bytes)")
        plt.ylabel(f"{y_label}")
        plt.title(f"{title_prefix} vs. {x_col.capitalize().replace('_', ' ')} for Different {secondary_col.capitalize()}s (Debits: {debits})")
        plt.grid(True)
        plt.savefig(f"{plots_path}/{file_prefix}_debits_{debits}.{file_extension}")
        plt.close()

# file vs key / Latency
generate_plot(datas, 'file_size', 'LATENCY', 'key_size', 'Average Latency (ms)', 'latency_vs_filesize', 'Average Latency')
# key vs threads / LATENCY
generate_plot(datas, 'key_size', 'LATENCY', 'threads', 'Average Latency (ms)', 'latency_vs_keysize_threads', 'Average Latency')
# file vs threads / LATENCY
generate_plot(datas, 'file_size', 'LATENCY', 'threads', 'Average Latency (ms)', 'latency_vs_filesize_threads', 'Average Latency')
# file vs threads / REQ
generate_plot(datas, 'file_size', 'REQ', 'threads', 'Average Request/Sec', 'request_vs_filesize_threads', 'Average Request')


grouped = datas.groupby(['threads', 'debits'])['LATENCY'].mean().unstack()
colors = ['b', 'g', 'r', 'c', 'm', 'y']
plt.figure(figsize=(10, 6))
debits = grouped.columns
width = 0.3
x = grouped.index
bottom_values = np.zeros(len(x))
fig, ax = plt.subplots()
for i, debit in enumerate(debits):
    latencies = grouped[debit]
    plt.bar(x + i * width, latencies, width, label=f"Debit: {debit}", color=colors[i])
plt.xlabel("Thread")
plt.ylabel("Average Latency (ms)")
plt.title("Average Latency vs. Thread for Different Debits")
plt.legend()
plt.grid(True)
plt.xticks(x + width * len(debits) / 2, x)
plt.savefig(f"{plots_path}/latency_vs_thread_debits.{file_extension}")
plt.close()

# Effect of nbRounds
grouped = datas.groupby('numRounds')['LATENCY'].mean() 
plt.figure(figsize=(10, 6))
grouped.plot(kind='bar', color='lightcoral')
plt.title('Latency vs NumRounds')
plt.xlabel('NumRounds')
plt.ylabel('Average Latency (ms)')
plt.grid(axis='y')
plt.tight_layout()
plt.savefig(f"{plots_path}/Latency_NumRounds_Average_bar.{file_extension}")
plt.close()



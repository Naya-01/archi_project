import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


datas = pd.read_csv("./data/results.csv")
datas['LATENCY'] = datas['LATENCY'] * 1000
datas['LATENCY'].fillna(datas['LATENCY'].mean(), inplace=True)
datas['REQ'].fillna(datas['REQ'].mean(), inplace=True)
datas['TRANSFER'] = datas['TRANSFER'] / 1024

grouped_debits = datas.groupby('debits')

plots_path = "./plots"
file_extension = "pdf"
markers = ['o', 's', '^', 'D', '*']
colors = ['b', 'g', 'r', 'c', 'm', 'y']


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


def generate_plot(x_col, y_col, secondary_col, y_label, file_prefix, title_prefix):
    line_styles = ['-', '--', '-.', ':']  # Different line styles
    marker_styles = ['o', 's', '^', 'D', '*']  # Different marker styles
    alpha = 0.7  # Opacity of the lines and error bars

    for debits, group_data in grouped_debits:
        plt.figure(figsize=(10, 6))
        grouped = group_data.groupby([x_col, secondary_col])[y_col].agg(['mean', 'std']).reset_index()

        for idx, unique_val in enumerate(grouped[secondary_col].unique()):
            subset = grouped[grouped[secondary_col] == unique_val]

            # Using different line and marker styles, and slightly offsetting each line
            x_values = subset[x_col] + idx * 0.01  # Offset to separate overlapping lines
            line_style = line_styles[idx % len(line_styles)]
            marker_style = marker_styles[idx % len(marker_styles)]

            plt.errorbar(x_values, subset['mean'], yerr=subset['std'], label=f"{secondary_col.capitalize()}: {unique_val}", 
                         marker=marker_style, linestyle=line_style, alpha=alpha)
        
        plt.legend()
        plt.xlabel(f"{x_col.capitalize().replace('_', ' ')} (bytes)")
        plt.ylabel(f"{y_label}")
        plt.title(f"{title_prefix} vs. {x_col.capitalize().replace('_', ' ')} for Different {secondary_col.capitalize()} (Debits: {debits})")
        plt.grid(True)

        # Set the lower limit of Y-axis to 0
        plt.ylim(bottom=0)

        plt.savefig(f"{plots_path}/{file_prefix}_debits_{debits}.{file_extension}")
        plt.close()




# file vs key / Latency
generate_plot('file_size', 'LATENCY', 'key_size', 'Average Latency (ms)', 'latency_vs_filesize', 'Average Latency')
# key vs threads / LATENCY
generate_plot('key_size', 'LATENCY', 'threads', 'Average Latency (ms)', 'latency_vs_keysize_threads', 'Average Latency')
# file vs threads / LATENCY
generate_plot('file_size', 'LATENCY', 'threads', 'Average Latency (ms)', 'latency_vs_filesize_threads', 'Average Latency')
# file vs threads / REQ
generate_plot('file_size', 'REQ', 'threads', 'Average Request/Sec', 'request_vs_filesize_threads', 'Average Request')
# file vs key / REQ
generate_plot('file_size', 'REQ', 'key_size', 'Average REQ', 'req_latency_vs_filesize', 'Average REQ')

grouped = datas.groupby(['threads', 'debits'])['LATENCY'].agg(['mean', 'std', 'var']).unstack()
plt.figure(figsize=(10, 6))
debits = grouped.columns.levels[1] 
width = 0.3
x = np.arange(len(grouped))
fig, ax = plt.subplots()
min_y_val = 0
for i, debit in enumerate(debits):
    latencies = grouped['mean'][debit]
    std_dev = grouped['std'][debit]

    min_latencies = latencies - std_dev
    min_y_val = min(min_y_val, min_latencies.min())

    plt.bar(x + i * width, latencies, width, label=f"Debit: {debit}", color=colors[i], yerr=std_dev)
    
plt.xlabel("Thread")
plt.ylabel("Average Latency (ms)")
plt.title("Average Latency vs. Thread for Different Debits")
plt.legend()
plt.grid(True)
plt.xticks(x + width * (len(debits) - 1) / 2, grouped.index)
plt.ylim(bottom=0)
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


def plot(dataframe, x_column, y_column, ylabel, title=''):
    grouped_data = dataframe.groupby(x_column).agg({y_column: ['mean', 'std']}).reset_index()
    grouped_data.columns = [x_column, f'{y_column}_mean', f'{y_column}_std']
    print(grouped_data[f'{y_column}_std'])
    lower_errors = np.maximum(grouped_data[f'{y_column}_mean'] - grouped_data[f'{y_column}_std'], 0)
    upper_errors = grouped_data[f'{y_column}_std']
    asymmetric_error = [grouped_data[f'{y_column}_mean'] - lower_errors, upper_errors]

    plt.figure(figsize=(10, 6))
    plt.errorbar(grouped_data[x_column], grouped_data[f'{y_column}_mean'], 
                 yerr=asymmetric_error, fmt='o', ecolor='blue', capsize=5, 
                 linestyle='-', color='blue')

    plt.xlabel(x_column)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.ylim(bottom=0)
    plt.grid(True)
    title = title.replace(" ", "_")
    plt.savefig(f"{plots_path}/{title}.{file_extension}")

plot(datas, 'file_size', 'LATENCY', 'Latency (ms)', title='Latency according to the File Sizes')
plot(datas, 'key_size', 'LATENCY', 'Latency (ms)', title='Latency according to the Key Sizes')
plot(datas, 'file_size', 'TRANSFER', 'Throughput (Mb/sec)', title='Throughput according to the File Sizes')
plot(datas, 'key_size', 'TRANSFER', 'Throughput (Mb/sec)', title='Throughput according to the Key Sizes')



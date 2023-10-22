import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

datas = pd.read_csv("./data/results.csv")
datas['LATENCY'] = datas['LATENCY'] * 1000
datas['REQ'] = datas['REQ']

plots_path = "./plots"
file_extension = "pdf"

markers = ['o', 's', '^', 'D', '*']
colors = ['blue', 'green', 'purple', 'orange', 'red']

# Regrouper les données par 'debits'
grouped = datas.groupby('numRounds')

# Latency/keysize
plt.figure(figsize=(10, 6))

for (index, (debits, group_data)) in enumerate(grouped):
    mean_latency = group_data.groupby('key_size')['LATENCY'].mean()
    error = group_data.groupby('key_size')['LATENCY'].std()

    mean_latency.plot(kind='line', label=f'Debits: {debits}', color=colors[index], linewidth=2)
    plt.scatter(mean_latency.index, mean_latency.values, marker=markers[index], color=colors[index], s=50)
    plt.errorbar(mean_latency.index, mean_latency.values, yerr=error.values, fmt=markers[index], elinewidth=2, capsize=5, color=colors[index])

plt.xlabel('Key size (bytes)')
plt.ylabel('LATENCY (ms)')
plt.title('LATENCY in line with Key size for Different Debits')
plt.grid(True)
plt.legend()
plt.savefig(f"{plots_path}/keyplot_all_debits_latency.{file_extension}")
plt.close()

# Request/keysize
plt.figure(figsize=(10, 6))

for (index, (debits, group_data)) in enumerate(grouped):
    mean_latency = group_data.groupby('key_size')['REQ'].mean()
    error = group_data.groupby('key_size')['REQ'].std()

    mean_latency.plot(kind='line', label=f'Debits: {debits}', color=colors[index], linewidth=2)
    plt.scatter(mean_latency.index, mean_latency.values, marker=markers[index], color=colors[index], s=50)
    plt.errorbar(mean_latency.index, mean_latency.values, yerr=error.values, fmt=markers[index], elinewidth=2, capsize=5, color=colors[index])

plt.xlabel('Key size (bytes)')
plt.ylabel('REQUEST (ms)')
plt.title('REQUEST in line with Key size for Different Debits')
plt.grid(True)
plt.legend()
plt.savefig(f"{plots_path}/keyplot_all_debits_requests.{file_extension}")
plt.close()

# Latency/FileSize
plt.figure(figsize=(10, 6))

for (index, (debits, group_data)) in enumerate(grouped):
    mean_latency = group_data.groupby('file_size')['LATENCY'].mean()
    error = group_data.groupby('file_size')['LATENCY'].std()

    mean_latency.plot(kind='line', label=f'Debits: {debits}', color=colors[index], linewidth=2)
    plt.scatter(mean_latency.index, mean_latency.values, marker=markers[index], color=colors[index], s=50)
    plt.errorbar(mean_latency.index, mean_latency.values, yerr=error.values, fmt=markers[index], elinewidth=2, capsize=5, color=colors[index])

plt.xlabel('File size (bytes)')
plt.ylabel('LATENCY (ms)')
plt.title('LATENCY in line with Key size for Different Debits')
plt.grid(True)
plt.legend()
plt.savefig(f"{plots_path}/fileplot_all_debits_latency.{file_extension}")
plt.close()

# Request/FileSize
plt.figure(figsize=(10, 6))

for (index, (debits, group_data)) in enumerate(grouped):
    mean_latency = group_data.groupby('file_size')['REQ'].mean()
    error = group_data.groupby('file_size')['REQ'].std()

    mean_latency.plot(kind='line', label=f'Debits: {debits}', color=colors[index], linewidth=2)
    plt.scatter(mean_latency.index, mean_latency.values, marker=markers[index], color=colors[index], s=50)
    plt.errorbar(mean_latency.index, mean_latency.values, yerr=error.values, fmt=markers[index], elinewidth=2, capsize=5, color=colors[index])

plt.xlabel('File size (bytes)')
plt.ylabel('Req (ms)')
plt.title('Req in line with Key size for Different Debits')
plt.grid(True)
plt.legend()
plt.savefig(f"{plots_path}/fileplot_all_debits_request.{file_extension}")
plt.close()

# Latency/Threads
plt.figure(figsize=(10, 6))

for (index, (debits, group_data)) in enumerate(grouped):
    mean_latency = group_data.groupby('threads')['LATENCY'].mean()
    error = group_data.groupby('threads')['LATENCY'].std()

    mean_latency.plot(kind='line', label=f'Débit moyen: {debits}', color=colors[index], linewidth=2)
    plt.scatter(mean_latency.index, mean_latency.values, marker=markers[index], color=colors[index], s=50)
    plt.errorbar(mean_latency.index, mean_latency.values, yerr=error.values, fmt=markers[index], elinewidth=2, capsize=5, color=colors[index])

plt.xlabel('File size (bytes)')
plt.ylabel('LATENCY (ms)')
plt.title('LATENCY in line with Key size for Different Debits')
plt.grid(True)
plt.legend()
plt.savefig(f"{plots_path}/threadsplot_all_debits_latency.{file_extension}")
plt.close()

# Request/Threads
plt.figure(figsize=(10, 6))

for (index, (debits, group_data)) in enumerate(grouped):
    mean_latency = group_data.groupby('threads')['REQ'].mean()
    error = group_data.groupby('threads')['REQ'].std()

    mean_latency.plot(kind='line', label=f'Debits: {debits}', color=colors[index], linewidth=2)
    plt.scatter(mean_latency.index, mean_latency.values, marker=markers[index], color=colors[index], s=50)
    plt.errorbar(mean_latency.index, mean_latency.values, yerr=error.values, fmt=markers[index], elinewidth=2, capsize=5, color=colors[index])

plt.xlabel('File size (bytes)')
plt.ylabel('REQ (ms)')
plt.title('REQ in line with Key size for Different Debits')
plt.grid(True)
plt.legend()
plt.savefig(f"{plots_path}/threadsplot_all_debits_request.{file_extension}")
plt.close()

#file vs key / Latency

grouped_debits = datas.groupby('debits')

for debits, group_data in grouped_debits:
    plt.figure(figsize=(10, 6))

    # Regrouper les données par 'file_size' et 'key_size' et calculer la moyenne de la latence
    grouped = group_data.groupby(['file_size', 'key_size'])['LATENCY'].mean().reset_index()

    for key_size in grouped['key_size'].unique():
        subset = grouped[grouped['key_size'] == key_size]
        plt.plot(subset['file_size'], subset['LATENCY'], label=f"Key Size: {key_size}", marker='o')

    plt.legend()
    plt.xlabel("File Size (bytes)")
    plt.ylabel("Average Latency (ms)")
    plt.title(f"Average Latency vs. File Size for Different Key Sizes (Debits: {debits})")
    plt.grid(True)
    plt.savefig(f"{plots_path}/latency_vs_filesize_debits_{debits}.{file_extension}")
    plt.close()

#file vs key / REQ

for debits, group_data in grouped_debits:
    plt.figure(figsize=(10, 6))

    # Regrouper les données par 'file_size' et 'key_size' et calculer la moyenne de la latence
    grouped = group_data.groupby(['file_size', 'key_size'])['REQ'].mean().reset_index()

    for key_size in grouped['key_size'].unique():
        subset = grouped[grouped['key_size'] == key_size]
        plt.plot(subset['file_size'], subset['REQ'], label=f"Key Size: {key_size}", marker='o')

    plt.legend()
    plt.xlabel("File Size (bytes)")
    plt.ylabel("Average REQ (ms)")
    plt.title(f"Average REQ vs. File Size for Different Key Sizes (Debits: {debits})")
    plt.grid(True)
    plt.savefig(f"{plots_path}/req_latency_vs_filesize_debits_{debits}.{file_extension}")
    plt.close()


grouped = datas.groupby(['key_size', 'file_size']).LATENCY.mean().reset_index()
for size in grouped['file_size'].unique():
    subset = grouped[grouped['file_size'] == size]
    plt.plot(subset['key_size'], subset['LATENCY'], label=f"File Size: {size} bytes", marker='o')

plt.legend()
plt.xlabel("Key Size (bits)")
plt.ylabel("Latency (ms)")
plt.title("Latency vs. Key Size for Different File Sizes")

# Grille
plt.grid(True)
plt.savefig(f"{plots_path}/latency_vs_keysize.{file_extension}")
plt.close()

for debits, group_data in grouped_debits:
    plt.figure(figsize=(10, 6))
    # Grouper par 'key_size' et 'threads' puis calculer la latence moyenne
    grouped = group_data.groupby(['key_size', 'threads'])['LATENCY'].mean().reset_index()

    for thread in grouped['threads'].unique():
        subset = grouped[grouped['threads'] == thread]
        plt.plot(subset['key_size'], subset['LATENCY'], label=f"Threads: {thread}", marker='o')

    plt.legend()
    plt.xlabel("Key Size (bytes)")
    plt.ylabel("Average Latency (ms)")
    plt.title(f"Average Latency vs. Key Size for Different Number of Threads (Debits: {debits})")
    plt.grid(True)
    plt.savefig(f"{plots_path}/latency_vs_keysize_threads_debits_{debits}.{file_extension}")
    plt.close()

for debits, group_data in grouped_debits:
    plt.figure(figsize=(10, 6))
    # Grouper par 'key_size' et 'threads' puis calculer la latence moyenne
    grouped = group_data.groupby(['key_size', 'threads'])['REQ'].mean().reset_index()

    for thread in grouped['threads'].unique():
        subset = grouped[grouped['threads'] == thread]
        plt.plot(subset['key_size'], subset['REQ'], label=f"Threads: {thread}", marker='o')

    plt.legend()
    plt.xlabel("Key Size (bytes)")
    plt.ylabel("Average Request (ms)")
    plt.title(f"Average Request vs. Key Size for Different Number of Threads (Debits: {debits})")
    plt.grid(True)
    plt.savefig(f"{plots_path}/request_vs_keysize_threads_debits_{debits}.{file_extension}")
    plt.close()

for debits, group_data in grouped_debits:
    plt.figure(figsize=(10, 6))
    # Grouper par 'key_size' et 'threads' puis calculer la latence moyenne
    grouped = group_data.groupby(['file_size', 'threads'])['LATENCY'].mean().reset_index()

    for thread in grouped['threads'].unique():
        subset = grouped[grouped['threads'] == thread]
        plt.plot(subset['file_size'], subset['LATENCY'], label=f"Threads: {thread}", marker='o')

    plt.legend()
    plt.xlabel("File Size (bytes)")
    plt.ylabel("Average Latency (ms)")
    plt.title(f"Average Latency vs. File Size for Different Number of Threads (Debits: {debits})")
    plt.grid(True)
    plt.savefig(f"{plots_path}/latency_vs_filesize_threads_debits_{debits}.{file_extension}")
    plt.close()

for debits, group_data in grouped_debits:
    plt.figure(figsize=(10, 6))
    # Grouper par 'key_size' et 'threads' puis calculer la latence moyenne
    grouped = group_data.groupby(['file_size', 'threads'])['REQ'].mean().reset_index()

    for thread in grouped['threads'].unique():
        subset = grouped[grouped['threads'] == thread]
        plt.plot(subset['file_size'], subset['REQ'], label=f"Threads: {thread}", marker='o')

    plt.legend()
    plt.xlabel("File Size (bytes)")
    plt.ylabel("Average Request (ms)")
    plt.title(f"Average Request vs. File Size for Different Number of Threads (Debits: {debits})")
    plt.grid(True)
    plt.savefig(f"{plots_path}/request_vs_filesize_threads_debits_{debits}.{file_extension}")
    plt.close()

plt.figure(figsize=(10, 6))

for debits, group_data in grouped_debits:
    plt.scatter(group_data['REQ'], group_data['LATENCY'], label=f"Debits: {debits}", marker='o')

plt.legend()
plt.xlabel("Request Count")
plt.ylabel("Latency (ms)")
plt.title("Latency vs. Request Count for Different Debits")
plt.grid(True)
plt.savefig(f"{plots_path}/latency_vs_request_count_debits.{file_extension}")
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



grouped_data = datas.groupby('numRounds')['LATENCY'].mean()
plt.figure(figsize=(10, 6))
plt.plot(grouped_data.index, grouped_data.values, marker='o', linestyle='-', color='b')
plt.title('Impact of NbRounds on Latency')
plt.xlabel('NbRounds')
plt.ylabel('Average Latency (ms)')
plt.grid(True, which="both", ls="--", c='0.7')
plt.savefig(f"{plots_path}/Latency_NumRounds_Average_line.{file_extension}")
plt.close()

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

for debits, group_data in grouped_debits:
    plt.figure(figsize=(10, 6))
    grouped = group_data.groupby(['file_size', 'key_size'])['TRANSFER'].mean().reset_index()
    for key_size in grouped['key_size'].unique():
        subset = grouped[grouped['key_size'] == key_size]
        plt.plot(subset['file_size'], subset['TRANSFER'], label=f"Key Size: {key_size}", marker='o')
    plt.legend()
    plt.xlabel("File Size (bytes)")
    plt.ylabel("Average Transfer/sec (ms)")
    plt.title(f"Average Transfer/sec vs. File Size for Different Key Sizes (Debits: {debits})")
    plt.grid(True)
    plt.savefig(f"{plots_path}/transfer_vs_filesize_debits_{debits}.{file_extension}")
    plt.close()

for debits, group_data in grouped_debits:
    plt.figure(figsize=(10, 6))
    grouped = group_data.groupby(['key_size', 'threads'])['TRANSFER'].mean().reset_index()
    for thread in grouped['threads'].unique():
        subset = grouped[grouped['threads'] == thread]
        plt.plot(subset['key_size'], subset['TRANSFER'], label=f"Threads: {thread}", marker='o')
    plt.legend()
    plt.xlabel("Key Size (bytes)")
    plt.ylabel("Average Transfer/sec")
    plt.title(f"Average transfer/sec vs. Key Size for Different Number of Threads (Debits: {debits})")
    plt.grid(True)
    plt.savefig(f"{plots_path}/transfer_vs_keysize_threads_debits_{debits}.{file_extension}")
    plt.close()
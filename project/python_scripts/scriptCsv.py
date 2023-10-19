import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

datas = pd.read_csv("./data/measurements.csv")
datas['LATENCY'] = datas['LATENCY'] * 1000
datas['REQ'] = datas['REQ'] * 1000
# Regrouper les données par 'debits'
grouped = datas.groupby('debits')

# Latency/keysize
plt.figure(figsize=(10, 6))

for debits, group_data in grouped:
    mean_latency = group_data.groupby('key_size')['LATENCY'].mean()
    error = group_data.groupby('key_size')['LATENCY'].std()

    mean_latency.plot(kind='line', label=f'Debits: {debits}')
    plt.scatter(mean_latency.index, mean_latency.values)
    plt.errorbar(mean_latency.index, mean_latency.values, yerr=error.values, fmt='o', elinewidth=2, capsize=5)

plt.xlabel('Key size (bytes)')
plt.ylabel('LATENCY (ms)')
plt.title('LATENCY in line with Key size for Different Debits')
plt.grid(True)
plt.legend()
plt.savefig("./plots/keyplot_all_debits_latency.PNG")
plt.close()

# Request/keysize
plt.figure(figsize=(10, 6))

for debits, group_data in grouped:
    mean_latency = group_data.groupby('key_size')['REQ'].mean()
    error = group_data.groupby('key_size')['REQ'].std()

    mean_latency.plot(kind='line', label=f'Debits: {debits}')
    plt.scatter(mean_latency.index, mean_latency.values)
    plt.errorbar(mean_latency.index, mean_latency.values, yerr=error.values, fmt='o', elinewidth=2, capsize=5)

plt.xlabel('Key size (bytes)')
plt.ylabel('REQUEST (ms)')
plt.title('REQUEST in line with Key size for Different Debits')
plt.grid(True)
plt.legend()
plt.savefig("./plots/keyplot_all_debits_requests.PNG")
plt.close()

# Latency/FileSize
plt.figure(figsize=(10, 6))

for debits, group_data in grouped:
    mean_latency = group_data.groupby('file_size')['LATENCY'].mean()
    error = group_data.groupby('file_size')['LATENCY'].std()

    mean_latency.plot(kind='line', label=f'Debits: {debits}')
    plt.scatter(mean_latency.index, mean_latency.values)
    plt.errorbar(mean_latency.index, mean_latency.values, yerr=error.values, fmt='o', elinewidth=2, capsize=5)

plt.xlabel('File size (bytes)')
plt.ylabel('LATENCY (ms)')
plt.title('LATENCY in line with Key size for Different Debits')
plt.grid(True)
plt.legend()
plt.savefig("./plots/fileplot_all_debits_latency.PNG")
plt.close()

# Request/FileSize
plt.figure(figsize=(10, 6))

for debits, group_data in grouped:
    mean_latency = group_data.groupby('file_size')['REQ'].mean()
    error = group_data.groupby('file_size')['REQ'].std()

    mean_latency.plot(kind='line', label=f'Debits: {debits}')
    plt.scatter(mean_latency.index, mean_latency.values)
    plt.errorbar(mean_latency.index, mean_latency.values, yerr=error.values, fmt='o', elinewidth=2, capsize=5)

plt.xlabel('File size (bytes)')
plt.ylabel('Req (ms)')
plt.title('Req in line with Key size for Different Debits')
plt.grid(True)
plt.legend()
plt.savefig("./plots/fileplot_all_debits_request.PNG")
plt.close()

# Latency/Threads
plt.figure(figsize=(10, 6))

for debits, group_data in grouped:
    mean_latency = group_data.groupby('threads')['LATENCY'].mean()
    error = group_data.groupby('threads')['LATENCY'].std()

    mean_latency.plot(kind='line', label=f'Debits: {debits}')
    plt.scatter(mean_latency.index, mean_latency.values)
    plt.errorbar(mean_latency.index, mean_latency.values, yerr=error.values, fmt='o', elinewidth=2, capsize=5)

plt.xlabel('File size (bytes)')
plt.ylabel('LATENCY (ms)')
plt.title('LATENCY in line with Key size for Different Debits')
plt.grid(True)
plt.legend()
plt.savefig("./plots/threadsplot_all_debits_latency.PNG")
plt.close()

# Request/Threads
plt.figure(figsize=(10, 6))

for debits, group_data in grouped:
    mean_latency = group_data.groupby('threads')['REQ'].mean()
    error = group_data.groupby('threads')['REQ'].std()

    mean_latency.plot(kind='line', label=f'Debits: {debits}')
    plt.scatter(mean_latency.index, mean_latency.values)
    plt.errorbar(mean_latency.index, mean_latency.values, yerr=error.values, fmt='o', elinewidth=2, capsize=5)

plt.xlabel('File size (bytes)')
plt.ylabel('REQ (ms)')
plt.title('REQ in line with Key size for Different Debits')
plt.grid(True)
plt.legend()
plt.savefig("./plots/threadsplot_all_debits_request.PNG")
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
    plt.savefig(f"./plots/latency_vs_filesize_debits_{debits}.PNG")
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
    plt.savefig(f"./plots/req_latency_vs_filesize_debits_{debits}.PNG")
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
plt.savefig("./plots/latency_vs_keysize.PNG")
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
    plt.savefig(f"./plots/latency_vs_keysize_threads_debits_{debits}.PNG")
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
    plt.savefig(f"./plots/request_vs_keysize_threads_debits_{debits}.PNG")
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
    plt.savefig(f"./plots/latency_vs_filesize_threads_debits_{debits}.PNG")
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
    plt.savefig(f"./plots/request_vs_filesize_threads_debits_{debits}.PNG")
    plt.close()

plt.figure(figsize=(10, 6))

for debits, group_data in grouped_debits:
    plt.scatter(group_data['REQ'], group_data['LATENCY'], label=f"Debits: {debits}", marker='o')

plt.legend()
plt.xlabel("Request Count")
plt.ylabel("Latency (ms)")
plt.title("Latency vs. Request Count for Different Debits")
plt.grid(True)
plt.savefig("./plots/latency_vs_request_count_debits.PNG")
plt.show()
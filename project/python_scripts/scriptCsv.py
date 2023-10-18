import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


datas = pd.read_csv("./data/measurements.csv")
datas['LATENCY'] = datas['LATENCY'] * 1000

mean_latency = datas.groupby('key_size')['LATENCY'].mean() 
error = datas.groupby('key_size')['LATENCY'].std() 
plt.figure(figsize=(10, 6))

mean_latency.plot(kind='line', color='blue')
plt.scatter(mean_latency.index, mean_latency.values, color='blue', label='Points', s=50)
plt.errorbar(mean_latency.index, mean_latency.values, yerr=error.values, fmt='o', color='blue', elinewidth=2, capsize=5, label='Barres d\'erreur')
plt.xlabel('Key size (bytes)')
plt.ylabel('LATENCY (ms)')
plt.title('LATENCY in line with Key size')  
plt.grid(True)
plt.savefig("./plots/keyplot.PNG")
plt.close()




mean_latency = datas.groupby('file_size')['LATENCY'].mean() 
error = datas.groupby('file_size')['LATENCY'].std() 
plt.figure(figsize=(10, 6))

mean_latency.plot(kind='line', color='blue')
plt.scatter(mean_latency.index, mean_latency.values, color='blue', label='Points', s=50)
plt.errorbar(mean_latency.index, mean_latency.values, yerr=error.values, fmt='o', color='blue', elinewidth=2, capsize=5, label='Barres d\'erreur')
plt.xlabel('File size (bytes)')
plt.ylabel('LATENCY (ms)')
plt.title('LATENCY in line with File size')  
plt.grid(True)
plt.savefig("./plots/fileplot.PNG")
plt.close()




mean_latency = datas.groupby('threads')['LATENCY'].mean() 
error = datas.groupby('threads')['LATENCY'].std() 
plt.figure(figsize=(10, 6))

mean_latency.plot(kind='line', color='blue')
plt.scatter(mean_latency.index, mean_latency.values, color='blue', label='Points', s=50)
plt.errorbar(mean_latency.index, mean_latency.values, yerr=error.values, fmt='o', color='blue', elinewidth=2, capsize=5, label='Barres d\'erreur')
plt.xlabel('threads')
plt.ylabel('LATENCY (ms)')
plt.title('LATENCY in line with Threads')  
plt.grid(True)
plt.savefig("./plots/threadsPlot.PNG")
plt.close()



plt.figure(figsize=(18, 6))

plt.subplot(131)  # Premier sous-graphique
plt.imshow(plt.imread("../plots/keyplot.PNG"))
plt.axis('off')
plt.title('Compare by key Size')

plt.subplot(132)  # Deuxième sous-graphique
plt.imshow(plt.imread("../plots/fileplot.PNG"))
plt.axis('off')
plt.title('Compare by File Size')

plt.subplot(133) 
plt.imshow(plt.imread("../plots/threadsPlot.PNG"))
plt.axis('off')
plt.title('Compare by Threads')

plt.tight_layout()

plt.suptitle('LATENCY comparisons', fontsize=16)
plt.savefig("./plots/compare3.PNG")
plt.close()





grouped = datas.groupby(['file_size', 'key_size']).LATENCY.mean().reset_index() 

for key in grouped['key_size'].unique():
    subset = grouped[grouped['key_size'] == key]
    plt.plot(subset['file_size'], subset['LATENCY'], label=f"Key Size: {key}", marker='o')

plt.legend()
plt.xlabel("File Size (bytes)")
plt.ylabel("Latency (ms)")
plt.title("Average Latency vs. File Size for Different Key Sizes")
plt.grid(True)
plt.savefig("./plots/latency_vs_filesize.PNG")
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





# Grouper par key_size et threads puis calcule la latence moyenne
grouped = datas.groupby(['key_size', 'threads']).LATENCY.mean().reset_index()
for thread in grouped['threads'].unique():
    subset = grouped[grouped['threads'] == thread]
    plt.plot(subset['key_size'], subset['LATENCY'], label=f"Threads: {thread}", marker='o')

plt.legend()
plt.xlabel("Key Size (bytes)")
plt.ylabel("Latency (ms)")
plt.title("Average Latency vs. Key Size for Different Number of Threads")
plt.grid(True)
plt.savefig("./plots/latency_vs_keysize_threads.PNG")
plt.close()


# Grouper par file_size et threads puis calcule la latence moyenne
grouped = datas.groupby(['file_size', 'threads']).LATENCY.mean().reset_index()
for thread in grouped['threads'].unique():
    subset = grouped[grouped['threads'] == thread]
    plt.plot(subset['file_size'], subset['LATENCY'], label=f"Threads: {thread}", marker='o')

plt.legend()
plt.xlabel("File Size (bytes)")
plt.ylabel("Latency (ms)")
plt.title("Average Latency vs. File Size for Different Number of Threads")
plt.grid(True)
plt.savefig("./plots/latency_vs_filesize_threads.PNG")
plt.close()
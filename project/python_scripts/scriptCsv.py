import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


datas = pd.read_csv("../data/measurements.csv")

mean_latency = datas.groupby('key_size')['LATENCY'].mean() * 1000
error = datas.groupby('key_size')['LATENCY'].std() * 1000
plt.figure(figsize=(10, 6))

mean_latency.plot(kind='line', color='blue')
plt.scatter(mean_latency.index, mean_latency.values, color='blue', label='Points', s=50)
plt.errorbar(mean_latency.index, mean_latency.values, yerr=error.values, fmt='o', color='blue', elinewidth=2, capsize=5, label='Barres d\'erreur')
plt.xlabel('Key size')
plt.ylabel('LATENCY (ms)')
plt.title('LATENCY in line with Key size')  
plt.grid(True)
plt.savefig("../plots/keyplot.PNG")
plt.close()




mean_latency = datas.groupby('file_size')['LATENCY'].mean() * 1000
error = datas.groupby('file_size')['LATENCY'].std() * 1000
plt.figure(figsize=(10, 6))

mean_latency.plot(kind='line', color='blue')
plt.scatter(mean_latency.index, mean_latency.values, color='blue', label='Points', s=50)
plt.errorbar(mean_latency.index, mean_latency.values, yerr=error.values, fmt='o', color='blue', elinewidth=2, capsize=5, label='Barres d\'erreur')
plt.xlabel('File size')
plt.ylabel('LATENCY (ms)')
plt.title('LATENCY in line with File size')  
plt.grid(True)
plt.savefig("../plots/fileplot.PNG")
plt.close()




mean_latency = datas.groupby('threads')['LATENCY'].mean() * 1000
error = datas.groupby('threads')['LATENCY'].std() * 1000
plt.figure(figsize=(10, 6))

mean_latency.plot(kind='line', color='blue')
plt.scatter(mean_latency.index, mean_latency.values, color='blue', label='Points', s=50)
plt.errorbar(mean_latency.index, mean_latency.values, yerr=error.values, fmt='o', color='blue', elinewidth=2, capsize=5, label='Barres d\'erreur')
plt.xlabel('threads')
plt.ylabel('LATENCY (ms)')
plt.title('LATENCY in line with Threads')  
plt.grid(True)
plt.savefig("../plots/threadsPlot.PNG")
plt.close()




result = datas.groupby(['file_size', 'threads'])['LATENCY'].mean().unstack() * 1000
result.plot(kind='area', stacked=True, figsize=(10, 6))
plt.xlabel('file size')
plt.ylabel('LATENCY (ms)')
plt.title('LATENCY by File Size and Threads')
plt.legend(title='Threads')
plt.grid(True)
plt.savefig("../plots/fileThreadsplots.PNG")
plt.close()



result = datas.groupby(['key_size', 'threads'])['LATENCY'].mean().unstack() * 1000
result.plot(kind='area', stacked=True, figsize=(10, 6))
plt.xlabel('key_size')
plt.ylabel('LATENCY (ms)')
plt.title('LATENCY by Key Size and Threads')
plt.legend(title='Threads')
plt.grid(True)
plt.savefig("../plots/keyThreadsplots.PNG")
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

# Affiche le graphique assemblé
plt.savefig("../plots/compare3.PNG")
plt.close()



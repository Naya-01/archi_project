import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

current_path = os.getcwd()
print("Le chemin actuel est PPPPP:", current_path)
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
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


datas = pd.read_csv("./data/results.csv")

plots_path = "./plots"
file_extension = "pdf"
markers = ['o', 's', '^', 'D', '*']
colors = ['b', 'g', 'r', 'c', 'm', 'y']


def plot(size):
    data = datas[datas['file_size'] == size]
    average_req = data['REQ'].mean()
    std_dev_req = data['REQ'].std()

    plt.figure(figsize=(6,6))
    plt.bar(f'{size}', average_req, yerr=std_dev_req,color='skyblue', capsize=10)
    plt.xlabel('File size')
    plt.ylabel('Request/Sec')
    plt.title(f'Requêtes moyennes par seconde pour la taille de fichier {size}')
    plt.savefig(f"{plots_path}/REQ_bar_{size}.{file_extension}")
    plt.close()





plot(1024)
plot(262144)

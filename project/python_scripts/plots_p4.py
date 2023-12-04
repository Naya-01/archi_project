import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Lecture des données
datas_128 = pd.read_csv("./data/results_128.csv")
datas_256 = pd.read_csv("./data/results_256.csv")
datas_best = pd.read_csv("./data/results_best.csv")

plots_path = "./plots"
file_extension = "pdf"
colors = ['b', 'g', 'r']

def prepare_data(file_size):
    means = [
        datas_128[datas_128['file_size'] == file_size]['REQ'].mean(),
        datas_256[datas_256['file_size'] == file_size]['REQ'].mean(),
        datas_best[datas_best['file_size'] == file_size]['REQ'].mean()
    ]
    std_devs = [
        datas_128[datas_128['file_size'] == file_size]['REQ'].std(),
        datas_256[datas_256['file_size'] == file_size]['REQ'].std(),
        datas_best[datas_best['file_size'] == file_size]['REQ'].std()
    ]
    return means, std_devs

def plot(size):
    average_req, std_dev_req = prepare_data(size)
    labels = ['128', '256', 'Best']

    x = np.arange(len(labels)) 
    width = 0.35 

    fig, ax = plt.subplots()
    rects = ax.bar(x, average_req, width, yerr=std_dev_req, color=colors, capsize=10)

    ax.set_xlabel('SIMD version')
    ax.set_ylabel('REQ/s')
    ax.set_title('Moyenne de REQ/s par build pour la taille de fichier de ' + str(size))
    ax.set_xticks(x)
    ax.set_xticklabels(labels)

    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(round(height, 2)),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3), 
                    textcoords="offset points",
                    ha='center', va='bottom')

    fig.tight_layout()

    plt.savefig(f"{plots_path}/REQ_bar_{size}.{file_extension}")
    plt.close()

plot(262144)
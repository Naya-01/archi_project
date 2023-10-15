import os
import re
import matplotlib.pyplot as plt
import numpy as np


repertoire = 'results'
fichiers = os.listdir(repertoire)


def clear_content(content):
    lines = content.split('\n')
    non_empty_lines = [line.strip() for line in lines if line.strip() != '']
    text_without_empty_lines = '\n'.join(non_empty_lines)

    return text_without_empty_lines


def convert_to_milliseconds(value):
    if "us" in value:
        value = float(value.replace("us", "")) / 1000
    elif "ms" in value:
        value = float(value.replace("ms", ""))
    return value


def write_file(file_name, content):
    try:
        with open(file_name, 'a') as file:
            file.write(content)
            file.write("\n")
        print(f"Le contenu a été écrit avec succès dans '{file_name}'.")
    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")


def parse_Latency_Dist(content, key_size):
    lines = content.split('\n')

    end_index = lines.index("Detailed Percentile spectrum:")
    result = []
    for line in lines[end_index-1:end_index]:
        colonnes = line.split()
        percent, latency = colonnes[:2]
        latency = convert_to_milliseconds(latency)
        result.append(latency)
        print(f"key= {key_size} et latency = {latency}")

        nom_fichier = './measurements/resultatK{}.txt'.format(key_size)

        write_file(nom_fichier, str(latency))

    return result


keySizeOptions = [8, 16, 32, 64]

for i in keySizeOptions:
    for fichier in fichiers:
        if fichier.endswith("key{}.txt".format(i)):
            chemin_complet = os.path.join(repertoire, fichier)
            with open(chemin_complet, 'r') as f:
                contenu = f.read()
                contenu = clear_content(contenu)
                legacy = parse_Latency_Dist(contenu, i)
                print(f"Contenu du fichier {fichier} :\n{legacy}")


datas = []
datas.append(np.loadtxt("./measurements/resultatK8.txt"))
datas.append(np.loadtxt("./measurements/resultatK16.txt"))
datas.append(np.loadtxt("./measurements/resultatK32.txt"))
datas.append(np.loadtxt("./measurements/resultatK64.txt"))

mean = np.array([])
for data in datas:
    mean = np.append(mean, np.mean(data))

key = np.array(keySizeOptions)

# example
fig = plt.figure()
plt.plot(key, mean, linewidth=2)
plt.errorbar(key, mean, color='blue', marker='o')
plt.xlabel("Size of key")
plt.ylabel("Latency (ms)")
plt.title("Latency for each key")

plt.savefig("./firstK8.PNG")
plt.close()

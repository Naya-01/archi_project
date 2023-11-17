import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_requests_vs_cores_for_range():
    files = [f"../data/results_{i}.csv" for i in range(1, 9)]

    all_data = pd.DataFrame()

    for file in files:
        df = pd.read_csv(file)
        all_data = pd.concat([all_data, df], ignore_index=True)

    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))

    sns.scatterplot(data=all_data, x="cores", y="REQ")

    for core in all_data['cores'].unique():
        core_data = all_data[all_data['cores'] == core]
        plt.errorbar(core_data['cores'], core_data['REQ'], yerr=core_data['StdDeviation'],
                     linestyle='', elinewidth=1, capsize=5, label=f"Core {core}")

    plt.title('Requests/sec vs. Number of Cores with Variance')
    plt.xlabel("Number of Cores")
    plt.ylabel("Requests/sec")

    
    plt.savefig("../plots/cores_graph.pdf")


plot_requests_vs_cores_for_range()

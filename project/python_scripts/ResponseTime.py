import csv
import matplotlib.pyplot as plt
import numpy as np

csv_file_path = 'service_times.csv'

with open(csv_file_path, 'r') as file:
    reader = csv.reader(file)
    next(reader, None)
    service_times = [int(row[0]) for row in reader]

average_service_time = sum(service_times) / len(service_times)

csv_file_path = 'results.csv'

with open(csv_file_path, 'r') as file:
    reader = csv.DictReader(file)
    latencies = [float(row['LATENCY']) for row in reader]

average_latency = sum(latencies) / len(latencies)

def calculate_response_time(service_time, arrival_rate):
    response_time = 1 / (service_time - arrival_rate)
    return response_time

    
def plot_response_time_with_exponential(service_rate):
    arrival_rates = np.linspace(0, service_rate) 
    
    # Calculer les temps de réponse correspondants avec une distribution exponentielle des arrivées
    response_times = 1 / (service_rate - arrival_rates)
    
    # Tracer la fonction
    plt.plot(arrival_rates, response_times, label=f'E(R) = 1 / (µ - lambda)')
    
    # Ajouter des étiquettes et un titre
    plt.xlabel('Req/sec')
    plt.ylabel('Response time [s]')
    plt.title('Responsetime théorique')
    
    # Ajouter une légende et afficher la grille
    plt.legend()
    plt.grid(True)
    
    # Afficher le graphique
    plt.show()

def average_latency_by_rate(csv_file_path):
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        latency_by_rate = {}

        for row in reader:
            rate = float(row['rate'])
            latency = float(row['LATENCY'])
            if rate != 1:
                if rate in latency_by_rate:
                    latency_by_rate[rate]['sum'] += latency
                    latency_by_rate[rate]['count'] += 1
                else:
                    latency_by_rate[rate] = {'sum': latency, 'count': 1}

    # Calculer la moyenne pour chaque taux
    average_latencies = {rate: data['sum'] / data['count'] for rate, data in latency_by_rate.items()}

    # Trier les taux pour le tracé
    sorted_rates = sorted(average_latencies.keys())
    average_latencies_values = [average_latencies[rate] for rate in sorted_rates]

    # Tracer le graphique
    plt.plot(sorted_rates, average_latencies_values, marker='o', linestyle='-', color='b')
    
    # Ajouter des étiquettes et un titre
    plt.xlabel('Taux (rate)')
    plt.ylabel('Moyenne de la latence')
    plt.title('Moyenne de la latence en fonction du taux')
    
    # Afficher le graphique
    plt.show()

def plot_response_time_and_latency(csv_file_path, service_rate):
    # Créer une figure avec un seul sous-graphique
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Graphique 1: Temps de réponse théorique en fonction du taux d'arrivée
    arrival_rates = np.linspace(0, 9.5)
    response_times = 1 / (service_rate - arrival_rates)
    ax1.plot(arrival_rates, response_times, label=f'Theoretical')
    ax1.set_xlabel('Req/sec')
    ax1.set_ylabel('Response time [s]')
    ax1.legend(loc='upper left')
    ax1.grid(True)

    # Graphique 2: Moyenne de la latence en fonction du taux
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        latency_by_rate = {}

        for row in reader:
            rate = float(row['rate'])
            latency = float(row['LATENCY'])
            if rate != 1:
                if rate in latency_by_rate:
                    latency_by_rate[rate]['sum'] += latency
                    latency_by_rate[rate]['count'] += 1
                else:
                    latency_by_rate[rate] = {'sum': latency, 'count': 1}

    # Calculer la moyenne pour chaque taux
    average_latencies = {rate: data['sum'] / data['count'] for rate, data in latency_by_rate.items()}

    # Trier les taux pour le tracé
    sorted_rates = sorted(average_latencies.keys())
    average_latencies_values = [average_latencies[rate] for rate in sorted_rates]

    # Graphique 2 (suite): Ajouter la courbe de la moyenne de la latence sur le même axe
    ax1.plot(sorted_rates, average_latencies_values, marker='o', linestyle='-', color='r', label='experimental')
    ax1.legend(loc='upper center')

    # Afficher le graphique
    plt.title('Response Time theorical vs experimental')
    plt.show()

# Exemple d'utilisation avec un service rate de 1 et un maximum de 1000 req/sec
plot_response_time_with_exponential(1/(average_service_time/1000))

print(f"service rate : {1/(average_service_time/1000)}")
print(f"Le service time moyen est : {average_service_time} milliseconds")
print(f"Le response time moyen est : {average_latency} milliseconds")
average_latency_by_rate('results.csv')
plot_response_time_and_latency('results.csv', 1/(average_service_time/1000))




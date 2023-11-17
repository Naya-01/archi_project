#!/bin/bash


# Boucle pour effectuer les tests de 1 à 8 processus
for ((i=1; i<=8; i++)); do

    cd server_implementation

    # Modifier la ligne appropriée dans le Makefile
    sed -i "s/daemon off;worker_processes [0-9];/daemon off;worker_processes $i;/" Makefile

    # Recompilez le projet avec la nouvelle configuration
    sleep 20

    cd ..

    echo "$i"
    # Exécutez le test NPF
    npf-run --test test.npf --single-output "./data/results_$i.csv"

    # Appeler le script Python pour générer les graphiques
    #python3 "python_scripts/plots_p3.py" "./data/results_$i.csv"

    # Tuer le processus éventuel sur le port 8888
    PID=$(lsof -t -i :8888)
    if [ ! -z "$PID" ]; then
        kill -9 $PID
        echo "Processus avec PID $PID a été tué."
    else
        echo "Aucun processus n'écoute sur le port 8888."
    fi

done
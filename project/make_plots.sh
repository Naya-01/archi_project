#!/bin/bash

# make -C "./server_implementation" run_inginious &

#lua "./wrk_scripts/test.lua"

# # tests
# npf-run --test test.npf --single-output "./data/results.csv"

# # Appeler le script Python pour générer les graphiques
python3 "python_scripts/plots_p3.py"

# PID=$(lsof -t -i :8888)
# if [ ! -z "$PID" ]; then
#     kill -9 $PID
#     echo "Processus avec PID $PID a été tué."
# else
#     echo "Aucun processus n'écoute sur le port 8888."
# fi
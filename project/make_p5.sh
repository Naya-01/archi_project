#!/bin/bash

# make -C "./server_implementation" run_inginious &

# #lua "./wrk_scripts/test.lua"

# for ((i=2; i<=10; i++)); do
#     rate=$((i))
#     npf-run --test test.npf --variables RATE=$rate --single-output "./data/results__rate_$rate.csv"
#     rm -rf results
# done


python3 "python_scripts/plots_p5.py"

# PID=$(lsof -t -i :8888)
# if [ ! -z "$PID" ]; then
#     kill -9 $PID
#     echo "Processus avec PID $PID a été tué."
# else
#     echo "Aucun processus n'écoute sur le port 8888."
# fi
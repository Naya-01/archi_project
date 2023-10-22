#!/bin/bash

make -C "./server_implementation" run_inginious &

echo "Executing performance evaluation for generated Lua scripts..."

lua "./wrk_scripts/test.lua"

# echo "Performance evaluation completed."

# tests
npf-run --test test.npf --single-output "./data/results.csv"

# Appeler le script Python pour générer les graphiques
python "python_scripts/scriptCsv.py"

sleep 10

PID=$(lsof -t -i :8888)
if [ ! -z "$PID" ]; then
    kill -9 $PID
    echo "Processus avec PID $PID a été tué."
else
    echo "Aucun processus n'écoute sur le port 8888."
fi
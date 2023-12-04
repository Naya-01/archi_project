#!/bin/bash

lua "./wrk_scripts/test.lua"

make -C "./server_implementation" run_simd128_inginious &
npf-run --test test.npf --single-output "./data/results_128.csv"

PID=$(lsof -t -i :8888)
if [ ! -z "$PID" ]; then
    kill -9 $PID
    echo "Processus avec PID $PID a été tué."
else
    echo "Aucun processus n'écoute sur le port 8888."
fi


make -C "./server_implementation" run_simd256_inginious &
rm -rf results
npf-run --test test.npf --single-output "./data/results_256.csv"

PID=$(lsof -t -i :8888)
if [ ! -z "$PID" ]; then
    kill -9 $PID
    echo "Processus avec PID $PID a été tué."
else
    echo "Aucun processus n'écoute sur le port 8888."
fi


make -C "./server_implementation" run_simd512_inginious &
rm -rf results
npf-run --test test.npf --single-output "./data/results_512.csv"

PID=$(lsof -t -i :8888)
if [ ! -z "$PID" ]; then
    kill -9 $PID
    echo "Processus avec PID $PID a été tué."
else
    echo "Aucun processus n'écoute sur le port 8888."
fi


make -C "./server_implementation" run_simd_best_inginious &
rm -rf results
npf-run --test test.npf --single-output "./data/results_best.csv"

PID=$(lsof -t -i :8888)
if [ ! -z "$PID" ]; then
    kill -9 $PID
    echo "Processus avec PID $PID a été tué."
else
    echo "Aucun processus n'écoute sur le port 8888."
fi

rm -rf results

python3 "python_scripts/plots_p4.py"
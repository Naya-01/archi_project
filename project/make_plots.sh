#!/bin/bash

echo "Executing performance evaluation for generated Lua scripts..."

# lua "./wrk_scripts/test.lua"

# echo "Performance evaluation completed."

# # tests
# npf-run --test test.npf --single-output "../data/measurements.csv"

# Appeler le script Python pour générer les graphiques
python "python_scripts/scriptCsv.py"

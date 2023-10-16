#!/bin/bash

echo "Executing performance evaluation for generated Lua scripts..."

# Créer le répertoire pour les résultats
results_dir="results"
mkdir -p "$results_dir"

# Paramètres à tester
numRounds=("5")
file_sizes=("8" "16" "32" "64")
key_sizes=("8" "16" "32" "64")

# Durée du test (en secondes)
test_duration=30

# Itérer sur les combinaisons de paramètres
for numRound in "${numRounds[@]}"; do
  for size in "${file_sizes[@]}"; do
    for key in "${key_sizes[@]}"; do

      # Chemin du script Lua généré
      script_file="script_${key}_${size}_${numRound}.lua"

      # Générer le nom du fichier de sortie
      output_file="$results_dir/numRound${numRound}_size${size}_key${key}.csv"

      # Exécuter le script Lua avec wrk
      ../wrk2-DeathStarBench/wrk http://localhost:8888/ -d$test_duration --latency -R100 -s ./wrk_scripts/$script_file > $output_file

      echo "Test completed for  file_size=${size}, key=${key}"

    done
  done
done

echo "Performance evaluation completed."

# Appeler le script Python pour générer les graphiques
# python scriptGraph.py
#python keyScript.py
npf-run --test newTest.npf

import os
import re

# Absolute file path
absolute_path = os.path.abspath('./project/results/test.txt')

with open(absolute_path, 'r') as fichier:
    content = fichier.read()


lines = content.split('\n')
start_index = lines.index("       Value   Percentile   TotalCount 1/(1-Percentile)")

pattern = r".*#\[Mean\s+=.*"

for line in lines[start_index+1:]:

    if re.match(pattern, line): 
        break

    if line.strip() != "":
        colonnes = line.split()
        value, percentile, total_count, inverse_percentile = colonnes[:4]
        print(f"Value: {value}, Percentile: {percentile}, TotalCount: {total_count}, 1/(1-Percentile): {inverse_percentile}") #only to see the parse results


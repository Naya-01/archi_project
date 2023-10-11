import os
import re


def parse(file):
    lines = file.split('\n')
    start_index = lines.index(
        "       Value   Percentile   TotalCount 1/(1-Percentile)")

    pattern = r".*#\[Mean\s+=.*"

    for line in lines[start_index+1:]:

        if re.match(pattern, line):
            break

        if line.strip() != "":
            colonnes = line.split()
            value, percentile, total_count, inverse_percentile = colonnes[:4]
            # only to see the parse results
            print(
                f"Value: {value}, Percentile: {percentile}, TotalCount: {total_count}, 1/(1-Percentile): {inverse_percentile}")


folder = "results"
for file in os.listdir(folder):
    if os.path.isfile(os.path.join(folder, file)):
        with open(os.path.join(folder, file), 'r') as open_file:
            content = open_file.read()

            print(f"File name : {file}")
            parse(content)

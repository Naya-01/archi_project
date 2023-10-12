import os
import re
import matplotlib.pyplot as plt


def parse_In_Details(content):
    lines = content.split('\n')
    start_index = lines.index(
        "Value   Percentile   TotalCount 1/(1-Percentile)")

    pattern = r".*#\[Mean\s+=.*"

    result = []
    for line in lines[start_index+1:]:
        if re.match(pattern, line):
            break

        colonnes = line.split()
        r = colonnes[:4]
        result.append(r)

    return result


def parse_Latency_Dist(content):
    lines = content.split('\n')
    start_index = lines.index(
        "Latency Distribution (HdrHistogram - Recorded Latency)")

    end_index = lines.index("Detailed Percentile spectrum:")
    result = []
    for line in lines[start_index+1:end_index]:
        colonnes = line.split()
        r = colonnes[:2]
        result.append(r)

    return result


def clear_content(content):
    lines = content.split('\n')
    non_empty_lines = [line.strip() for line in lines if line.strip() != '']
    text_without_empty_lines = '\n'.join(non_empty_lines)

    return text_without_empty_lines


folder = "results"
for file in os.listdir(folder):
    if os.path.isfile(os.path.join(folder, file)):
        with open(os.path.join(folder, file), 'r') as open_file:
            content = open_file.read()

            print(f"File name : {file}")
            content = clear_content(content)

            latency = parse_Latency_Dist(content)
            details = parse_In_Details(content)

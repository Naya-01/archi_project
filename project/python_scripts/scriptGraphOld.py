import os
import re
import matplotlib.pyplot as plt
import numpy as np

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


def convert_to_milliseconds(value):
    if "us" in value:
        value = float(value.replace("us", "")) / 1000  
    elif "ms" in value:
        value = float(value.replace("ms", "")) 
    return value

def parse_Latency_Dist(content):
    lines = content.split('\n')
    start_index = lines.index(
        "Latency Distribution (HdrHistogram - Recorded Latency)")

    end_index = lines.index("Detailed Percentile spectrum:")
    result = []
    for line in lines[start_index+1:end_index]:
        colonnes = line.split()
        percent, latency = colonnes[:2]
        latency = convert_to_milliseconds(latency)
        percent = percent.split("%")[0]
        result.append([percent, latency])

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
            print(latency)

#example
fig = plt.figure()
plt.plot(np.sin(np.linspace(0, 20, 100)));
plt.savefig("./ok.PNG")
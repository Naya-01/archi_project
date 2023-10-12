import os
import re


def parse_In_Details(content):
    lines = content.split('\n')
    start_index = lines.index(
        "Value   Percentile   TotalCount 1/(1-Percentile)")

    pattern = r".*#\[Mean\s+=.*"

    for line in lines[start_index+1:]:
        if re.match(pattern, line):
            break

        colonnes = line.split()
        value, percentile, total_count, inverse_percentile = colonnes[:4]
        # only to see the parse results
        print(f"Value: {value}, Percentile: {percentile}, TotalCount: {total_count}, 1/(1-Percentile): {inverse_percentile}")
            

def parse_Latency_Dist(content):
    lines = content.split('\n')
    start_index = lines.index(
        "Latency Distribution (HdrHistogram - Recorded Latency)")

    end_index = lines.index("Detailed Percentile spectrum:")

    for line in lines[start_index+1:end_index]:
            colonnes = line.split()
            percent, latency = colonnes[:2]
            # only to see the parse results
            print(
                f"percent: {percent}, latency: {latency}")


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
            parse_Latency_Dist(content)
            parse_In_Details(content)



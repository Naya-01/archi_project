#!/usr/bin/bash
echo "Wow ! Don't just execute random scripts from the internet are you crazy ?"
echo "By the way this is where the scripts that runs your experiments and plots your data should go ! :)"

results_dir="results"
mkdir -p $results_dir

request_rates=("100")
file_sizes=("1024")
key_sizes=("16")
#request_rates=("100" "500" "1000")
#file_sizes=("1024" "4096" "8192")
#key_sizes=("16" "32" "64")

#threads=4
test_duration=30

for rate in "${request_rates[@]}"; do
  for size in "${file_sizes[@]}"; do
    for key in "${key_sizes[@]}"; do

      output_file="$results_dir/result_rate${rate}_size${size}_key${key}.csv"

      # Execute it from "project-2023-student/project"
      ../wrk2/wrk http://localhost:8888/ -d$test_duration --latency -R$rate -s ./wrk_scripts/post.lua >> $output_file
      #../wrk2-DeathStarBench/wrk http://localhost:8888/  -d$test_duration  --latency -R$rate -s ./wrk_scripts/test.lua > $output_file

      echo "Test completed for rate=${rate}, size=${size}, key=${key}"

    done
  done
done

# call script python
python scriptGraph.py
import glob
import os
import re

PATH = "logs/"

list_of_files = glob.glob(f"{PATH}*")
latest_file = max(list_of_files, key=os.path.getctime)
sorted_files = sorted(list_of_files, key=lambda x: int(x.split("/")[-1].split(".")[-2]), reverse=True)
top_two_files = sorted_files[:2]
file_with_largest_no = top_two_files[0]  # Keep the largest for compatibility

print_next = False
for f in top_two_files:
    with open(f) as file:
        for line in file:
            if "tunnelling instructions" in line:
                print_next = True
            if print_next:
                print(line.strip())
                exit(0)

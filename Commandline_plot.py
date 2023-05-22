import numpy as np
import time
import matplotlib.pyplot as plt
import argparse
from pathlib import Path
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument(
    "paths",
    type=argparse.FileType("r"),
    help="files to plot, accepts csv, CSV, xy and dat. To plot multiple files type $(ls) or only a certian filetype $(ls *csv)",
    nargs="+",
)
parser.add_argument(
    "-s",
    "--style",
    type=str,
    help=f"matplotlib style to use, options are: {plt.style.available}",
    default="seaborn-pastel",
)
parser.add_argument("-x", "--xlabel", type=str, help="label for x axis", default=None)
parser.add_argument("-y", "--ylabel", type=str, help="label for y axis", default=None)
delimiters = {"csv": ",", "CSV": ",", "dat": "\t", "xy": " "}
args = parser.parse_args()
plt.style.use(args.style)
files_to_plot = dict()
start = time.time()
for file_location in args.paths:
    file_type = file_location.name.split(".")[-1]
    data = pd.read_csv(file_location, delimiter=delimiters[file_type])

    files_to_plot[file_location] = data
load = time.time()

# print(f"Load time is {load-start}")
fig, ax = plt.subplots()
for data in files_to_plot:
    # print(csv_file)
    if "CSV" in data.name:
        ax.plot(
            files_to_plot[data].iloc[4500:, 0],
            files_to_plot[data].iloc[4500:, 1],
            label=data,
        )
    else:
        for i in range(1, files_to_plot[data].shape[1]):
            if files_to_plot[data].shape[1] > 2 and ".dat" not in data.name:
                label = files_to_plot[data].iloc[:, i].name
            else:
                label = data
            ax.plot(
                files_to_plot[data].iloc[:, 0],
                files_to_plot[data].iloc[:, i],
                label=label,
            )

# print(f"Plot time is {time.time()-load}")
ax.set_xlabel(args.xlabel)
ax.set_ylabel(args.ylabel)
plt.show()

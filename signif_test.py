import numpy as np
from scipy.stats import ttest_ind

with open("./runtime.txt") as f:
    all_data = f.read().split("\n")
    with_ = []
    without_ = []
    for data in all_data:
        if data.split(" ")[1] == "with":
            with_.append(float(data.split(" ")[-1]))
        if data.split(" ")[1] == "without":
            without_.append(float(data.split(" ")[-1]))
with_ = np.array(with_)
without_ = np.array(without_)
res = ttest_ind(with_, without_).pvalue

print(res)
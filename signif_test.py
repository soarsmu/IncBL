import numpy as np
from scipy.stats import ttest_ind
import pandas as pd
with open("./runtime1.txt") as f:
    all_data = f.read().split("\n")
    with_ = []
    without_ = []
    for data in all_data:
        if data.split(" ")[2] == "without":
            with_.append(float(data.split(" ")[-1]))
        if data.split(" ")[1] == "with":
            without_.append(float(data.split(" ")[-1]))
with_ = np.array(with_)
without_ = np.array(without_)
res = ttest_ind(with_, without_).pvalue
print(res, len(with_), len(without_))
rate = []
for i in range(len(with_)):
    rate.append(with_[i]/without_[i])

# rate=pd.DataFrame(data=rate)

# rate.to_csv('./rate.csv')

# print(rate)
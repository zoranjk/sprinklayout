import csv
import seaborn as sns
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt
import etl

# farm = list(csv.reader(open("/home/zoran/sprinklayout/farmlands/meadowlands_sw.csv")))
# farm = np.loadtxt(open("/home/zoran/sprinklayout/farmlands/meadowlands_sw.csv", "rb"), delimiter=",", skiprows=0)
farm = etl.csv_to_np("/home/zoran/sprinklayout/farmlands/meadowlands_sw.csv")


for i in range(len(farm)):
    for j in range(len(farm[0])):
        print(int(farm[i][j]), end='')

    print()

# sns.heatmap(farm)
# plt.show()
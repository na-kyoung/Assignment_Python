# 1개 열의 막대 그래프 출력

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('../../data/UR2 BXPC3 raman raw data__24h.csv')

x = []
y = np.array(df['ROI 1 []'])
yy = np.delete(y,0)

for i in range(len(df)-1):
    x.append(i)

plt.figure(figsize=(15, 10))

plt.bar(x, yy)

plt.show()


# 2개 열의 각각 산점도 그래프 출력

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('../../data/UR2 BXPC3 raman raw data__24h.csv')

x = []
y1 = np.array(df['ROI 10 []'])
yy1 = np.delete(y1,0)
y2 = np.array(df['ROI 8 []'])
yy2 = np.delete(y2,0)

for i in range(len(df)-1):
    x.append(i)

plt.figure(figsize=(15, 10))
plt.scatter(x, yy1, s=10, c='blue')
plt.scatter(x, yy2, s=10, c='red')

plt.show()


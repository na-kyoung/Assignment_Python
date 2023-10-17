# 3개 열로 각각의 바이올린 그래프 출력

import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('../data/UR2 BXPC3 raman raw data__24h.csv')

y1 = np.array(df['ROI 10 []'])
yy1 = np.delete(y1,0)
y2 = np.array(df['ROI 9 []'])
yy2 = np.delete(y2,0)
y3 = np.array(df['ROI 8 []'])
yy3 = np.delete(y3,0)

plt.figure(figsize=(12, 8))

plt.violinplot(yy1, positions=[2], showmeans=True)
plt.violinplot(yy2, positions=[3], showmeans=True)
plt.violinplot(yy3, positions=[4], showmeans=True)

plt.ylim([10, 50])
plt.xticks(np.arange(1, 6))

plt.show()


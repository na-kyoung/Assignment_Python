# 모든 열의 선 그래프 출력

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('../../data/UR2 BXPC3 raman raw data__24h.csv')

df1 = df['ROI 1 []']
df2 = df['ROI 2 []']
df3 = df['ROI 3 []']
df4 = df['ROI 4 []']
df5 = df['ROI 5 []']
df6 = df['ROI 6 []']
df7 = df['ROI 7 []']
df8 = df['ROI 8 []']
df9 = df['ROI 9 []']
df10 = df['ROI 10 []']
df11 = df['ROI 11 []']
df12 = df['ROI 12 []']
df13 = df['ROI 13 []']

plt.figure(figsize=(18, 10))

plt.plot(df1, label='ROI 1 []')
plt.plot(df2, label='ROI 2 []')
plt.plot(df3, label='ROI 3 []')
plt.plot(df4, label='ROI 4 []')
plt.plot(df5, label='ROI 5 []')
plt.plot(df6, label='ROI 6 []')
plt.plot(df7, label='ROI 7 []')
plt.plot(df8, label='ROI 8 []')
plt.plot(df9, label='ROI 9 []')
plt.plot(df10, label='ROI 10 []')
plt.plot(df11, label='ROI 11 []')
plt.plot(df12, label='ROI 12 []')
plt.plot(df13, label='ROI 13 []')

plt.legend(ncol=1, loc='upper right', fontsize=12)
plt.show()


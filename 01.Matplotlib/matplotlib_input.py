# 열 입력 시, 해당 열의 선 그래프 출력

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('../../data/UR2 BXPC3 raman raw data__24h.csv')

col = df.columns

code = input("열 입력 : ")

if code in col:
    df = df[code]

plt.figure(figsize=(18, 10))

plt.plot(df, label=code)

plt.legend(ncol=1, loc='upper right', fontsize=12)
plt.show()


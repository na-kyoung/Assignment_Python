# for문을 활용하여 모든 열의 선 그래프 출력

import matplotlib.pyplot as plt
import pandas as pd

file = '../data/UR2 BXPC3 raman raw data__24h.csv'
df = pd.read_csv(file)


cols = len(df.columns) - 1
# rows = len(df)

df['Axis [nm]'] = df['Axis [nm]'].replace('[\$,]', '', regex=True).astype(float)
x = df['Axis [nm]']

plt.figure(figsize=(15, 8))
for i in range(1,cols+1):
    colName = f'ROI {i} []'
    df[colName] = df[colName].replace('[\$,]', '', regex=True).astype(float)
    y = df[colName]

    plt.plot(x,y,label=colName)
    #plt.xlabel(df.columns[i])
    #plt.ylabel(df.columns[0])
    #plt.axis([860,975,0,55])
    #plt.title(colName+" "+'Axis')
    plt.legend(loc='upper right',frameon=True)

plt.show()


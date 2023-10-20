# 데이터 전처리 - 정규화 최대최소(MinMax)
# 0. 데이터 및 그래프 출력
# 1. 전체 데이터 수 확인
# 2. 결측치 확인
# 3. Null값 확인
# 4. 중복값 확인
# 5. 이상치 확인 및 제거
# 6. 정규화 - 최대최소(MinMax)
# 7. 데이터 및 그래프 출력

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# 파일 불러오기 & 데이터 출력
file = '../../data/UR2 BXPC3 raman raw data__24h.csv'
df = pd.read_csv(file)
print("전처리 전 데이터 출력 \n")
print(df.head())

# 그래프 출력
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
    plt.title("Before Data Processing")
    plt.legend(loc='upper right',frameon=True)

plt.show()


# 데이터 수 확인
print('전체 데이터 개수 :', len(df)) # 546개
print("\n")

# 결측치
print('칼럼별 결측치 개수')
print(len(df) - df.count()) #0개
print("\n")

# Null값
print('칼럼별 Null값 개수')
print(df.isnull().sum()) # 0개
print("\n")

# 중복값
print('중복 데이터 개수')
print(df.duplicated().sum()) # 0
print(df[df.duplicated()]) # Empty DataFrame
print("\n")


# 이상치 칼럼 추출 함수 (IQR - 25%~75% 범위를 벗어난 값을 이상치로 판단)
def get_outlier(df=None, column=None, weight=1.5):
    # 25%, 75% 값 설정
    quantile_25 = np.percentile(df[column].values, 25)
    quantile_75 = np.percentile(df[column].values, 75)
    
    IQR = quantile_75 - quantile_25
    IQR_weight = IQR*weight
    
    lowest = quantile_25 - IQR_weight
    highest = quantile_75 + IQR_weight
    
    outlier_idx = df[column][ (df[column] < lowest) | (df[column] > highest) ].index
    return outlier_idx

# 이상치 제거
# outlier_idx = get_outlier(df=df, column='ROI 1 []', weight=1.5)
# df.drop(outlier_idx, axis=0, inplace=True)


# 정규화 - 최대최소(MinMax)
df_minmax = (df - df.min())/(df.max() - df.min())
print("전처리 후 데이터 출력 \n")
print(df_minmax.head())
print("\n")


# 그래프 출력
cols = len(df_minmax.columns) - 1
# rows = len(df)

df_minmax['Axis [nm]'] = df_minmax['Axis [nm]'].replace('[\$,]', '', regex=True).astype(float)
x = df_minmax['Axis [nm]']

plt.figure(figsize=(15, 8))
for i in range(1,cols+1):
    colName = f'ROI {i} []'
    df_minmax[colName] = df_minmax[colName].replace('[\$,]', '', regex=True).astype(float)
    y = df_minmax[colName]
     
    plt.plot(x,y,label=colName)
    #plt.xlabel(df.columns[i])
    #plt.ylabel(df.columns[0])
    #plt.axis([860,975,0,55])
    #plt.title(colName+" "+'Axis')
    plt.title("After Data Processing")
    plt.legend(loc='upper right',frameon=True)

plt.show()


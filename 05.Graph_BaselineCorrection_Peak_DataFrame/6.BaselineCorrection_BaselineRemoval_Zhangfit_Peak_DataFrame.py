# 라이브러리 BaselineRemoval를 활용한 Graph Baseline Correction

# 2 개의 파일 불러와 Zhangfit 함수 이용해 베이스라인 보정
# 베이스라인 보정 후 두 그래프 출력

# 그래프 Peak 점 표시
# Peak 점의 x좌표, x좌표별 y좌표 차이값 출력

# 두 그래프의 x좌표별 y값 차이값 데이터프레임 출력
# 데이터프레임 검색 - x좌표 검색 시 차이값 출력

import numpy as np
import pandas as pd
import rampy
from matplotlib import pyplot as plt
from BaselineRemoval import BaselineRemoval
from scipy.signal import find_peaks, peak_prominences

# 데이터 로드 df1 - Raw / df2 - UR2
df1 = pd.read_csv('../../data/new_fix/cnt_new_4lipids_fix.csv')
df2 = pd.read_csv('../../data/new_fix/ur2_4lipids_fix.csv')

# 빈 리스트
list1 = []
list2 = []

# 소수점 둘째 자리까지 반올림
df1 = df1.round(2)
df2 = df2.round(2)

# 첫번째 행 읽기
col1 = df1.columns
col2 = df2.columns

# X축 데이터
x1 = df1[col1[0]]
x2 = df2[col2[0]]

# Raw - Y좌표
for i in range(1,len(col1)):
    colName = f'ROI {i} []'
    #df1[colName] = df1[colName].replace('[\$,]', '', regex=True).astype(float)
    list1.append(colName)

# UR2 - Y좌표
for i in range(1,len(col2)):
    colName = f'ROI {i} []'
    #df2[colName] = df2[colName].replace('[\$,]', '', regex=True).astype(float)
    list2.append(colName)

# Y좌표 평균값
y1 = df1[list1].mean(axis=1).values
y2 = df2[list2].mean(axis=1).values

# 베이스라인 조정
baseObj1 = BaselineRemoval(y1)
baseObj2 = BaselineRemoval(y2)
Zhangfit_output1 = baseObj1.ZhangFit()
Zhangfit_output2 = baseObj2.ZhangFit()

# peak 변수
baselined_spectrum1 = Zhangfit_output1
baselined_spectrum2 = Zhangfit_output2

# peak값 찾기
peaks, _ = find_peaks(baselined_spectrum1, height=0, width=2)
prominences = peak_prominences(baselined_spectrum1, peaks)[0]
prominence_new = np.percentile(prominences, [0, 25, 50, 75, 80, 100], interpolation='nearest')[3]
peaks, _ = find_peaks(baselined_spectrum1, prominence=prominence_new)

peaks, _ = find_peaks(baselined_spectrum2, height=0, width=2)
prominences = peak_prominences(baselined_spectrum2, peaks)[0]
prominence_new = np.percentile(prominences, [0, 25, 50, 75, 80, 100], interpolation='nearest')[3]
peaks, _ = find_peaks(baselined_spectrum2, prominence=prominence_new)

# 그래프 그리기
plt.figure(figsize=(15,10))
#plt.plot(x1,y1)
#plt.plot(x2, y2)
plt.plot(x1, Zhangfit_output1, label='Raw', color='blue')
plt.plot(x2, Zhangfit_output2, label='UR2', color='red')
#plt.axhline(y=min(Zhangfit_output1), label='min(Raw)', color='gray')
plt.axhline(y=min(Zhangfit_output2), label='min(UR2)', color='gray')
#plt.axhline(y=0, label='y=0', color='gray')

# peak값 그래프 표시 (UR2)
for i in range(len(peaks)):
    x_value = x2[peaks[i]]  # x 값
    plt.plot(x_value, baselined_spectrum2[peaks[i]], "go")

# 피크점 수치 출력 (파수, UR2-Raw)
for i in range(len(peaks)):
    x_value = x2[peaks[i]]  # 피크의 x 값
    y_value1 = baselined_spectrum1[peaks[i]]  # 피크의 y 값
    y_value2 = baselined_spectrum2[peaks[i]]  # 피크의 y 값
    change_value = y_value2 - y_value1 # (UR2 - Raw) 차이
    x_value = int(x_value)
    plt.text(x_value, y_value2, f'{x_value} \n +{change_value: .2f}', fontsize=10, verticalalignment='bottom')

# 그래프 범례 및 띄우기
plt.xlabel('Wavelength')
plt.ylabel('Intensity')
plt.title('Comparsion After Baseline Correction')
plt.legend()
plt.show()

# wavelength 리스트 정수 변환
x_int = list(map(int, x1))

# 차이값 데이터프레임 생성
df_change = pd.DataFrame({
    'Wavelength' : x_int,
    'ChangeValue' : Zhangfit_output2-Zhangfit_output1
})

# 데이터프레임 내 검색
search_value = int(input("wavelength : "))

for i in range(len(x_int)):
    if x_int[i] == search_value:
        #print(df_change.loc[i,['ChangeValue']])
        print(df_change.loc[i])

df_change

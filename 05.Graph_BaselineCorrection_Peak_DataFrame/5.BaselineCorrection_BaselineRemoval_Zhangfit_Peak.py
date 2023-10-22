# 라이브러리 BaselineRemoval를 활용한 Graph Baseline Correction
# Zhangfit 함수 이용해 베이스라인 보정
# 베이스라인 보정 전/후 그래프 출력
# 그래프 각각 Peak 점 표시
# Peak 점의 좌표 출력

import numpy as np
import pandas as pd
import rampy
from matplotlib import pyplot as plt
from BaselineRemoval import BaselineRemoval
from scipy.signal import find_peaks, peak_prominences

# 데이터 로드
df = pd.read_csv('../../data/UR2 BXPC3 raman raw data__24h.csv')

# 소수점 둘째 자리까지 반올림
df = df.round(2)

# 관심 영역 선택 (ROI)
roi_columns = ['ROI 1 []', 'ROI 2 []', 'ROI 3 []', 'ROI 4 []', 'ROI 5 []', 'ROI 6 []', 'ROI 7 []', 'ROI 8 []', 'ROI 9 []', 'ROI 10 []', 'ROI 11 []', 'ROI 12 []', 'ROI 13 []']
roi_data = df[roi_columns]

# X축 데이터
x = df['Axis [nm]'].values

# Y축 데이터 평균
y = roi_data.mean(axis=1).values  # pandas Series에서 numpy 배열로 변환

# 다항식 차수
polynomial_degree = 3

# 베이스라인 조정
baseObj = BaselineRemoval(y)
Modpoly_output = baseObj.ModPoly(polynomial_degree)
Imodpoly_output = baseObj.IModPoly(polynomial_degree)
Zhangfit_output = baseObj.ZhangFit()

#print('Raw Data:',y)
#print('Modpoly base corrected values:',Modpoly_output)
#print('IModPoly base corrected values:',Imodpoly_output)
#print('ZhangFit base corrected values:',Zhangfit_output)

# peak 변수 (Zhangfit)
baselined_spectrum = Zhangfit_output

# peak값 찾기 (Zhangfit)
peaks, _ = find_peaks(baselined_spectrum, height=0, width=2)
prominences = peak_prominences(baselined_spectrum, peaks)[0]
prominence_new = np.percentile(prominences, [0, 25, 50, 75, 80, 100], interpolation='nearest')[4]
peaks, _ = find_peaks(baselined_spectrum, prominence=prominence_new)

# peak 변수 (raw)
baselined_spectrum_y = y

# peak값 찾기 (raw)
peaks, _ = find_peaks(baselined_spectrum_y, height=0, width=2)
prominences = peak_prominences(baselined_spectrum_y, peaks)[0]
prominence_new = np.percentile(prominences, [0, 25, 50, 75, 80, 100], interpolation='nearest')[4]
peaks, _ = find_peaks(baselined_spectrum_y, prominence=prominence_new)

# 그래프 그리기
plt.figure(figsize=(15,10))
plt.plot(x, y, label='raw', color='blue')
plt.plot(x, Zhangfit_output, label='Zhangfit', color='red')
#plt.plot(x, Modpoly_output, label='modpoly', color='green')
#plt.plot(x, Imodpoly_output, label='Imodpoly', color='pink')
plt.axhline(y=min(Zhangfit_output), color='gray')
plt.axhline(y=min(y), color='gray')
#plt.axhline(y=min(Modpoly_output), color='gray')
#plt.axhline(y=min(Imodpoly_output), color='gray')

# peak값 그래프 표시 (Zhangfit)
for i in range(len(peaks)):
    x_value = x[peaks[i]]  # 그리고자 하는 x 값
    plt.plot(x_value, baselined_spectrum[peaks[i]], "x")

# 피크점 수치 출력 (Zhangfit)
for i in range(len(peaks)):
    x_value = x[peaks[i]]  # 피크의 x 값
    y_value = baselined_spectrum[peaks[i]]  # 피크의 y 값
    plt.text(x_value, y_value, f'({x_value:.2f}, {y_value:.2f})', fontsize=10, verticalalignment='bottom')
    
# peak값 그래프 표시 (raw)
for i in range(len(peaks)):
    x_value = x[peaks[i]]  # 그리고자 하는 x 값
    plt.plot(x_value, baselined_spectrum_y[peaks[i]], "x")

# 피크점 수치 출력 (raw)
for i in range(len(peaks)):
    x_value = x[peaks[i]]  # 피크의 x 값
    y_value = baselined_spectrum_y[peaks[i]]  # 피크의 y 값
    plt.text(x_value, y_value, f'({x_value:.2f}, {y_value:.2f})', fontsize=10, verticalalignment='bottom')

    
plt.legend()
plt.show()

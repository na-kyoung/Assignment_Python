# 라이브러리 Scipy를 활용한 Graph Baseline Correction
# detrend 함수를 이용한 베이스라인 보정
# 베이스라인 보정 전후 그래프 출력

import numpy as np
import pandas as pd
import rampy
from matplotlib import pyplot as plt
from BaselineRemoval import BaselineRemoval
from scipy import signal

# 데이터 로드
df = pd.read_csv('../../data/UR2 BXPC3 raman raw data__24h.csv')

# 데이터에서 추세 제거
#detrended_data = signal.detrend(df)

# 소수점 둘째 자리까지 반올림
#df = df.round(2)

# 관심 영역 선택 (ROI)
roi_columns = ['ROI 1 []', 'ROI 2 []', 'ROI 3 []', 'ROI 4 []', 'ROI 5 []', 'ROI 6 []', 'ROI 7 []', 'ROI 8 []', 'ROI 9 []', 'ROI 10 []', 'ROI 11 []', 'ROI 12 []', 'ROI 13 []']
roi_data = df[roi_columns]

# X축 데이터
x = df['Axis [nm]'].values

# Y축 데이터 평균
y = roi_data.mean(axis=1).values  # pandas Series에서 numpy 배열로 변환
detrended_data = signal.detrend(y) # 데이터에서 추세 제거

# 그래프 그리기
plt.figure(figsize=(15,10))
plt.plot(x, y, label='raw', color='blue')
plt.plot(x, detrended_data, label='detrended_data', color='red')
plt.axhline(y=min(y), color='gray')
plt.axhline(y=min(detrended_data), color='gray')

plt.legend()
plt.show()

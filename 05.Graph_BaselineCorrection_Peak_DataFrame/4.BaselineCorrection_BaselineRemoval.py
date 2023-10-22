# 라이브러리 BaselineRemoval를 활용한 Graph Baseline Correction
# 3가지 함수로 각각 베이스라인 보정 (ModPoly, IModPoly, ZhangFit)
# 베이스라인 보정 전/후 그래프 출력

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from BaselineRemoval import BaselineRemoval

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

#for i in Zhangfit_output:
#    if i < 0 :
#        print(i)

# 그래프 그리기
plt.figure(figsize=(15,10))
plt.plot(x, y, label='raw', color='blue')
plt.plot(x, Modpoly_output, label='modpoly', color='green')
plt.plot(x, Imodpoly_output, label='Imodpoly', color='pink')
plt.plot(x, Zhangfit_output, label='Zhangfit', color='red')
plt.axhline(y=min(y), color='gray')
plt.axhline(y=0, color='gray')

plt.legend()
plt.show()

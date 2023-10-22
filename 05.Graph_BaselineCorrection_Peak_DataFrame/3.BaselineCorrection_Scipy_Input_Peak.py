# 라이브러리 Scipy를 활용한 Graph Baseline Correction

# 기준점 개수 입력 (2 이상)
# 입력받은 기준점 개수로 기준선 만듦
# 기준선을 기준으로 베이스라인 보정
# 베이스라인 보정 전/후 그래프 출력
# 베이스라인 보정 후 그래프
# - 엑셀 파일 불러와, x좌표에 맞는 성분 출력
# - Peak 점 표시
# - Peak 점의 좌표 출력

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import sparse
from scipy.sparse.linalg import spsolve
from scipy.signal import find_peaks, peak_prominences

# 파일 불러오기
file = '../../data/UR2 BXPC3 raman raw data__24h.csv'
df = pd.read_csv(file)

# x축 값 지정
x = df['Axis [nm]'].replace('[\$,]', '', regex=True).astype(float)

# y축 값 지정
y = df['ROI 10 []'].replace('[\$,]', '', regex=True).astype(float)

# 기준점 개수 n 입력받기
n = int(input("기준점 개수: "))

# 기준점 수 예외처리
if n < 2:
    print("기준점은 2개 이상 필요합니다.")
    exit()

# 기준점 인덱스
nlist = []
for i in range(0, n - 1):
    nlist.append(int(len(x) / (n - 1) * i))
nlist.append(len(x) - 1)

# 기준점 x, y좌표
a = []
b = []
for i in nlist:
    a.append(x[i])
    b.append(y[i])

# Baseline Correction 함수
def baseline_als(y, lam, p, niter=100):
    L = len(y)
    D = sparse.diags([1, -2, 1], [0, -1, -2], shape=(L, L - 2))
    w = np.ones(L)
    for i in range(niter):
        W = sparse.spdiags(w, 0, L, L)
        Z = W + lam * D.dot(D.transpose())
        z = spsolve(Z, w * y)
        w = p * (y > z) + (1 - p) * (y < z)
    return z

# 기존-최소값
#baselined_spectrum = y - y.min() # 최소값 뺀 y축 값

# 기존-기준선
baselined_spectrum = y - min(b)

# peak값 찾기
peaks, _ = find_peaks(baselined_spectrum, height=0, width=2)
prominences = peak_prominences(baselined_spectrum, peaks)[0]
prominence_new = np.percentile(prominences, [0, 25, 50, 75, 100], interpolation='nearest')[3]
peaks, _ = find_peaks(baselined_spectrum, prominence=prominence_new)

# 성분 데이터
# additional_data = pd.read_excel('../../data/additional_data.xlsx')

# 필요한 성분과 해당하는 주파수 가져오기
# assignment = additional_data['Assignment']
# frequency = additional_data['Frequency(RAMAN)']
# sample = additional_data['Samle']

# 그래프 형식 지정
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(18, 12))

# ax1 그래프 (기존, 기준선)
ax1.plot(x, y, color='black')
ax1.plot(a, b, 'ro-')
#ax1.axhline(y=np.mean(b))
ax1.set_title('Before Baseline Correction', fontsize=15)
ax1.set_xlabel('Wavelength', fontsize=13)
ax1.set_ylabel('Intensity', fontsize=13)
#ax1.legend()

# ax2 그래프 (기존 - 기준선)
ax2.plot(x, baselined_spectrum, color = 'black')
# ax2.plot(x, 0*x, color="green")
ax2.set_title('After Baseline Correction', fontsize = 15)
ax2.set_xlabel('Wavelength', fontsize = 13)
ax2.set_ylabel('Intensity',  fontsize = 13)

# ax2 그래프 (y=0)
ax2.axhline(y=0,color='green', label='y=0')
ax2.legend()

# peak값 그래프 표시
for i in range(len(peaks)):
    x_value = x[peaks[i]]  # 그리고자 하는 x 값
    ax2.plot(x_value, baselined_spectrum[peaks[i]], "x")

# peak점 수치 출력
for i in range(len(peaks)):
    x_value = x[peaks[i]]  # 피크의 x 값
    y_value = baselined_spectrum[peaks[i]]  # 피크의 y 값
    ax2.text(x_value, y_value, f'({x_value:.2f}, {y_value:.2f})', fontsize=8, verticalalignment='bottom')

# 성분 데이터 표시
#for i in range(len(assignment)):
#    freq = frequency[i]
#    sample_name = sample[i]
#    idx = np.abs(x - freq).argmin()
#    ax2.text(x[idx], baselined_spectrum[idx], sample_name, fontsize=8, verticalalignment='top')

# 그래프 띄우기
plt.show()

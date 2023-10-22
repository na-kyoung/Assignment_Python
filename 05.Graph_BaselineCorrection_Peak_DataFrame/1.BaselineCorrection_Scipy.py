# 라이브러리 Scipy를 활용한 Graph Basline Correction
# csv 파일 불러와, 베이스라인 보정 전후 그래프 출력

# https://towardsdatascience.com/data-science-for-raman-spectroscopy-a-practical-example-e81c56cf25f

from scipy import sparse
from scipy.sparse.linalg import spsolve
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# 파일 불러오기
file = '../../data/UR2 BXPC3 raman raw data__24h.csv'
df = pd.read_csv(file)

cols = len(df.columns) - 1
# rows = len(df)

df['Axis [nm]'] = df['Axis [nm]'].replace('[\$,]', '', regex=True).astype(float)
x = df['Axis [nm]']

# for i in range(1,cols+1):
i = 2
colName = f'ROI {i} []'
df[colName] = df[colName].replace('[\$,]', '', regex=True).astype(float)
y = df[colName]
 
#plt.figure()
#plt.plot(x,y)
#plt.xlabel(df.columns[i])
#plt.ylabel(df.columns[0])
#plt.axis([860,975,0,55])
#plt.title(colName+" "+'Axis')

#plt.show()

# Baseline stimation function:
def baseline_als(y, lam, p, niter=100):
    L = len(y)
    D = sparse.diags([1,-2,1],[0,-1,-2], shape=(L,L-2))
    w = np.ones(L)
    for i in range(niter):
        W = sparse.spdiags(w, 0, L, L)
        Z = W + lam * D.dot(D.transpose())
        z = spsolve(Z, w*y)
        w = p * (y > z) + (1-p) * (y < z)
    return z

# For more info see the paper and https://stackoverflow.com/questions/29156532/python-baseline-correction-library

# Parameters for this case:
l = 1000000 # smoothness, baseline을 얼마나 부드럽게 추정할지를 결정. 이 값을 높게 설정하면 데이터의 잡음에 덜 민감한 baseline이 생성될 수 있지만, 실제 baseline의 변화를 덜 반영할 수도 있습니다. chatGPT said..
p = 0.05 # asymmetry. 비대칭성.
# 양쪽으로 비대칭적으로 어떤 정도의 기울기를 허용할지를 결정합니다. 값이 작을수록 추정된 baseline은 더 많은 비대칭성을 가집니다

# Estimation of the baseline:
estimated_baselined = baseline_als(y, l, p)

# Baseline subtraction:
baselined_spectrum = y - estimated_baselined

# How does it look like?
fig, (ax1, ax2) = plt.subplots(1,2, figsize=(16,4))

# We compared the original mix spectrum and the estimated baseline:
ax1.plot(x, y, color = 'black', label = 'Mix spectrum with noise' )
ax1.plot(x, estimated_baselined, color = 'red', label = 'Estimated baseline')
ax1.set_title('Baseline estimation', fontsize = 15)
ax1.set_xlabel('Wavelength', fontsize = 15)
ax1.set_ylabel('Intensity',  fontsize = 15)
ax1.legend()

# We plot the mix spectrum after baseline subtraction
ax2.plot(x, baselined_spectrum, color = 'black', label = 'Baselined spectrum with noise' )
ax2.set_title('Baselined spectrum (original - baseline)', fontsize = 15)
ax2.set_xlabel('Wavelength', fontsize = 15)
ax2.set_ylabel('Intensity',  fontsize = 15)
plt.show()

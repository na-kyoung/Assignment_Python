# CSV 파일을 불러오면,
# 1. 데이터 출력
# 2. 모든 열 직선 그래프
# 3. 모든 열 산점도 그래프
# 4. 첫번째 열 막대 그래프

from tkinter import *
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import pandas as pd

from os import path


# 파일 불러오기
def open_file():
    # csv 파일만 보이도록 설정
    filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

    if filepath:
        # 파일 데이터 가져오기
        df = pd.read_csv(filepath)
        text.delete("1.0", tk.END)  
        text.insert(tk.END, df.to_string())
        
        linegraph(df) # 직선 그래프
        scatter(df) # 산점도 그래프
        barchart(df) # 막대 그래프


# 직선 그래프 함수
def linegraph(df):
    cols = len(df.columns) - 1

    df['Axis [nm]'] = df['Axis [nm]'].replace('[\$,]', '', regex=True).astype(float)
    x = df['Axis [nm]']
    
    #fig = plt.figure()
    fig = plt.figure(figsize=(5,4))
    
    # column이 여러개 있어도 반영
    for i in range(1,cols+1):
        colName = f'ROI {i} []'
        df[colName] = df[colName].replace('[\$,]', '', regex=True).astype(float)
        y = df[colName]
         
        plt.plot(x,y,label=colName)
        plt.xlabel(df.columns[0])
        plt.ylabel('intensity')
        # x,y좌표 길이
        plt.axis([860,975,0,55])
        
        #plt.legend(loc='lower left', bbox_to_anchor=(1.0,0.0),frameon=True)
        plt.title("Line Graph")
        plt.tight_layout()
        
    # 화면에 직선 그래프 출력
    canvas = FigureCanvasTkAgg(fig,master=root) 
    canvas.get_tk_widget().pack(side='left', padx=10)

# 산점도 그래프 함수
def scatter(df):
    cols = len(df.columns) - 1
    
    df['Axis [nm]'] = df['Axis [nm]'].replace('[\$,]', '', regex=True).astype(float)
    x = df['Axis [nm]']

    #fig = plt.figure()
    fig = plt.figure(figsize=(5,4))
    
    for i in range(1,cols+1):
        colName = f'ROI {i} []'
        df[colName] = df[colName].replace('[\$,]', '', regex=True).astype(float)
        y = df[colName]
        
        plt.scatter(x,y)
        plt.title("Scatter Graph")
        plt.tight_layout()
    
    # 화면에 산점도 그래프 출력
    canvas = FigureCanvasTkAgg(fig,master=root)
    canvas.get_tk_widget().pack(side='left')

# 막대 그래프 함수
def barchart(df):
    colName = 'ROI 1 []' # 열 지정
    
    df['Axis [nm]'] = df['Axis [nm]'].replace('[\$,]', '', regex=True).astype(float)
    x = df['Axis [nm]']
    
    df[colName] = df[colName].replace('[\$,]', '', regex=True).astype(float)
    y = df[colName]
    
    #fig = plt.figure()
    fig = plt.figure(figsize=(5,4))
    plt.bar(x,y)
    plt.xlabel(df.columns[1])
    plt.ylabel(df.columns[0])
    plt.axis([860,975,0,55])
    plt.title(colName+" "+"Bar Graph")

    # 화면에 막대 그래프 출력
    canvas = FigureCanvasTkAgg(fig,master=root) 
    canvas.get_tk_widget().pack(side='left', padx=10)

root = tk.Tk()
root.title("Tkinter Data&Graph")


# 파일 불러오기 버튼
button = tk.Button(root, text="파일 불러오기", command=open_file)
button.pack()

scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)

text = tk.Text(root)
text = Text(root, yscrollcommand=scrollbar.set)
text.pack()

root.mainloop()

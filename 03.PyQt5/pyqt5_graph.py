# CSV 파일 불러오면,
# 1. 데이터 출력
# 2. 모든 열 직선 그래프 출력
# 3. 모든 열 산점도 그래프 출력
# 4. 열 1개의 막대 그래프 출력
# 5. 열 1개의 파이 차트 출력
# 6. 열 이름 검색 -> 해당 열 데이터 및 직선 그래프 출력

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QLabel, QVBoxLayout, QWidget, QFileDialog, QLineEdit, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt5 - GUI 구현")
        self.setGeometry(200, 200, 800, 600)  # 윈도우 크기 조정

        # 버튼 및 텍스트 에디터 생성
        self.button = QPushButton("첨부하기", self)
        self.button.clicked.connect(self.load_file)
        self.text_edit = QTextEdit(self)
        self.label = QLabel(self)
        self.label1 = QLabel(self)
        self.label2 = QLabel(self)
        self.label3 = QLabel(self)

        # 레이아웃 설정
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.text_edit)

        # 입력 상자를 추가하는 레이아웃
        input_layout = QHBoxLayout()
        self.column_input = QLineEdit(self)
        self.column_input.returnPressed.connect(self.display_column)
        input_layout.addWidget(self.column_input)
        layout.addLayout(input_layout)

        # 이미지를 감싸는 레이아웃 추가
        image_layout = QHBoxLayout()
        image_layout.addWidget(self.label)
        image_layout.addWidget(self.label1)
        image_layout.addWidget(self.label2)
        image_layout.addWidget(self.label3)
        layout.addLayout(image_layout)

        # 추가한 레이아웃을 메인 윈도우에 설정
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


    # 파일 불러오면, 데이터 및 그래프 출력
    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "파일 선택", "", "CSV 파일 (*.csv)")

        if file_path:
            # CSV 파일 불러오기
            try:
                self.df = pd.read_csv(file_path)
                self.df1 = pd.read_csv(file_path)
                # CSV 파일 내용 출력
                self.text_edit.setPlainText(self.df.to_string())

                # 직선 그래프
                self.linegraph(self.df) 
                image_path = "graph_image.png" # 그래프를 이미지 파일로 저장
                plt.savefig(image_path)
                self.set_image(image_path,0) # 이미지 출력

                # 산점도 그래프
                self.scatter(self.df)
                image_path = "graph_image.png"
                plt.savefig(image_path)
                self.set_image(image_path,1)
                
                # 막대 그래프
                self.barchart(self.df) 
                image_path = "graph_image2.png"
                plt.savefig(image_path)
                self.set_image(image_path,2)
                
                # 파이 차트
                self.piechart(self.df1)
                image_path = "graph_image.png"
                plt.savefig(image_path)
                self.set_image(image_path,3)
                
            except pd.errors.ParserError:
                self.text_edit.setPlainText("잘못된 파일 형식입니다.")
    
    # 모든 열 직선 그래프
    def linegraph(self, df):
        cols = len(df.columns) - 1

        df['Axis [nm]'] = df['Axis [nm]'].replace('[\$,]', '', regex=True).astype(float)
        x = df['Axis [nm]']
        
        plt.figure()
        for i in range(1, cols+1):
            colName = f'ROI {i} []'
            df[colName] = df[colName].replace('[\$,]', '', regex=True).astype(float)
            y = df[colName]
             
            plt.plot(x, y, label=colName)
            # plt.tight_layout()
            # 범례 추가
            plt.legend(loc='lower left', bbox_to_anchor=(1.0,0.0), frameon=True)
        
        # 그래프 제목 설정
        plt.title('Line Graph')

        # x축, y축 레이블 설정
        plt.xlabel('Axis [nm]')
        plt.ylabel('Intensity')
        plt.tight_layout()

    # 산점도 그래프
    def scatter(self, df):
        cols = len(df.columns) - 1
        
        df['Axis [nm]'] = df['Axis [nm]'].replace('[\$,]', '', regex=True).astype(float)
        x = df['Axis [nm]']
    
        plt.figure()
        
        for i in range(1, cols+1):
            colName = f'ROI {i} []'
            df[colName] = df[colName].replace('[\$,]', '', regex=True).astype(float)
            y = df[colName]
            
            plt.scatter(x, y, label=colName)
            
            # 범례 추가
            plt.legend(loc='lower left', bbox_to_anchor=(1.0,0.0), frameon=True)

        # 그래프 제목 설정
        plt.title('Scatter Graph')

        # x축, y축 레이블 설정
        plt.xlabel('Axis [nm]')
        plt.ylabel('Intensity')
        plt.tight_layout()
        
    # 막대 차트
    def barchart(self, df):
        colName = 'ROI 1 []' # 열 지정
        
        df['Axis [nm]'] = df['Axis [nm]'].replace('[\$,]', '', regex=True).astype(float)
        x = df['Axis [nm]']
        
        df[colName] = df[colName].replace('[\$,]', '', regex=True).astype(float)
        y = df[colName]
        
        plt.figure()
        plt.bar(x, y)
        plt.xlabel(df.columns[1])
        plt.ylabel(df.columns[0])
        plt.axis([860, 975, 0, 55])
        plt.title(colName +" Bar Graph")
    
    # 원 그래프
    def piechart(self,df):
        colName = 'ROI 1 []'
        df[colName] = df[colName].replace('[\$,]', '', regex=True).astype(int)
        df[colName] = round(df[colName].div(10,1))
        
        data = []

        for i in range(1,6):
            data.append(len(df.loc[df[colName] == i])/len(df[colName]))
        
        plt.figure()
        y = pd.DataFrame(data)
        y.plot.pie(subplots=True,labels=['10-19','20-29','30-39','40-49','50-59'],autopct='%.1f')
        plt.legend(loc='lower left', bbox_to_anchor=(1.0,0.0),frameon=True)
        plt.title(colName+" Pie Chart")
    
    # 검색 열 직선 그래프
    def oneGraph(self,column_name):
        self.df['Axis [nm]'] = self.df['Axis [nm]'].replace('[\$,]', '', regex=True).astype(float)
        x = self.df['Axis [nm]']

        self.df[column_name] = self.df[column_name].replace('[\$,]', '', regex=True).astype(float)
        y = self.df[column_name]
         
        plt.figure()
        plt.plot(x,y)
        plt.axis([860,975,0,55])
        plt.title(column_name+" Line Graph")
        plt.xlabel('Axis [nm]')
        plt.ylabel('Intensity')

    def set_text(self, text):
        self.text_edit.setPlainText(text)

    def set_image(self, image_path, num_label):
        pixmap = QPixmap(image_path)
        
        if num_label == 0: 
            self.label.setPixmap(pixmap.scaledToWidth(600))  
        elif num_label == 1:
            self.label1.setPixmap(pixmap.scaledToWidth(600))  
        elif num_label == 2:
            self.label2.setPixmap(pixmap.scaledToWidth(600)) 
        elif num_label == 3:
            self.label3.setPixmap(pixmap.scaledToWidth(600))  

    # 열 이름 검색 - 직선 그래프 출력
    def display_column(self):
        column_name = self.column_input.text()
        if column_name in self.df.columns:
            column = self.df[column_name]

            # 데이터 출력
            self.text_edit.setPlainText(column.to_string())

            # 그래프 출력
            self.oneGraph(column_name)
            image_path = "graph_image.png"
            plt.savefig(image_path)
            self.set_image(image_path,0)
            
        else:
            self.text_edit.setPlainText("Invalid column name.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

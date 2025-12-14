import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QWidget, QMessageBox, QMenu
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

class RandomCaller(QMainWindow):
    def __init__(self):
        super().__init__()
        # 先初始化数据属性
        self.students = ["001","002","003","004","005","006"]
        self.running = False
        self.current_student = ""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_caller)
        # 然后设置UI
        self.init_ui()
    
    def init_ui(self):
        # 设置窗口标志 - 移除关闭和最大化按钮，保持置顶
        flags = Qt.Window | Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        
        # 设置窗口标题和大小
        self.setWindowTitle("普通点名器")
        self.setGeometry(300, 300, 400, 300)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # 标题标签
        title_label = QLabel("随机点名器")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # 点名显示标签
        self.call_label = QLabel("准备开始")
        self.call_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.call_label.setAlignment(Qt.AlignCenter)
        self.call_label.setStyleSheet("color: blue;")
        main_layout.addWidget(self.call_label)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        # 开始/停止按钮
        self.start_button = QPushButton("开始点名")
        self.start_button.setFont(QFont("Arial", 16, QFont.Bold))
        self.start_button.setMinimumWidth(200)
        self.start_button.setMinimumHeight(50)
        self.start_button.clicked.connect(self.toggle_calling)
        button_layout.addWidget(self.start_button)
        
        main_layout.addLayout(button_layout)
        
        # 学生数量标签
        self.count_label = QLabel(f"当前学生数量: {len(self.students)}")
        self.count_label.setFont(QFont("Arial", 10))
        self.count_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.count_label)
    
    def toggle_calling(self):
        if self.running:
            # 停止点名
            self.running = False
            self.timer.stop()
            self.start_button.setText("开始点名")
            QMessageBox.information(self, "点名结果", f"本次点名: {self.current_student}")
        else:
            # 开始点名
            self.running = True
            self.start_button.setText("停止点名")
            # 启动定时器，每100毫秒更新一次
            self.timer.start(100)
    
    def update_caller(self):
        # 随机选择学生并更新显示
        self.current_student = random.choice(self.students)
        self.call_label.setText(self.current_student)
    
    def keyPressEvent(self, event):
        # 添加键盘事件处理
        if event.key() == Qt.Key_Escape:
            # Escape键关闭窗口
            self.close()
        else:
            # 其他按键继续传递给父类
            super().keyPressEvent(event)
    
    def contextMenuEvent(self, event):
        # 添加右键菜单
        context_menu = QMenu(self)
        quit_action = context_menu.addAction("退出")
        action = context_menu.exec_(self.mapToGlobal(event.pos()))
        if action == quit_action:
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    caller = RandomCaller()
    caller.show()
    # 确保窗口始终置顶
    caller.raise_()
    caller.activateWindow()
    sys.exit(app.exec_())

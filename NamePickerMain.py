import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QWidget, QMessageBox, QMenuBar, QMenu, QAction,
    QListWidget, QListWidgetItem, QAbstractItemView, QInputDialog
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

class RandomCaller(QMainWindow):
    def __init__(self):
        super().__init__()
        # 先初始化数据属性
        self.students = ["张三","王二","李四"]
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
        self.setWindowTitle("墨屿点抽")
        self.setGeometry(300, 300, 400, 300)
        
        # 创建菜单栏
        menubar = self.menuBar()
        
        # 学生管理菜单
        student_menu = menubar.addMenu("学生管理")
        
        # 添加学生动作
        add_action = QAction("添加学生", self)
        add_action.triggered.connect(self.add_student)
        student_menu.addAction(add_action)
        
        # 删除学生动作
        delete_action = QAction("删除学生", self)
        delete_action.triggered.connect(self.delete_student)
        student_menu.addAction(delete_action)
        
        # 清空名单动作
        clear_action = QAction("清空名单", self)
        clear_action.triggered.connect(self.clear_students)
        student_menu.addAction(clear_action)
        
        # 查看名单动作
        view_action = QAction("查看名单", self)
        view_action.triggered.connect(self.view_students)
        student_menu.addAction(view_action)
        
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
    
    def add_student(self):
        # 添加学生
        name, ok = QInputDialog.getText(self, "添加学生", "请输入学生姓名:")
        if ok and name.strip():
            name = name.strip()
            if name not in self.students:
                self.students.append(name)
                self.count_label.setText(f"当前学生数量: {len(self.students)}")
                QMessageBox.information(self, "成功", f"已添加学生: {name}")
            else:
                QMessageBox.warning(self, "警告", f"学生 {name} 已存在!")
    
    def delete_student(self):
        # 删除学生
        name, ok = QInputDialog.getText(self, "删除学生", "请输入要删除的学生姓名:")
        if ok and name.strip():
            name = name.strip()
            if name in self.students:
                reply = QMessageBox.question(
                    self, "确认", f"确定要删除学生 {name} 吗?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    self.students.remove(name)
                    self.count_label.setText(f"当前学生数量: {len(self.students)}")
                    QMessageBox.information(self, "成功", f"已删除学生: {name}")
            else:
                QMessageBox.warning(self, "警告", f"学生 {name} 不存在!")
    
    def clear_students(self):
        # 清空学生名单
        if len(self.students) == 0:
            QMessageBox.warning(self, "警告", "学生名单已经是空的!")
            return
        
        reply = QMessageBox.question(
            self, "确认", "确定要清空所有学生吗?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.students.clear()
            self.count_label.setText(f"当前学生数量: {len(self.students)}")
            QMessageBox.information(self, "成功", "已清空所有学生")
    
    def view_students(self):
        # 查看学生名单
        if len(self.students) == 0:
            QMessageBox.information(self, "学生名单", "当前没有学生")
            return
        
        student_list = "\n".join(self.students)
        QMessageBox.information(self, "学生名单", f"当前学生名单:\n\n{student_list}")
    
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

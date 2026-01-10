import sys
import random
import os
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QWidget, QMessageBox, QMenuBar, QMenu, QAction,
    QListWidget, QListWidgetItem, QAbstractItemView, QInputDialog
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QIcon

class RandomCaller(QMainWindow):
    """随机点名系统主窗口类"""
    
    def __init__(self):
        """初始化类实例"""
        super().__init__()
        # 初始化数据属性
        self.students = self.load_students()  # 学生名单
        self.running = False  # 点名运行状态
        self.current_student = ""  # 当前选中的学生
        self.timer = QTimer(self)  # 用于随机选择的定时器
        self.timer.timeout.connect(self.update_caller)  # 定时器触发事件
        
        # 初始化UI界面
        self.init_ui()
    
    def load_students(self):
        # 从JSON文件加载学生名单
        try:
            file_path = os.path.join(os.path.dirname(__file__), "students.json")
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            QMessageBox.warning(self, "警告", f"加载学生名单失败，将使用默认名单: {str(e)}")
        # 默认学生名单
        return ["我","老子","老几","老自","吾","朕"]
    
    def init_ui(self):
        # 设置窗口标志 - 移除关闭和最大化按钮，保持置顶
        flags = Qt.Window | Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        
        # 设置窗口标题和大小
        self.setWindowTitle("Moyu Select")
        self.setGeometry(300, 300, 450, 350)
        
        # 设置应用图标
        self.set_app_icon()
        
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
        
        # 设置主窗口样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QWidget {
                background-color: #f5f5f5;
                font-family: "Microsoft YaHei", Arial;
            }
            
            /* QMessageBox样式 */
            QMessageBox {
                background-color: #f5f5f5;
                border-radius: 15px;
                font-family: "Microsoft YaHei", Arial;
            }
            
            QMessageBox QLabel {
                color: #2c3e50;
                font-size: 14px;
                padding: 10px;
            }
            
            QMessageBox QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 8px 20px;
                font-size: 14px;
                min-width: 80px;
            }
            
            QMessageBox QPushButton:hover {
                background-color: #2980b9;
            }
            
            QMessageBox QPushButton:pressed {
                background-color: #1a5276;
            }
            
            /* 确认对话框的Yes按钮可以使用不同颜色 */
            QMessageBox QPushButton#qt_msgbox_yes {
                background-color: #27ae60;
            }
            
            QMessageBox QPushButton#qt_msgbox_yes:hover {
                background-color: #229954;
            }
            
            QMessageBox QPushButton#qt_msgbox_yes:pressed {
                background-color: #1e8449;
            }
            
            /* 取消按钮使用中性颜色 */
            QMessageBox QPushButton#qt_msgbox_no {
                background-color: #95a5a6;
            }
            
            QMessageBox QPushButton#qt_msgbox_no:hover {
                background-color: #7f8c8d;
            }
            
            QMessageBox QPushButton#qt_msgbox_no:pressed {
                background-color: #6c7a89;
            }
        """)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(25)
        main_layout.setContentsMargins(40, 40, 40, 40)
        
        # 标题标签
        title_label = QLabel("Moyu Select")
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                padding: 10px;
                border: none;
            }
        """)
        main_layout.addWidget(title_label)
        
        # 点名显示标签
        self.call_label = QLabel("准备开始")
        self.call_label.setFont(QFont("Arial", 32, QFont.Bold))
        self.call_label.setAlignment(Qt.AlignCenter)
        self.call_label.setMinimumHeight(100)
        self.call_label.setStyleSheet("""
            QLabel {
                color: #3498db;
                background-color: white;
                border-radius: 15px;
                padding: 20px;
                border: 2px solid #e0e0e0;
            }
        """)
        main_layout.addWidget(self.call_label)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        
        # 开始/停止按钮
        self.start_button = QPushButton("开始点名")
        self.start_button.setFont(QFont("Arial", 16, QFont.Bold))
        self.start_button.setMinimumWidth(200)
        self.start_button.setMinimumHeight(60)
        self.start_button.setCursor(Qt.PointingHandCursor)
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 25px;
                padding: 15px 30px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1a5276;
            }
        """)
        self.start_button.clicked.connect(self.toggle_calling)
        button_layout.addWidget(self.start_button)
        
        main_layout.addLayout(button_layout)
        
        # 学生数量标签
        self.count_label = QLabel(f"当前学生数量: {len(self.students)}")
        self.count_label.setFont(QFont("Arial", 11))
        self.count_label.setAlignment(Qt.AlignCenter)
        self.count_label.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                padding: 5px;
                border: none;
            }
        """)
        main_layout.addWidget(self.count_label)
    
    def set_app_icon(self):
        # 设置应用图标
        icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            QApplication.setWindowIcon(QIcon(icon_path))
    
    def toggle_calling(self):
        if self.running:
            # 停止点名
            self.running = False
            self.timer.stop()
            self.start_button.setText("开始点名")
            QMessageBox.information(self, "Moyu Select", f"本次点名: {self.current_student}")
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
                self.save_students()
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
                    self.save_students()
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
            self.save_students()
    
    def view_students(self):
        # 查看学生名单
        if len(self.students) == 0:
            QMessageBox.information(self, "学生名单", "当前没有学生")
            return
        
        student_list = "\n".join(self.students)
        QMessageBox.information(self, "学生名单", f"当前学生名单:\n\n{student_list}")
    
    def save_students(self):
        # 将学生名单保存到JSON文件
        try:
            file_path = os.path.join(os.path.dirname(__file__), "students.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.students, f, ensure_ascii=False, indent=2)
        except Exception as e:
            QMessageBox.warning(self, "警告", f"保存学生名单失败: {str(e)}")
    
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

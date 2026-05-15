import sys
import os
import subprocess
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                             QHBoxLayout, QWidget, QFileDialog, QTextEdit, QLabel, 
                             QSpacerItem, QSizePolicy)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices

class YSMGui(QMainWindow):
    def __init__(self):
        super().__init__()
        # 设置窗口基本信息
        self.setWindowTitle("YSMParser-Pro")
        self.resize(800, 550)
        
        # --- GitHub 极客深色风格样式表 ---
        self.setStyleSheet("""
            QMainWindow { background-color: #0d1117; }
            QLabel { color: #c9d1d9; font-family: 'Segoe UI', sans-serif; }
            QTextEdit { 
                background-color: #161b22; 
                color: #7ee787; 
                border: 1px solid #30363d; 
                border-radius: 6px; 
                font-family: 'Consolas', monospace; 
                font-size: 13px;
                padding: 10px;
            }
            QPushButton#mainBtn {
                background-color: #238636;
                color: white;
                border-radius: 6px;
                font-weight: bold;
                font-size: 15px;
                min-height: 45px;
                border: 1px solid rgba(255,255,255,0.1);
            }
            QPushButton#mainBtn:hover { background-color: #2ea043; }
            QPushButton#githubBtn {
                background-color: transparent;
                color: #58a6ff;
                border: none;
                font-size: 13px;
                text-decoration: underline;
            }
            QPushButton#githubBtn:hover { color: #79c0ff; }
        """)

        # 主布局容器
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(30, 30, 30, 20)
        layout.setSpacing(15)

        # 头部区域
        header = QLabel("YSMParser Pro")
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: #ffffff;")
        layout.addWidget(header)

        desc = QLabel("现代化 YSM OpenGUI | 基于 OpenYSM 核心")
        desc.setStyleSheet("color: #8b949e; margin-bottom: 10px;")
        layout.addWidget(desc)

        # 核心功能按钮
        self.btn = QPushButton("📂 选择文件夹并批量解析模型")
        self.btn.setObjectName("mainBtn")
        self.btn.setCursor(Qt.PointingHandCursor)
        self.btn.clicked.connect(self.start_parse)
        layout.addWidget(self.btn)

        # 日志显示区域
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setPlaceholderText("日志将在此处实时显示...")
        layout.addWidget(self.log_area)

        # --- 底部工具栏 ---
        bottom_bar = QHBoxLayout()
        
        # 左下角：直通你的 GitHub 仓库按钮
        self.github_btn = QPushButton("⭐ View on GitHub")
        self.github_btn.setObjectName("githubBtn")
        self.github_btn.setCursor(Qt.PointingHandCursor)
        self.github_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/Phoebemc-sb/YSMParser-Pro")))
        
        bottom_bar.addWidget(self.github_btn)
        
        # 弹簧空间，将版本号推向右侧
        bottom_bar.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        # 右下角：版本标识
        version_tag = QLabel("Stable v1.0")
        version_tag.setStyleSheet("color: #484f58;")
        bottom_bar.addWidget(version_tag)
        
        layout.addLayout(bottom_bar)

    def start_parse(self):
        # 调取文件夹选择器（解决 V3 --input 要求文件夹的问题）
        dir_path = QFileDialog.getExistingDirectory(self, "选择包含 .ysm 文件的目录")
        
        if dir_path:
            # 规范化路径，适配 Windows 反斜杠
            dir_path = os.path.normpath(dir_path)
            self.log_area.clear()
            self.log_area.append(f"<b>[ 任务启动 ]</b> 扫描目录: {dir_path}\n")
            
            try:
                # 自动在当前程序下创建 output 文件夹
                output_dir = os.path.join(os.getcwd(), "output")
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                # 调用核心二进制文件
                command = ["YSMParser.exe", "--input", dir_path, "--output", output_dir]
                
                # 执行进程并捕获输出
                result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
                
                if result.stdout:
                    self.log_area.append(result.stdout)
                if result.stderr:
                    self.log_area.append(f"<span style='color:#d29922;'>[ 提示/错误 ]</span>\n{result.stderr}")
                
                self.log_area.append(f"\n<b>[ 处理完成 ]</b> 结果已保存至: {output_dir}")
                
            except Exception as e:
                self.log_area.append(f"<b style='color:#f85149;'>[ 运行失败 ]</b> 找不到 YSMParser.exe 或执行出错: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YSMGui()
    window.show()
    sys.exit(app.exec())
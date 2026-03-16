#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
三角洲游戏助手 - 小麻虾电竞出品
开源、绿色、无毒、免登录
Windows端专属
低内存占用
"""

import sys
import os
import json
import ctypes
import subprocess
import threading
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QPushButton, QColorDialog, QSlider, QCheckBox,
    QGroupBox, QTextEdit, QLineEdit, QComboBox, QMessageBox, QSplitter,
    QScrollArea, QFrame, QProgressBar, QDialog
)
from PyQt6.QtCore import Qt, QPoint, QTimer, QRect, QThread, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QPen, QFont, QBrush, QPainterPath
import keyboard

CONFIG_FILE = "config.json"
SKILLS_FILE = "skills.json"
DEFAULT_CONFIG = {
    "crosshair": {
        "enabled": False,
        "color": "#FF0000",
        "size": 20,
        "glow_enabled": True,
        "glow_color": "#FF0000",
        "glow_radius": 8
    },
    "upload_block": {
        "enabled": False,
        "shortcut": "F10",
        "notification_pos": "top_left"
    },
    "ai_chat": {
        "enabled": False,
        "chroma_installed": False,
        "db_initialized": False
    },
    "hotkeys": {
        "crosshair": "F9"
    }
}
DEFAULT_SKILLS = {
    "warfare": [
        {
            "name": "跑刀流配装",
            "description": "轻量化快速获取物资，低风险高收益",
            "content": "武器：手枪（修脚枪）+ 近战武器\n头盔：无需头盔\n护甲：无护甲\n背包：小型背包\n打法：快速搜刮，遇敌修脚，灵活撤离"
        },
        {
            "name": "以小搏大流派",
            "description": "修脚枪专属配装与打法攻略",
            "content": "武器：修脚枪（推荐MP7/P90）\n弹药：达姆弹/空尖弹\n头盔：二级头\n护甲：一级甲\n背包：中型背包\n打法：修脚攻击敌人腿部，快速制敌"
        }
    ],
    "extraction": [
        {
            "name": "露娜炸撤离点点位",
            "description": "露娜角色专属炸撤离点点位",
            "content": "点位1：西北区域A点\n  - 投掷角度：45度\n  - 距离：15米\n  - 技巧：等待敌人聚集时引爆\n点位2：东南区域B点\n  - 投掷角度：30度\n  - 距离：20米"
        },
        {
            "name": "红狼炸撤离点点位",
            "description": "红狼角色专属炸撤离点点位",
            "content": "点位1：中央区域C点\n  - 投掷角度：60度\n  - 距离：12米\n  - 技巧：利用地形掩护\n点位2：东北区域D点\n  - 投掷角度：40度\n  - 距离：18米"
        },
        {
            "name": "乌鲁鲁炸撤离点点位",
            "description": "乌鲁鲁角色专属炸撤离点点位",
            "content": "点位1：西南区域E点\n  - 投掷角度：50度\n  - 距离：16米\n  - 技巧：隐蔽投掷\n点位2：东北区域F点\n  - 投掷角度：35度\n  - 距离：22米"
        }
    ]
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                for key, value in DEFAULT_CONFIG.items():
                    if key not in config:
                        config[key] = value
                    elif isinstance(value, dict):
                        for sub_key, sub_value in value.items():
                            if sub_key not in config[key]:
                                config[key][sub_key] = sub_value
                return config
        except:
            pass
    return DEFAULT_CONFIG.copy()

def save_config(config):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

def load_skills():
    if os.path.exists(SKILLS_FILE):
        try:
            with open(SKILLS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return DEFAULT_SKILLS.copy()

def save_skills(skills):
    with open(SKILLS_FILE, 'w', encoding='utf-8') as f:
        json.dump(skills, f, ensure_ascii=False, indent=4)

class CrosshairWindow(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.init_ui()
        
    def init_ui(self):
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.update_position()
        
    def update_position(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        center_x = screen_geometry.center().x()
        center_y = screen_geometry.center().y()
        size = self.config['crosshair']['size'] + 40
        self.setGeometry(center_x - size//2, center_y - size//2, size, size)
        
    def paintEvent(self, event):
        if not self.config['crosshair']['enabled']:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        center = self.rect().center()
        color = QColor(self.config['crosshair']['color'])
        size = self.config['crosshair']['size']
        if self.config['crosshair']['glow_enabled']:
            glow_color = QColor(self.config['crosshair']['glow_color'])
            glow_radius = self.config['crosshair']['glow_radius']
            for i in range(glow_radius, 0, -2):
                alpha = int(255 * (1 - i / glow_radius))
                glow_color.setAlpha(alpha)
                pen = QPen(glow_color, i)
                pen.setCapStyle(Qt.PenCapStyle.RoundCap)
                painter.setPen(pen)
                painter.drawLine(int(center.x() - size//2), int(center.y()), int(center.x() + size//2), int(center.y()))
                painter.drawLine(int(center.x()), int(center.y() - size//2), int(center.x()), int(center.y() + size//2))
        pen = QPen(color, 2)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.drawLine(int(center.x() - size//2), int(center.y()), int(center.x() + size//2), int(center.y()))
        painter.drawLine(int(center.x()), int(center.y() - size//2), int(center.x()), int(center.y() + size//2))
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center, 3, 3)

class NotificationWindow(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.message = ""
        self.init_ui()
        self.hide_timer = QTimer()
        self.hide_timer.timeout.connect(self.hide)
        
    def init_ui(self):
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setFixedSize(300, 80)
        
    def show_message(self, message):
        self.message = message
        self.update_position()
        self.show()
        self.update()
        self.hide_timer.start(3000)
        
    def update_position(self):
        screen = QApplication.primaryScreen()
        screen_geo = screen.availableGeometry()
        pos = self.config['upload_block']['notification_pos']
        if pos == 'top_left':
            self.move(20, 20)
        elif pos == 'top_right':
            self.move(screen_geo.width() - 320, 20)
        elif pos == 'bottom':
            self.move(screen_geo.width() // 2 - 150, screen_geo.height() - 100)
            
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect().adjusted(2, 2, -2, -2)
        path = QPainterPath()
        path.addRoundedRect(rect, 10, 10)
        painter.fillPath(path, QColor(0, 0, 0, 200))
        painter.setPen(QColor(255, 255, 255))
        font = QFont('Microsoft YaHei', 14, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.message)

class DependencyInstaller(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool)
    
    def run(self):
        try:
            packages = ["chromadb", "sentence-transformers"]
            for i, package in enumerate(packages):
                self.progress.emit(f"正在安装: {package} ({i+1}/{len(packages)})")
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", package
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.progress.emit("依赖安装完成!")
            self.finished.emit(True)
        except Exception as e:
            self.progress.emit(f"安装失败: {str(e)}")
            self.finished.emit(False)

class AIChatModule:
    def __init__(self, db_path: str = "./chroma_db"):
        self.db_path = db_path
        self.client = None
        self.collection = None
        self.ef = None
        self.initialized = False
        self.has_chroma = self._check_chroma()
        
    def _check_chroma(self):
        try:
            import chromadb
            from chromadb.utils import embedding_functions
            return True
        except ImportError:
            return False
            
    def is_available(self):
        return self.has_chroma
        
    def initialize(self):
        if not self.has_chroma:
            return False
        try:
            import chromadb
            from chromadb.utils import embedding_functions
            self.client = chromadb.PersistentClient(path=self.db_path)
            self.ef = embedding_functions.DefaultEmbeddingFunction()
            self.collection = self.client.get_or_create_collection(
                name="delta_game_knowledge",
                embedding_function=self.ef
            )
            self.initialized = True
            return True
        except Exception as e:
            print(f"AI模块初始化失败: {e}")
            return False
            
    def add_documents(self, documents, ids=None):
        if not self.initialized:
            return False
        try:
            texts = [doc["content"] for doc in documents]
            metadatas = [{"title": doc.get("title", "")} for doc in documents]
            if ids is None:
                ids = [f"doc_{i}" for i in range(len(documents))]
            self.collection.add(
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            return True
        except Exception as e:
            print(f"添加文档失败: {e}")
            return False
            
    def query(self, question, n_results=3):
        if not self.initialized:
            return []
        try:
            results = self.collection.query(
                query_texts=[question],
                n_results=n_results
            )
            return [
                {
                    "content": doc,
                    "title": meta["title"],
                    "distance": dist
                }
                for doc, meta, dist in zip(
                    results["documents"][0],
                    results["metadatas"][0],
                    results["distances"][0]
                )
            ]
        except Exception as e:
            print(f"查询失败: {e}")
            return []
            
    def generate_answer(self, question, retrieved_docs):
        if not retrieved_docs:
            return "抱歉，没有找到相关资料，请尝试其他问题。"
        context = "\n\n".join([f"【{doc['title']}】\n{doc['content']}" for doc in retrieved_docs])
        answer = f"根据检索到的资料，为您解答：\n\n{context}\n\n以上信息仅供参考，请结合实际游戏情况判断。"
        return answer
        
    def chat(self, question):
        retrieved = self.query(question)
        return self.generate_answer(question, retrieved)
        
    def load_default_knowledge(self, skills_path="skills.json"):
        if not os.path.exists(skills_path):
            return False
        try:
            with open(skills_path, 'r', encoding='utf-8') as f:
                skills = json.load(f)
            docs = []
            for category in skills.values():
                for skill in category:
                    docs.append({
                        "title": skill["name"],
                        "content": f"{skill['description']}\n\n{skill['content']}"
                    })
            extra_docs = [
                {
                    "title": "游戏基本介绍",
                    "content": "三角洲游戏是一款战术射击游戏，玩家需要在地图中搜刮物资、击败敌人、安全撤离。"
                },
                {
                    "title": "修脚技巧",
                    "content": "修脚是指专门攻击敌人腿部的战术，可以快速击倒敌人而不直接击杀，适合以小搏大的战术。"
                }
            ]
            docs.extend(extra_docs)
            return self.add_documents(docs)
        except Exception as e:
            print(f"加载默认知识库失败: {e}")
            return False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = load_config()
        self.skills = load_skills()
        self.crosshair_window = None
        self.notification_window = None
        self.upload_blocked = False
        self.ai_module = None
        self.init_ui()
        self.init_hotkeys()
        self.create_crosshair()
        self.create_notification()
        if self.config['ai_chat']['enabled']:
            self.init_ai_module()
        
    def init_ui(self):
        self.setWindowTitle('三角洲游戏助手 - 小麻虾电竞')
        self.setGeometry(100, 100, 800, 600)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        self.create_crosshair_tab()
        self.create_skills_tab()
        self.create_block_upload_tab()
        self.create_chat_tab()
        self.create_settings_tab()
        main_layout.addWidget(self.create_promotion_bar())
        
    def create_promotion_bar(self):
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setStyleSheet('background-color: #2c3e50; color: white; border-radius: 5px;')
        layout = QHBoxLayout(frame)
        logo_label = QLabel('🦐')
        logo_label.setStyleSheet('font-size: 24px;')
        layout.addWidget(logo_label)
        text_label = QLabel('小麻虾电竞 - 专注游戏辅助')
        text_label.setStyleSheet('font-size: 14px; font-weight: bold;')
        layout.addWidget(text_label)
        layout.addStretch()
        qr_label = QLabel('📱 扫码关注小程序')
        qr_label.setStyleSheet('font-size: 12px;')
        layout.addWidget(qr_label)
        return frame
        
    def create_crosshair_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        enable_group = QGroupBox('准星开关')
        enable_layout = QVBoxLayout()
        self.crosshair_enable = QCheckBox('启用准星')
        self.crosshair_enable.setChecked(self.config['crosshair']['enabled'])
        self.crosshair_enable.stateChanged.connect(self.toggle_crosshair)
        enable_layout.addWidget(self.crosshair_enable)
        enable_group.setLayout(enable_layout)
        layout.addWidget(enable_group)
        color_group = QGroupBox('准星设置')
        color_layout = QVBoxLayout()
        color_btn_layout = QHBoxLayout()
        color_btn_layout.addWidget(QLabel('准星颜色:'))
        self.color_btn = QPushButton('选择颜色')
        self.color_btn.clicked.connect(self.choose_color)
        color_btn_layout.addWidget(self.color_btn)
        color_layout.addLayout(color_btn_layout)
        glow_btn_layout = QHBoxLayout()
        self.glow_enable = QCheckBox('启用外发光')
        self.glow_enable.setChecked(self.config['crosshair']['glow_enabled'])
        self.glow_enable.stateChanged.connect(self.update_crosshair_config)
        glow_btn_layout.addWidget(self.glow_enable)
        self.glow_color_btn = QPushButton('发光颜色')
        self.glow_color_btn.clicked.connect(self.choose_glow_color)
        glow_btn_layout.addWidget(self.glow_color_btn)
        color_layout.addLayout(glow_btn_layout)
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel('准星大小:'))
        self.size_slider = QSlider(Qt.Orientation.Horizontal)
        self.size_slider.setMinimum(10)
        self.size_slider.setMaximum(50)
        self.size_slider.setValue(self.config['crosshair']['size'])
        self.size_slider.valueChanged.connect(self.update_crosshair_config)
        size_layout.addWidget(self.size_slider)
        color_layout.addLayout(size_layout)
        glow_size_layout = QHBoxLayout()
        glow_size_layout.addWidget(QLabel('发光半径:'))
        self.glow_size_slider = QSlider(Qt.Orientation.Horizontal)
        self.glow_size_slider.setMinimum(2)
        self.glow_size_slider.setMaximum(20)
        self.glow_size_slider.setValue(self.config['crosshair']['glow_radius'])
        self.glow_size_slider.valueChanged.connect(self.update_crosshair_config)
        glow_size_layout.addWidget(self.glow_size_slider)
        color_layout.addLayout(glow_size_layout)
        color_group.setLayout(color_layout)
        layout.addWidget(color_group)
        layout.addStretch()
        self.tab_widget.addTab(tab, '🎯 准星设置')
        
    def create_skills_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        skills_tab = QTabWidget()
        warfare_widget = QWidget()
        warfare_layout = QVBoxLayout(warfare_widget)
        for skill in self.skills['warfare']:
            self.add_skill_card(warfare_layout, skill)
        warfare_layout.addStretch()
        skills_tab.addTab(warfare_widget, '⚔️ 战备配置')
        extraction_widget = QWidget()
        extraction_layout = QVBoxLayout(extraction_widget)
        for skill in self.skills['extraction']:
            self.add_skill_card(extraction_layout, skill)
        extraction_layout.addStretch()
        skills_tab.addTab(extraction_widget, '💥 撤离点攻坚')
        layout.addWidget(skills_tab)
        self.tab_widget.addTab(tab, '📚 AI Skill 技能库')
        
    def add_skill_card(self, parent_layout, skill):
        group = QGroupBox(skill['name'])
        group.setStyleSheet('QGroupBox { font-weight: bold; font-size: 14px; }')
        layout = QVBoxLayout()
        desc_label = QLabel(skill['description'])
        desc_label.setStyleSheet('color: #666; font-style: italic;')
        layout.addWidget(desc_label)
        content_text = QTextEdit()
        content_text.setPlainText(skill['content'])
        content_text.setReadOnly(True)
        content_text.setMaximumHeight(150)
        layout.addWidget(content_text)
        group.setLayout(layout)
        parent_layout.addWidget(group)
        
    def create_block_upload_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        status_group = QGroupBox('断上传状态')
        status_layout = QVBoxLayout()
        self.status_label = QLabel('当前状态: 正常上传')
        self.status_label.setStyleSheet('font-size: 16px; font-weight: bold; color: green;')
        status_layout.addWidget(self.status_label)
        self.block_btn = QPushButton('切换断上传')
        self.block_btn.clicked.connect(self.toggle_upload_block)
        status_layout.addWidget(self.block_btn)
        status_group.setLayout(status_layout)
        layout.addWidget(status_group)
        pos_group = QGroupBox('提示位置设置')
        pos_layout = QVBoxLayout()
        pos_combo_layout = QHBoxLayout()
        pos_combo_layout.addWidget(QLabel('提示位置:'))
        self.pos_combo = QComboBox()
        self.pos_combo.addItems(['左上角', '右上角', '屏幕底部'])
        pos_map = {'top_left': 0, 'top_right': 1, 'bottom': 2}
        self.pos_combo.setCurrentIndex(pos_map.get(self.config['upload_block']['notification_pos'], 0))
        self.pos_combo.currentIndexChanged.connect(self.update_notification_pos)
        pos_combo_layout.addWidget(self.pos_combo)
        pos_layout.addLayout(pos_combo_layout)
        pos_group.setLayout(pos_layout)
        layout.addWidget(pos_group)
        layout.addStretch()
        self.tab_widget.addTab(tab, '🔒 断上传设置')
        
    def create_chat_tab(self):
        self.chat_tab = QWidget()
        layout = QVBoxLayout(self.chat_tab)
        if not self.config['ai_chat']['enabled']:
            disabled_label = QLabel('AI问答模块未启用\n请在设置页面启用该功能')
            disabled_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            disabled_label.setStyleSheet('color: #999; font-size: 16px;')
            layout.addWidget(disabled_label)
        else:
            self.chat_display = QTextEdit()
            self.chat_display.setReadOnly(True)
            self.chat_display.setPlaceholderText('问答历史将显示在这里...')
            layout.addWidget(self.chat_display)
            input_layout = QHBoxLayout()
            self.chat_input = QLineEdit()
            self.chat_input.setPlaceholderText('输入您的问题...')
            self.chat_input.returnPressed.connect(self.send_chat_message)
            input_layout.addWidget(self.chat_input)
            self.send_btn = QPushButton('发送')
            self.send_btn.clicked.connect(self.send_chat_message)
            input_layout.addWidget(self.send_btn)
            layout.addLayout(input_layout)
        self.tab_widget.addTab(self.chat_tab, '🤖 AI问答')
        if not self.config['ai_chat']['enabled']:
            self.tab_widget.setTabEnabled(self.tab_widget.indexOf(self.chat_tab), False)
        
    def create_settings_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        hotkey_group = QGroupBox('快捷键设置')
        hotkey_layout = QVBoxLayout()
        crosshair_hotkey_layout = QHBoxLayout()
        crosshair_hotkey_layout.addWidget(QLabel('准星快捷键:'))
        self.crosshair_hotkey_label = QLabel(self.config['hotkeys']['crosshair'])
        self.crosshair_hotkey_label.setStyleSheet('font-weight: bold;')
        crosshair_hotkey_layout.addWidget(self.crosshair_hotkey_label)
        hotkey_layout.addLayout(crosshair_hotkey_layout)
        block_hotkey_layout = QHBoxLayout()
        block_hotkey_layout.addWidget(QLabel('断上传快捷键:'))
        self.block_hotkey_label = QLabel(self.config['upload_block']['shortcut'])
        self.block_hotkey_label.setStyleSheet('font-weight: bold;')
        block_hotkey_layout.addWidget(self.block_hotkey_label)
        hotkey_layout.addLayout(block_hotkey_layout)
        hotkey_group.setLayout(hotkey_layout)
        layout.addWidget(hotkey_group)
        ai_group = QGroupBox('AI问答模块（选配）')
        ai_layout = QVBoxLayout()
        self.ai_enable = QCheckBox('启用AI问答模块')
        self.ai_enable.setChecked(self.config['ai_chat']['enabled'])
        self.ai_enable.stateChanged.connect(self.toggle_ai_chat)
        ai_layout.addWidget(self.ai_enable)
        ai_info_label = QLabel('注意：启用后需要重启工具，首次使用将自动安装依赖\n依赖：chromadb、sentence-transformers等')
        ai_info_label.setStyleSheet('color: #666; font-size: 11px;')
        ai_info_label.setWordWrap(True)
        ai_layout.addWidget(ai_info_label)
        ai_group.setLayout(ai_layout)
        layout.addWidget(ai_group)
        layout.addStretch()
        self.tab_widget.addTab(tab, '⚙️ 设置')
        
    def init_hotkeys(self):
        try:
            keyboard.add_hotkey(self.config['hotkeys']['crosshair'], self.toggle_crosshair_hotkey)
            keyboard.add_hotkey(self.config['upload_block']['shortcut'], self.toggle_upload_block)
        except Exception as e:
            print(f'快捷键注册失败: {e}')
            
    def create_crosshair(self):
        self.crosshair_window = CrosshairWindow(self.config)
        if self.config['crosshair']['enabled']:
            self.crosshair_window.show()
            
    def create_notification(self):
        self.notification_window = NotificationWindow(self.config)
        
    def init_ai_module(self):
        self.ai_module = AIChatModule()
        if not self.ai_module.is_available():
            reply = QMessageBox.question(
                self, '依赖安装', 
                'AI问答模块需要安装依赖，是否现在安装？\n(需要联网)',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.show_install_dialog()
            else:
                self.config['ai_chat']['enabled'] = False
                save_config(self.config)
        else:
            if not self.config['ai_chat']['db_initialized']:
                if self.ai_module.initialize():
                    self.ai_module.load_default_knowledge()
                    self.config['ai_chat']['db_initialized'] = True
                    save_config(self.config)
                    
    def show_install_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('安装依赖')
        dialog.setFixedSize(400, 150)
        layout = QVBoxLayout(dialog)
        self.progress_label = QLabel('准备安装...')
        layout.addWidget(self.progress_label)
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        layout.addWidget(self.progress_bar)
        dialog.show()
        self.installer = DependencyInstaller()
        self.installer.progress.connect(lambda msg: self.progress_label.setText(msg))
        self.installer.finished.connect(lambda success: self.on_install_finished(success, dialog))
        self.installer.start()
        
    def on_install_finished(self, success, dialog):
        dialog.close()
        if success:
            self.config['ai_chat']['chroma_installed'] = True
            save_config(self.config)
            QMessageBox.information(self, '成功', '依赖安装成功，请重启工具！')
        else:
            QMessageBox.warning(self, '失败', '依赖安装失败，请手动运行: pip install chromadb sentence-transformers')
            
    def send_chat_message(self):
        if not self.ai_module or not self.ai_module.initialized:
            QMessageBox.warning(self, '提示', 'AI模块未初始化')
            return
        question = self.chat_input.text().strip()
        if not question:
            return
        self.chat_display.append(f"👤 你: {question}")
        self.chat_input.clear()
        QApplication.processEvents()
        answer = self.ai_module.chat(question)
        self.chat_display.append(f"🤖 AI: {answer}")
        self.chat_display.append("---")
        
    def toggle_crosshair(self, state):
        enabled = state == Qt.CheckState.Checked.value
        self.config['crosshair']['enabled'] = enabled
        save_config(self.config)
        if enabled:
            self.crosshair_window.show()
        else:
            self.crosshair_window.hide()
        self.crosshair_window.update()
        
    def toggle_crosshair_hotkey(self):
        new_state = not self.config['crosshair']['enabled']
        self.crosshair_enable.setChecked(new_state)
        self.toggle_crosshair(Qt.CheckState.Checked.value if new_state else Qt.CheckState.Unchecked.value)
        
    def choose_color(self):
        color = QColorDialog.getColor(QColor(self.config['crosshair']['color']))
        if color.isValid():
            self.config['crosshair']['color'] = color.name()
            save_config(self.config)
            self.crosshair_window.update()
            
    def choose_glow_color(self):
        color = QColorDialog.getColor(QColor(self.config['crosshair']['glow_color']))
        if color.isValid():
            self.config['crosshair']['glow_color'] = color.name()
            save_config(self.config)
            self.crosshair_window.update()
            
    def update_crosshair_config(self):
        self.config['crosshair']['size'] = self.size_slider.value()
        self.config['crosshair']['glow_enabled'] = self.glow_enable.isChecked()
        self.config['crosshair']['glow_radius'] = self.glow_size_slider.value()
        save_config(self.config)
        self.crosshair_window.update_position()
        self.crosshair_window.update()
        
    def toggle_upload_block(self):
        self.upload_blocked = not self.upload_blocked
        if self.upload_blocked:
            self.status_label.setText('当前状态: 已断上传')
            self.status_label.setStyleSheet('font-size: 16px; font-weight: bold; color: red;')
            self.block_btn.setText('恢复上传')
            self.notification_window.show_message('⚠️ 已断上传')
            self.block_network_upload()
        else:
            self.status_label.setText('当前状态: 正常上传')
            self.status_label.setStyleSheet('font-size: 16px; font-weight: bold; color: green;')
            self.block_btn.setText('切换断上传')
            self.notification_window.show_message('✅ 恢复上传')
            self.unblock_network_upload()
            
    def block_network_upload(self):
        try:
            rule_name = 'DeltaHelper_BlockUpload'
            subprocess.run([
                'netsh', 'advfirewall', 'firewall', 'add', 'rule',
                f'name={rule_name}',
                'dir=out',
                'action=block',
                'protocol=any',
                'remoteip=any',
                'remoteport=any',
                'profile=any'
            ], shell=True, check=True, capture_output=True)
        except Exception as e:
            print(f'防火墙规则添加失败: {e}')
            
    def unblock_network_upload(self):
        try:
            rule_name = 'DeltaHelper_BlockUpload'
            subprocess.run([
                'netsh', 'advfirewall', 'firewall', 'delete', 'rule',
                f'name={rule_name}'
            ], shell=True, check=True, capture_output=True)
        except Exception as e:
            print(f'防火墙规则删除失败: {e}')
            
    def update_notification_pos(self, index):
        pos_map = {0: 'top_left', 1: 'top_right', 2: 'bottom'}
        self.config['upload_block']['notification_pos'] = pos_map[index]
        save_config(self.config)
        self.notification_window.update_position()
        
    def toggle_ai_chat(self, state):
        enabled = state == Qt.CheckState.Checked.value
        self.config['ai_chat']['enabled'] = enabled
        save_config(self.config)
        QMessageBox.information(self, '提示', '设置已保存，请重启工具使更改生效')
        
    def closeEvent(self, event):
        if self.crosshair_window:
            self.crosshair_window.close()
        if self.notification_window:
            self.notification_window.close()
        self.unblock_network_upload()
        event.accept()

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

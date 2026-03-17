#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主窗口模块
"""

import subprocess
import sys
import platform

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel, QPushButton,
    QColorDialog, QSlider, QCheckBox, QGroupBox, QTextEdit, QLineEdit,
    QComboBox, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

# 使用 PySide6 的 QShortcut 注册热键
KEYBOARD_AVAILABLE = True

from config import load_config, save_config, load_skills
from widgets import CrosshairWindow, NotificationWindow
from ui.tabs import create_promotion_bar, add_skill_card


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = load_config()
        self.skills = load_skills()
        self.crosshair_window = None
        self.notification_window = None
        self.upload_blocked = False
        self.init_ui()
        self.init_hotkeys()
        self.create_crosshair()
        self.create_notification()

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
        main_layout.addWidget(create_promotion_bar())

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
            add_skill_card(warfare_layout, skill)
        warfare_layout.addStretch()
        skills_tab.addTab(warfare_widget, '⚔️ 战备配置')
        extraction_widget = QWidget()
        extraction_layout = QVBoxLayout(extraction_widget)
        for skill in self.skills['extraction']:
            add_skill_card(extraction_layout, skill)
        extraction_layout.addStretch()
        skills_tab.addTab(extraction_widget, '💥 撤离点攻坚')
        layout.addWidget(skills_tab)
        self.tab_widget.addTab(tab, '📚 AI Skill 技能库')

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
            chat_display = QTextEdit()
            chat_display.setReadOnly(True)
            chat_display.setPlaceholderText('问答历史将显示在这里...')
            layout.addWidget(chat_display)
            input_layout = QHBoxLayout()
            chat_input = QLineEdit()
            chat_input.setPlaceholderText('输入您的问题...')
            input_layout.addWidget(chat_input)
            send_btn = QPushButton('发送')
            input_layout.addWidget(send_btn)
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
        if not KEYBOARD_AVAILABLE:
            print('快捷键功能仅在 Windows 上可用')
            return
        try:
            from PySide6.QtGui import QShortcut, QKeySequence
            
            # 注册 F9 热键
            crosshair_shortcut = QShortcut(QKeySequence('F9'), self)
            crosshair_shortcut.activated.connect(self.toggle_crosshair_hotkey)
            print('注册 F9 热键成功')
            
            # 注册 F10 热键
            block_shortcut = QShortcut(QKeySequence('F10'), self)
            block_shortcut.activated.connect(self.toggle_upload_block)
            print('注册 F10 热键成功')
            
            print('热键注册成功')
        except Exception as e:
            print(f'快捷键注册失败: {e}')

    def create_crosshair(self):
        self.crosshair_window = CrosshairWindow(self.config)
        if self.config['crosshair']['enabled']:
            self.crosshair_window.show()

    def create_notification(self):
        self.notification_window = NotificationWindow(self.config)

    def toggle_crosshair(self, state):
        print(f'toggle_crosshair 被调用，状态: {state}')
        enabled = state == Qt.CheckState.Checked.value
        print(f'准星状态: {enabled}')
        self.config['crosshair']['enabled'] = enabled
        print(f'保存配置')
        save_config(self.config)
        if enabled:
            print('显示准星窗口')
            self.crosshair_window.show()
        else:
            print('隐藏准星窗口')
            self.crosshair_window.hide()
        print('更新准星窗口')
        self.crosshair_window.update()

    def toggle_crosshair_hotkey(self):
        print('F9 热键被触发')
        # 使用 QTimer 确保在主线程中执行 UI 操作
        from PySide6.QtCore import QTimer
        QTimer.singleShot(0, self._toggle_crosshair_ui)

    def _toggle_crosshair_ui(self):
        print('_toggle_crosshair_ui 被调用')
        # 防止快速连续触发
        if hasattr(self, 'crosshair_blocking') and self.crosshair_blocking:
            print('crosshair_blocking 为 True，跳过')
            return
        print('crosshair_blocking 为 False，执行操作')
        self.crosshair_blocking = True
        
        new_state = not self.config['crosshair']['enabled']
        print(f'新状态: {new_state}')
        # 只需要设置复选框状态，它会自动触发 toggle_crosshair
        self.crosshair_enable.setChecked(new_state)
        
        # 重置阻塞标志 - 使用线程
        import threading
        import time
        def reset_blocking():
            time.sleep(0.5)
            self.crosshair_blocking = False
            print('重置 crosshair_blocking 标志')
        threading.Thread(target=reset_blocking, daemon=True).start()

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
        print('F10 热键被触发')
        # 使用 QTimer 确保在主线程中执行 UI 操作
        from PySide6.QtCore import QTimer
        QTimer.singleShot(0, self._toggle_upload_block_ui)

    def _toggle_upload_block_ui(self):
        print('_toggle_upload_block_ui 被调用')
        # 防止快速连续触发
        if hasattr(self, 'upload_blocking') and self.upload_blocking:
            print('upload_blocking 为 True，跳过')
            return
        print('upload_blocking 为 False，执行操作')
        self.upload_blocking = True
        
        self.upload_blocked = not self.upload_blocked
        print(f'新状态: {self.upload_blocked}')
        if self.upload_blocked:
            self.status_label.setText('当前状态: 已断上传')
            self.status_label.setStyleSheet('font-size: 16px; font-weight: bold; color: red;')
            self.block_btn.setText('恢复上传')
            self.notification_window.show_message('⚠️ 已断上传')
        else:
            self.status_label.setText('当前状态: 正常上传')
            self.status_label.setStyleSheet('font-size: 16px; font-weight: bold; color: green;')
            self.block_btn.setText('切换断上传')
            self.notification_window.show_message('✅ 恢复上传')
        
        # 异步执行网络操作
        import threading
        if self.upload_blocked:
            print('执行 block_network_upload')
            threading.Thread(target=self.block_network_upload, daemon=True).start()
        else:
            print('执行 unblock_network_upload')
            threading.Thread(target=self.unblock_network_upload, daemon=True).start()
        
        # 重置阻塞标志 - 使用线程
        import time
        def reset_blocking():
            time.sleep(1)
            self.upload_blocking = False
            print('重置 upload_blocking 标志')
        threading.Thread(target=reset_blocking, daemon=True).start()

    def block_network_upload(self):
        if platform.system() != 'Windows':
            print('断上传功能仅在 Windows 上可用')
            return
        try:
            rule_name = 'DeltaHelper_BlockUpload'
            # 先检查规则是否已经存在
            check_result = subprocess.run([
                'netsh', 'advfirewall', 'firewall', 'show', 'rule',
                f'name="{rule_name}"'
            ], shell=True, capture_output=True, text=True)
            
            if check_result.returncode == 0:
                print(f'防火墙规则 {rule_name} 已存在，跳过添加')
                return
            
            # 添加防火墙规则 - 移除 remoteport 参数，因为 protocol=any 时不能指定端口
            result = subprocess.run([
                'netsh', 'advfirewall', 'firewall', 'add', 'rule',
                f'name="{rule_name}"',
                'dir=out',
                'action=block',
                'protocol=any',
                'remoteip=any',
                'profile=any'
            ], shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f'防火墙规则 {rule_name} 添加成功')
            else:
                # 优先使用标准输出中的错误信息
                error_msg = result.stdout if result.stdout else result.stderr
                print(f'防火墙规则添加失败: {error_msg}')
                if '请求的操作需要提升' in error_msg or 'access is denied' in error_msg.lower():
                    print('提示：请以管理员权限运行程序以使用断上传功能')
        except Exception as e:
            print(f'防火墙规则添加失败: {e}')

    def unblock_network_upload(self):
        if platform.system() != 'Windows':
            return
        try:
            rule_name = 'DeltaHelper_BlockUpload'
            # 先检查规则是否存在
            check_result = subprocess.run([
                'netsh', 'advfirewall', 'firewall', 'show', 'rule',
                f'name="{rule_name}"'
            ], shell=True, capture_output=True, text=True)
            
            if check_result.returncode != 0:
                print(f'防火墙规则 {rule_name} 不存在，跳过删除')
                return
            
            # 删除防火墙规则
            result = subprocess.run([
                'netsh', 'advfirewall', 'firewall', 'delete', 'rule',
                f'name="{rule_name}"'
            ], shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f'防火墙规则 {rule_name} 删除成功')
            else:
                print(f'防火墙规则删除失败: {result.stderr}')
                if '请求的操作需要提升' in result.stderr or 'access is denied' in result.stderr.lower():
                    print('提示：请以管理员权限运行程序以使用断上传功能')
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

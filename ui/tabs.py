#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tab页模块
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel, QPushButton,
    QColorDialog, QSlider, QCheckBox, QGroupBox, QTextEdit, QLineEdit,
    QComboBox, QMessageBox, QFrame
)
from PySide6.QtCore import Qt


def create_promotion_bar():
    """创建推广栏"""
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


def add_skill_card(parent_layout, skill):
    """添加技能卡片"""
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

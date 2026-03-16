#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通知窗口模块
"""

from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QPainterPath


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
        path.addRoundedRect(rect.toRectF(), 10.0, 10.0)
        painter.fillPath(path, QColor(0, 0, 0, 200))
        painter.setPen(QColor(255, 255, 255))
        font = QFont('Microsoft YaHei', 14, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.message)

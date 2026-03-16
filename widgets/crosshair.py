#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
准星窗口模块
"""

from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QPainterPath


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

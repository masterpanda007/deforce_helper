#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
准星窗口模块
"""

import ctypes
from ctypes import wintypes
from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QPainterPath

# Windows API 常量
HWND_TOPMOST = -1
SWP_NOACTIVATE = 0x0010
SWP_NOMOVE = 0x0002
SWP_NOSIZE = 0x0001
SWP_SHOWWINDOW = 0x0040

# Windows API 函数
user32 = ctypes.windll.user32
user32.SetWindowPos.restype = wintypes.BOOL
user32.SetWindowPos.argtypes = [wintypes.HWND, wintypes.HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint]


class CrosshairWindow(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.init_ui()
        self.setup_force_topmost()

    def init_ui(self):
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowDoesNotAcceptFocus
        )
        self.update_position()

    def setup_force_topmost(self):
        """设置强制置顶机制"""
        try:
            # 初始更新位置
            self.update_position()
            
            # 初始强制置顶
            hwnd = int(self.winId())
            user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE | SWP_SHOWWINDOW)
            
            # 设置定时器，定期更新位置和强制置顶
            self.topmost_timer = QTimer(self)
            def update_and_topmost():
                self.update_position()
                self.force_topmost()
            self.topmost_timer.timeout.connect(update_and_topmost)
            self.topmost_timer.start(500)  # 每500毫秒更新一次
        except Exception as e:
            print(f'设置强制置顶失败: {e}')

    def force_topmost(self):
        """强制将窗口置顶"""
        try:
            hwnd = int(self.winId())
            user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE)
        except Exception as e:
            pass

    def update_position(self):
        """更新准星位置到屏幕中心"""
        screen = QApplication.primaryScreen()
        # 使用 geometry() 而不是 availableGeometry() 以获取完整屏幕尺寸
        screen_geometry = screen.geometry()
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

    def closeEvent(self, event):
        """窗口关闭时停止定时器"""
        if hasattr(self, 'topmost_timer'):
            self.topmost_timer.stop()
        super().closeEvent(event)

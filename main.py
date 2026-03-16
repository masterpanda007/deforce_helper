#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
三角洲游戏助手 - 小麻虾电竞出品
开源、绿色、无毒、免登录
Windows端专属
低内存占用
"""

import sys
from PySide6.QtWidgets import QApplication
from ui import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

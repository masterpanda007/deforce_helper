#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试热键功能
"""

import keyboard
import time

print('测试热键功能...')
print('按 F9 键测试')
print('按 Ctrl+C 退出')

def on_f9_press():
    print('F9 键被按下')

def on_f10_press():
    print('F10 键被按下')

try:
    keyboard.add_hotkey('F9', on_f9_press)
    keyboard.add_hotkey('F10', on_f10_press)
    print('热键注册成功')
    
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('退出测试')

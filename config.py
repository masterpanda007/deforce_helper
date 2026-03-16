#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理模块
"""

import os
import json

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

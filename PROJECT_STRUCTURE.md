# 项目结构说明

三角洲游戏助手项目已重构为模块化结构，便于维护和扩展。

## 📁 目录结构

```
deforce_helper/
├── main.py                      # 程序入口文件
├── config.py                    # 配置管理模块
├── requirements.txt             # 依赖包列表
├── skills.json                  # 技能数据文件
├── README.md                    # 详细使用说明
├── PROJECT_STRUCTURE.md         # 本文档
├── 启动.bat                     # Windows一键启动脚本
├── build.spec                   # 基础版打包配置
├── build_complete.spec          # 完整版打包配置
├── widgets/                     # 自定义窗口组件模块
│   ├── __init__.py
│   ├── crosshair.py             # 准星窗口
│   └── notification.py          # 通知窗口
├── ui/                          # UI界面模块
│   ├── __init__.py
│   ├── main_window.py           # 主窗口
│   └── tabs.py                  # Tab页辅助函数
└── (备份文件)
    ├── deforce_helper.py.bak    # 原单文件版本
    ├── deforce_helper_complete.py
    └── ai_chat_module.py
```

## 📦 模块说明

### 1. config.py - 配置管理模块
- `CONFIG_FILE`: 配置文件路径
- `SKILLS_FILE`: 技能数据文件路径
- `DEFAULT_CONFIG`: 默认配置字典
- `DEFAULT_SKILLS`: 默认技能数据
- `load_config()`: 加载配置
- `save_config(config)`: 保存配置
- `load_skills()`: 加载技能数据
- `save_skills(skills)`: 保存技能数据

### 2. widgets/ - 窗口组件模块

#### widgets/crosshair.py - 准星窗口
- `CrosshairWindow`: 准星窗口类
  - `init_ui()`: 初始化UI
  - `update_position()`: 更新位置到屏幕中心
  - `paintEvent()`: 绘制准星

#### widgets/notification.py - 通知窗口
- `NotificationWindow`: 通知窗口类
  - `init_ui()`: 初始化UI
  - `show_message(message)`: 显示消息
  - `update_position()`: 更新通知位置
  - `paintEvent()`: 绘制通知

### 3. ui/ - UI界面模块

#### ui/main_window.py - 主窗口
- `MainWindow`: 主窗口类
  - `init_ui()`: 初始化主界面
  - `create_*_tab()`: 创建各个Tab页
  - `toggle_*()`: 各种切换功能
  - `block_network_upload()`: 阻断上传
  - `unblock_network_upload()`: 恢复上传

#### ui/tabs.py - Tab页辅助函数
- `create_promotion_bar()`: 创建推广栏
- `add_skill_card(parent_layout, skill)`: 添加技能卡片

### 4. main.py - 程序入口
- `main()`: 主函数，启动应用

## 🔧 维护指南

### 添加新功能
1. 若需要新的窗口组件 → 在 `widgets/` 目录下创建新文件
2. 若需要UI页面 → 在 `ui/` 目录下修改或创建文件
3. 配置相关 → 修改 `config.py`

### 修改配置
- 默认配置: 修改 `config.py` 中的 `DEFAULT_CONFIG`
- 默认技能: 修改 `config.py` 中的 `DEFAULT_SKILLS`

### 打包
- 基础版: `pyinstaller build.spec`
- 完整版: `pyinstaller build_complete.spec`

## 🚀 运行方式

```bash
# 方式1: 直接运行
python main.py

# 方式2: 使用启动脚本 (Windows)
双击 启动.bat
```

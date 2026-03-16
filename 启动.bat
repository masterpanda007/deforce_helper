@echo off
chcp 65001 >nul
echo ========================================
echo   三角洲游戏助手 - 小麻虾电竞
echo ========================================
echo.

echo [1/3] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未检测到Python，请先安装Python 3.8+
    pause
    exit /b 1
)
echo Python环境正常
echo.

echo [2/3] 检查依赖...
python -c "import PyQt6, keyboard" >nul 2>&1
if errorlevel 1 (
    echo 正在安装依赖...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo 依赖安装失败，请检查网络连接
        pause
        exit /b 1
    )
)
echo 依赖检查完成
echo.

echo [3/3] 启动程序...
echo.
python main.py

if errorlevel 1 (
    echo.
    echo 程序运行出错，请检查错误信息
    pause
)

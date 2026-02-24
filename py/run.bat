@echo off
REM Windows 批处理脚本 - 快速启动 HTML 生成工具
REM 运行方式: 双击此文件或在 cmd 中执行 run.bat

echo.
echo ====================================================================
echo.
echo     ^^!^^! HTML 生成工具 - Windows 版本 ^^!^^!
echo.
echo ====================================================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ^^!^^! 错误: 未找到 Python
    echo 请先安装 Python 3.6 或更高版本
    pause
    exit /b 1
)

echo ✓ 找到 Python 环境
echo.

REM 安装依赖
echo 正在安装/检查依赖...
python -m pip install -q openpyxl jinja2
if errorlevel 1 (
    echo ^^! 警告: 依赖安装失败，继续尝试...
)

echo.
echo ====================================================================
echo 正在生成 HTML 文件...
echo ====================================================================
echo.

REM 运行生成脚本
python run.py

if errorlevel 1 (
    echo.
    echo 生成失败，请检查错误信息
    pause
    exit /b 1
)

echo.
echo ====================================================================
echo ✓ 完成！按任意键关闭窗口...
echo ====================================================================
pause

#!/usr/bin/env powershell
# PowerShell 脚本 - HTML 生成工具启动器
# 运行方式: powershell -ExecutionPolicy Bypass -File run.ps1

Write-Host "`n"
Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "                   🎬 HTML 生成工具 v1.0" -ForegroundColor Yellow
Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "`n"

# 检查 Python
Write-Host "检查 Python 环境..." -ForegroundColor Green
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue

if ($null -eq $pythonCmd) {
    Write-Host "❌ 错误: 未找到 Python" -ForegroundColor Red
    Write-Host "请先安装 Python 3.6 或更高版本" -ForegroundColor Yellow
    Read-Host "按 Enter 键退出"
    exit 1
}

$pythonVersion = python --version
Write-Host "✓ $pythonVersion" -ForegroundColor Green
Write-Host ""

# 安装依赖
Write-Host "安装依赖包..." -ForegroundColor Green
python -m pip install -q openpyxl jinja2 | Out-Null

if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  依赖安装可能失败，继续尝试..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "正在生成 HTML 文件..." -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# 运行生成脚本
& python run.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ 生成失败，请检查错误信息" -ForegroundColor Red
    Read-Host "按 Enter 键退出"
    exit 1
}

Write-Host ""
Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "✅ 完成！" -ForegroundColor Green
Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Read-Host "按 Enter 键关闭窗口"

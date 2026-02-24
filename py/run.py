#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速启动脚本 - 一键运行所有生成步骤
"""

import os
import sys
import subprocess


def run_command(cmd, description):
    """运行命令并显示进度"""
    print(f"\n{'=' * 60}")
    print(f"📋 {description}")
    print(f"{'=' * 60}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=False)
        if result.returncode == 0:
            print(f"✅ {description} 完成！")
            return True
        else:
            print(f"❌ {description} 失败！")
            return False
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False


def check_excel_file():
    """检查 Excel 文件是否存在"""
    if not os.path.exists('resource_config.xlsx'):
        print("⚠️  警告: resource_config.xlsx 不存在")
        print("将从示例生成...")
        return False
    return True


def main():
    """主函数"""
    print("\n")
    print("┌" + "─" * 58 + "┐")
    print("│" + " " * 10 + "🎬 网站 HTML 生成工具 v1.0" + " " * 21 + "│")
    print("└" + "─" * 58 + "┘")
    
    # 检查 Python 版本
    if sys.version_info < (3, 6):
        print("❌ 错误: 需要 Python 3.6 或更高版本")
        return False
    
    print(f"✓ Python 版本: {sys.version}")
    
    # 第一步: 安装依赖
    print("\n" + "=" * 60)
    print("1️⃣  安装依赖包")
    print("=" * 60)
    try:
        import openpyxl
        print("✓ openpyxl 已安装")
    except ImportError:
        print("⚠️  openpyxl 未安装，正在安装...")
        run_command(
            f"{sys.executable} -m pip install openpyxl jinja2",
            "安装依赖包"
        )
    
    # 第二步: 创建示例 Excel（如果不存在）
    if not check_excel_file():
        if run_command(
            f"{sys.executable} create_sample_excel.py",
            "创建示例 Excel 文件"
        ):
            print("\n💡 提示: 请编辑 resource_config.xlsx，添加你的数据，然后重新运行此脚本")
            return True
    
    # 第三步: 生成 HTML
    if run_command(
        f"{sys.executable} generate_html_from_excel.py",
        "生成 HTML 页面"
    ):
        print("\n" + "=" * 60)
        print("✅ 所有步骤完成！")
        print("=" * 60)
        print("\n📝 后续步骤:")
        print("1. 检查 sections/ 目录中生成的 HTML 文件")
        print("2. 更新 index.html 中的 section 卡片配置")
        print("3. 更新 docs/js/count-badges.js 中的卡片数量")
        print("4. 更新 docs/js/global-search.js 中的搜索配置")
        print("5. 检查 res/ 目录中的海报图片是否存在")
        print("\n📖 详细说明请参考: SCRIPT_README.md")
        return True
    
    return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

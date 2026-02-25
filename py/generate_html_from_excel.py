#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 Excel 生成 HTML 页面脚本
功能：
1. 从 Sheet0 生成 index.html
2. 从 Sheet1-n 生成 section-01.html ~ section-n.html
"""

import os
import re
import random
import string
from pathlib import Path
from openpyxl import load_workbook
from jinja2 import Template


# ===========================
# 配置
# ===========================
EXCEL_FILE = "./templates/resource_config.xlsx"  # Excel 文件名
OUTPUT_DIR = "sections"  # 输出目录
TEMPLATE_SECTION = "./templates/section-tpl.html"  # section 模板文件
TEMPLATE_CARD = "./templates/card-tpl.html"  # card 模板文件


# ===========================
# 主流程
# ===========================
def main():
    """主函数"""
    print("=" * 60)
    print("HTML 生成器 - 从 Excel 生成网站页面")
    print("=" * 60)
    
    # 检查 Excel 文件
    if not os.path.exists(EXCEL_FILE):
        print(f"❌ 错误: 找不到 {EXCEL_FILE}")
        print(f"请在项目根目录放置 {EXCEL_FILE} 文件")
        return
    
    try:
        # 加载 Excel 数据
        print(f"\n📖 读取 Excel 文件: {EXCEL_FILE}")
        sheets = load_excel_data(EXCEL_FILE)
        print(f"✓ 找到 {len(sheets)} 个 Sheet")
        
        # 创建输出目录
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        print(f"✓ 输出目录: {OUTPUT_DIR}/")
        
        # 处理每个 Sheet
        sheet_list = list(sheets.keys())
        
        generate_sections(sheets, sheet_list[1:])
        generate_index(sheets, sheet_list[0])
        
        print("\n" + "=" * 60)
        print("✅ 生成完成！")
        print("=" * 60)
        print("\n📝 后续步骤:")
        print("1. 检查生成的 HTML 文件是否正确")
        print("2. 更新 index.html 中的 section 卡片配置")
        print("3. 更新 docs/js/count-badges.js 中的卡片数量")
        print("4. 更新 docs/js/global-search.js 中的搜索配置")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        


def generate_sections(sheets, sheet_list) :
    # Sheet1-n 生成 section HTML
    for idx, sheet_name in enumerate(sheet_list):
        print(f"\n📄 转换 {sheet_name} -> section-{idx:02d}.html")
        
        table = sheets[sheet_name]
        header = table['headers']
        lines = table['data']
        print(header)
        print(lines)

        if not lines:
            print(f"  ⚠️  {sheet_name} 没有数据，跳过")
            continue
        
        # 获取 section 标题 (从第一行的 sheet 名称或配置)
        section_title = sheet_name
        
        # 生成 HTML
        html_content = generate_section(
            lines,
            section_title,
            idx
        )
        
        # 保存文件
        output_file = os.path.join(OUTPUT_DIR, f'section-{idx:02d}.html')
        # with open(output_file, 'w', encoding='utf-8') as f:
        #     f.write(html_content)
        
        print(f"  ✓ 生成 {len(lines)} 个卡片")
        print(f"  ✓ 保存至: {output_file}")


def generate_section(sheet_data, section_title, section_number):
    """生成 section HTML（从模板渲染）"""
    # 生成卡片 HTML
    cards_html = ''
    for movie in sheet_data:
        cards_html += generate_card_html(movie)
    
    # 准备模板上下文
    context = {
        'section_title': section_title,
        'section_number': section_number,
        'cards': cards_html
    }
    
    # 加载 section 模板并渲染
    tpl_text = load_template_section()
    tpl = Template(tpl_text)
    return tpl.render(**context)




def generate_index(sheets, sheet_list) :
    # Sheet0 用于生成 index.html (如果存在)
    if sheet_list and sheet_list[0] == 'Sheet0':
        print(f"\n📄 处理 Sheet0 -> index.html")
        # generate_index_html 需要自定义实现
        print("  (需手动调整 index.html 配置)")
        sheet_list = sheet_list[1:]  # 移除 Sheet0


# ===========================
# 工具函数
# ===========================
def generate_uuid(length=8):
    """生成随机 UUID (8 字符)"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def get_badge_html(format_name):
    """生成格式徽章 HTML"""
    badge_colors = {
        'mp4': ('blue', 'mp4'),
        'mkv': ('purple', 'mkv'),
        'rmvb': ('orange', 'rmvb'),
        'tv': ('green', 'tv'),
        'avi': ('red', 'avi'),
        'flv': ('yellow', 'flv'),
    }
    
    color, label = badge_colors.get(format_name.lower(), ('gray', format_name))
    return f'<img src="https://img.shields.io/badge/{label}-Yes-{color}.svg" data-bs-toggle="tooltip" title="视频格式">'


def parse_formats(format_str):
    """解析格式列表，返回 HTML"""
    if not format_str or format_str.strip() == '':
        return ''
    
    formats = [f.strip() for f in format_str.split(',')]
    return ' '.join([get_badge_html(f) for f in formats])


def load_excel_data(excel_file):
    """加载 Excel 数据"""
    if not os.path.exists(excel_file):
        raise FileNotFoundError(f"找不到文件: {excel_file}")
    
    wb = load_workbook(excel_file)
    sheets = {}
    
    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        data = []
        
        # 获取标题行
        headers = []
        for cell in ws[1]:
            headers.append(cell.value)
        
        # 读取数据行
        for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=False), start=2):
            row_data = {}
            for col_idx, cell in enumerate(row):
                header = headers[col_idx]
                row_data[header] = cell.value if cell.value is not None else ''
            data.append(row_data)
        
        sheets[sheet_name] = {
            'headers': headers,
            'data': data
        }
    
    return sheets


def load_template_section():
    """加载 section 模板"""
    with open(TEMPLATE_SECTION, 'r', encoding='utf-8') as f:
        return f.read()


def load_template_card():
    """加载 card 模板"""
    with open(TEMPLATE_CARD, 'r', encoding='utf-8') as f:
        return f.read()


def generate_card_html(card_data):
    """生成单个电影卡片 HTML（从模板渲染）"""
    # 准备字段
    context = {
        'title': card_data.get('标题', '未命名'),
        'subtitle': card_data.get('副标题', ''),
        'description': card_data.get('简介', ''),
        'language': card_data.get('语言', '日语'),
        'subtitle_text': card_data.get('字幕', '中文'),
        'download_name': card_data.get('网盘名称', '百度网盘'),
        'download_link': card_data.get('下载链接', 'TODO'),
        'password': card_data.get('解压密码', generate_uuid()),
        'formats': card_data.get('支持格式', 'mp4'),
        'release_time': card_data.get('上映时间', '待定'),
        'poster_path': card_data.get('海报路径', '../res/film/其他系列/默认/title.webp')
    }

    # 生成格式徽章（仍保留原有解析逻辑）
    context['format_badges'] = parse_formats(context['formats'])

    # 加载 card 模板并渲染
    tpl_text = load_template_card()
    tpl = Template(tpl_text)
    return tpl.render(**context)





def generate_index_html(sheets_config):
    """生成 index.html"""
    # 读取现有的 index.html
    index_file = "index.html"
    if not os.path.exists(index_file):
        print(f"警告: {index_file} 不存在，将创建新文件")
        return None
    
    with open(index_file, 'r', encoding='utf-8') as f:
        index_content = f.read()
    
    # 从 Excel 的 Sheet0 获取配置
    # 这里需要根据 Sheet0 的数据结构来更新 index.html
    # 假设 Sheet0 包含: section_id, section_title, description, image_url, count
    
    print("✓ index.html 配置完成 (需手动调整)")
    return index_content





if __name__ == '__main__':
    main()

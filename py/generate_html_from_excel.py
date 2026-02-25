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
TEMPLATE_SECTION = "./templates/section-00.html"  # section 模板文件


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
        
        # Sheet0 用于生成 index.html (如果存在)
        if sheet_list and sheet_list[0] == 'Sheet0':
            print(f"\n📄 处理 Sheet0 -> index.html")
            # generate_index_html 需要自定义实现
            print("  (需手动调整 index.html 配置)")
            sheet_list = sheet_list[1:]  # 移除 Sheet0
        
        # Sheet1-n 生成 section HTML
        for idx, sheet_name in enumerate(sheet_list, start=1):
            print(f"\n📄 处理 {sheet_name} -> section-{idx:02d}.html")
            
            sheet_data = sheets[sheet_name]
            movies = sheet_data['data']
            
            if not movies:
                print(f"  ⚠️  {sheet_name} 没有数据，跳过")
                continue
            
            # 获取 section 标题 (从第一行的 sheet 名称或配置)
            section_title = sheet_name
            
            # 生成 HTML
            html_content = generate_section_html(
                movies,
                section_title,
                idx
            )
            
            # 保存文件
            output_file = os.path.join(OUTPUT_DIR, f'section-{idx:02d}.html')
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"  ✓ 生成 {len(movies)} 个卡片")
            print(f"  ✓ 保存至: {output_file}")
        
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


def generate_card_html(movie_data):
    """生成单个电影卡片 HTML"""
    title = movie_data.get('标题', '未命名')
    subtitle = movie_data.get('副标题', '')
    description = movie_data.get('简介', '')
    language = movie_data.get('语言', '日语')
    subtitle_text = movie_data.get('字幕', '中文')
    download_name = movie_data.get('网盘名称', '百度网盘')
    download_link = movie_data.get('下载链接', 'TODO')
    password = movie_data.get('解压密码', generate_uuid())
    formats = movie_data.get('支持格式', 'mp4')
    release_time = movie_data.get('上映时间', '待定')
    poster_path = movie_data.get('海报路径', '../res/film/其他系列/默认/title.webp')
    
    # 生成格式徽章
    format_badges = parse_formats(formats)
    
    # 副标题 HTML
    subtitle_html = f'<h6><i>（{subtitle}）</i></h6>' if subtitle else ''
    
    # 生成下载按钮
    if download_link.upper() == 'TODO':
        download_button = f'''<button type="button" class="btn button-link" data-bs-toggle="modal" data-bs-target="#downloadModal"
                        data-bs-download="TODO"
                        data-uuid="{password}">[{download_name}]</button>'''
    else:
        download_button = f'''<button type="button" class="btn button-link" data-bs-toggle="modal" data-bs-target="#downloadModal" 
                        data-bs-download="{download_link}" 
                        data-uuid="{password}">[{download_name}]</button>'''
    
    card_html = f'''        <div class="col-sm-12 col-md-6 col-lg-4">
          <div class="card mb-3 bold-border" style="max-width: 540px;">
            <div class="row g-0">
              <div class="col-md-4">
                <a href="{poster_path}" target="_blank">
                  <img src="{poster_path}" class="card-img" alt="{title}">
                </a>
              </div>
              <div class="col-md-8">
                <div class="card-body">
                  <h4 class="card-title">{title}</h4>{subtitle_html}
                  <ul class="list-group">
                    <li class="list-group-item list-group-item-primary">{description}</li>
                    <li class="list-group-item list-group-item-success">语言：{language}</li>
                    <li class="list-group-item list-group-item-info">字幕：{subtitle_text}</li>
                    <li class="list-group-item list-group-item-danger">下载：
                      {download_button}
                    </li>
                    <li class="list-group-item list-group-item-warning">
                      {format_badges}
                    </li>
                  </ul>
                </div>
              </div>
            </div>
            <div class="card-footer">
              <small class="text-muted">上映时间：{release_time}</small>
            </div>
          </div>
        </div>
'''
    return card_html


def generate_section_html(sheet_data, section_title, section_number):
    """生成 section HTML"""
    template = load_template_section()
    
    # 替换标题
    template = re.sub(
        r'<h4[^>]*>XXXX系列</h4>',
        f'<h4 id="section-{section_number:02d}" style="color:#ffff00; background-color:#000000; text-align: center;">{section_title}</h4>',
        template
    )
    
    # 生成卡片
    cards_html = ''
    for movie in sheet_data:
        cards_html += generate_card_html(movie)
    
    # 替换卡片区域
    # 找到 <!-- 这是模板。... --> 之间的空白区域，替换成卡片
    template = re.sub(
        r'(<!--\s*这是模板。[\s\S]*?-->\s*)(\s*</div>)',
        f'\\1\n{cards_html}\n      \\2',
        template
    )
    
    return template


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

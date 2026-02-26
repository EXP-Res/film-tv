#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解析 sections/*.html 中的卡片并导出到 Excel
输出文件: templates/resource_config.xlsx
"""
import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Font, PatternFill, Alignment


SECTIONS_DIR = Path(__file__).resolve().parents[1] / 'sections'
OUT_XLSX = Path(__file__).resolve().parents[1] / 'templates' / 'resource_config.xlsx'


def extract_from_card(card_div):
    """从单个 card div 提取字段，返回 dict"""
    # poster - from image src
    poster = ''
    img = card_div.select_one('img.card-img')
    if img:
        poster = img.get('src', '')

    # title
    title_el = card_div.select_one('.card-title')
    title = title_el.get_text(strip=True) if title_el else ''

    # subtitle - not present in current HTML, but support h6 if it exists
    subtitle_el = card_div.select_one('h6')
    subtitle = ''
    if subtitle_el:
        subtitle = subtitle_el.get_text(strip=True)

    # description - from primary list item
    desc_el = card_div.select_one('.list-group-item-primary')
    description = desc_el.get_text(strip=True) if desc_el else ''

    # language - from success list item
    lang_el = card_div.select_one('.list-group-item-success')
    language = lang_el.get_text(strip=True).replace('语言：', '').strip() if lang_el else '日语'

    # subtitle_text (字幕) - from info list item
    sub_el = card_div.select_one('.list-group-item-info')
    subtitle_text = sub_el.get_text(strip=True).replace('字幕：', '').strip() if sub_el else '中文'

    # download info - from danger list item
    menu_path = ''
    download_link = ''
    password = ''
    download_li = card_div.select_one('.list-group-item-danger')
    if download_li:
        # check for menu link
        a_menu = download_li.find('a')
        if a_menu and a_menu.has_attr('href'):
            menu_path = a_menu['href']
        # check for download button
        btn = download_li.find('button')
        if btn:
            download_link = btn.get('data-bs-download', '').strip()
            password = btn.get('data-uuid', '').strip()

    # formats - from warning list item
    formats = []
    warning_li = card_div.select_one('.list-group-item-warning')
    if warning_li:
        for img in warning_li.select('img'):
            src = img.get('src', '')
            # extract from shields.io badge URL: /badge/FORMAT-Yes-COLOR.svg
            m = re.search(r'/badge/([^-]+)-Yes-', src)
            if m:
                formats.append(m.group(1).lower())

    formats_str = ','.join(formats)

    # card footer - from footer small tag (get all HTML content as-is)
    release = ''
    card_foot = ''
    foot = card_div.select_one('.card-footer')
    if foot:
        small = foot.select_one('small')
        if small:
            # get the inner HTML of the small tag as-is
            card_foot = str(small.decode_contents()).strip()

    return {
        '封面图片路径': poster,
        '主标题': title,
        '副标题': subtitle,
        '概要': description,
        '语言': language,
        '字幕': subtitle_text,
        '目录路径': menu_path,
        '网盘名称': '百度网盘',
        '下载链接': download_link,
        '解压密码': password,
        '支持格式': formats_str,
        '卡片页脚': card_foot,
    }


def process_section_file(path: Path):
    """解析 section HTML 文件，返回 (标题, 卡片列表)"""
    try:
        html = path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"  ❌ 读取失败: {e}")
        return path.stem, []

    soup = BeautifulSoup(html, 'html.parser')

    # section title from h4
    h4 = soup.find('h4')
    section_title = h4.get_text(strip=True) if h4 else path.stem

    # find card containers - locate all card wrapper divs
    cards = []
    for card_div in soup.select('div.card'):
        # ensure this is one of the item cards (has .card-title)
        if card_div.select_one('.card-title'):
            try:
                card_data = extract_from_card(card_div)
                cards.append(card_data)
            except Exception as e:
                print(f"  ⚠️  解析单个卡片失败: {e}")
                continue

    return section_title, cards


def write_excel(sections_data):
    """将 sections 数据写入 Excel，如果文件存在则更新对应 sheet"""
    
    # 尝试加载现有 Excel
    if OUT_XLSX.exists():
        print(f"📖 加载现有 Excel: {OUT_XLSX}")
        wb = load_workbook(OUT_XLSX)
    else:
        print(f"📝 创建新 Excel 文件")
        wb = Workbook()
        # 移除默认 sheet
        if 'Sheet' in wb.sheetnames:
            wb.remove(wb['Sheet'])

    headers = ['封面图片路径', '主标题', '副标题', '概要', '语言', '字幕', '目录路径', '网盘名称', '下载链接', '解压密码', '支持格式', '卡片页脚']

    for idx, (title, cards) in enumerate(sections_data, 1):
        # sheet name max 31 chars
        sheet_name = title[:31] if title else f'Sheet{idx}'
        
        # avoid duplicate names by checking existing sheets
        orig_name = sheet_name
        counter = 1
        while sheet_name in wb.sheetnames:
            sheet_name = f"{orig_name[:28]}_{counter}"
            counter += 1

        # 如果 sheet 已存在，删除重新创建
        if sheet_name in wb.sheetnames:
            del wb[sheet_name]

        # 创建新 sheet
        ws = wb.create_sheet(sheet_name)
        
        # 添加表头并格式化
        ws.append(headers)
        header_row = ws[1]
        for cell in header_row:
            cell.font = Font(bold=True)
            cell.fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
            cell.font = Font(bold=True, color='FFFFFF')
            cell.alignment = Alignment(horizontal='center', vertical='center')
        
        # 冻结表头第一行
        ws.freeze_panes = 'A2'

        # 添加数据行
        for card_data in cards:
            row = [card_data.get(h, '') for h in headers]
            ws.append(row)

        # 调整列宽
        ws.column_dimensions['A'].width = 25  # 封面图片路径
        ws.column_dimensions['B'].width = 15  # 主标题
        ws.column_dimensions['C'].width = 12  # 副标题
        ws.column_dimensions['D'].width = 30  # 概要
        ws.column_dimensions['E'].width = 8   # 语言
        ws.column_dimensions['F'].width = 12  # 字幕
        ws.column_dimensions['G'].width = 25  # 目录路径
        ws.column_dimensions['H'].width = 10  # 网盘名称
        ws.column_dimensions['I'].width = 35  # 下载链接
        ws.column_dimensions['J'].width = 10  # 解压密码
        ws.column_dimensions['K'].width = 12  # 支持格式
        ws.column_dimensions['L'].width = 15  # 卡片页脚

        print(f"  ✓ {sheet_name}: {len(cards)} 张卡片")

    OUT_XLSX.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUT_XLSX)


def main():
    print("=" * 60)
    print("卡片提取工具 - 从 HTML 导出到 Excel")
    print("=" * 60)
    
    if not SECTIONS_DIR.exists():
        print(f"❌ sections 目录不存在: {SECTIONS_DIR}")
        return

    # 按编号排序
    files = sorted(SECTIONS_DIR.glob('section-*.html'), 
                   key=lambda f: int(re.search(r'\d+', f.name).group()) if re.search(r'\d+', f.name) else 0)
    
    if not files:
        print("❌ 未找到任何 section-*.html 文件")
        return

    print(f"\n📂 找到 {len(files)} 个 section 文件\n")

    sections_data = []
    for f in files:
        title, cards = process_section_file(f)
        print(f"📄 {f.name}: {title}")
        if cards:
            print(f"  ✓ {len(cards)} 张卡片")
        else:
            print(f"  ⚠️  无卡片")
        sections_data.append((title, cards))

    print("\n💾 写入 Excel...")
    write_excel(sections_data)
    
    print(f"\n✅ 完成！")
    print(f"📁 输出文件: {OUT_XLSX}")
    print(f"📊 总计 {len(sections_data)} 个 sheet")


if __name__ == '__main__':
    main()

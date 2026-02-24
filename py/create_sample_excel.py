#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建示例 Excel 文件模板
"""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment


def create_sample_excel():
    """创建示例 Excel 文件"""
    wb = Workbook()
    
    # 删除默认 sheet
    if 'Sheet' in wb.sheetnames:
        wb.remove(wb['Sheet'])
    
    # Sheet0: 首页配置（可选）
    ws0 = wb.create_sheet('Sheet0', 0)
    ws0['A1'] = 'section_id'
    ws0['B1'] = 'section_name'
    ws0['C1'] = 'description'
    ws0['D1'] = 'image_url'
    ws0['E1'] = 'count'
    
    ws0['A2'] = '1'
    ws0['B2'] = '推理探案系列'
    ws0['C2'] = '死神小学生与大侦探的推理世界'
    ws0['D2'] = './imgs/covers/08.jpg'
    ws0['E2'] = '28'
    
    # Sheet1: 电影资源配置示例
    ws1 = wb.create_sheet('推理探案系列', 1)
    
    # 设置表头
    headers = ['标题', '副标题', '简介', '语言', '字幕', '网盘名称', '下载链接', '解压密码', '支持格式', '上映时间', '海报路径']
    for col_idx, header in enumerate(headers, start=1):
        cell = ws1.cell(row=1, column=col_idx)
        cell.value = header
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
        cell.alignment = Alignment(horizontal="center", vertical="center")
    
    # 示例数据 1: 柯南剧场版
    ws1['A2'] = '名侦探柯南：时计坍塌的摩天楼'
    ws1['B2'] = '第1部'
    ws1['C2'] = '建筑大亨的摩天楼遭到炸弹威胁，小学生侦探柯南必须在有限的时间内找出真凶，阻止爆炸发生...'
    ws1['D2'] = '日语'
    ws1['E2'] = '中文'
    ws1['F2'] = '百度网盘'
    ws1['G2'] = 'https://pan.baidu.com/s/xxxxx?pwd=xxxx'
    ws1['H2'] = 'abcd1234'
    ws1['I2'] = 'mp4,mkv'
    ws1['J2'] = '1997-04-19'
    ws1['K2'] = '../res/film/推理系列/柯南/conan00.webp'
    
    # 示例数据 2: 金田一事件簿
    ws1['A3'] = '金田一少年事件簿：瞳孔之中的黑影'
    ws1['B3'] = '电影版'
    ws1['C3'] = '神秘村落连续杀人案，金田一需要在极端环境中破案...'
    ws1['D3'] = '日语'
    ws1['E3'] = '中文'
    ws1['F3'] = '百度网盘'
    ws1['G3'] = 'TODO'
    ws1['H3'] = 'xyz98765'
    ws1['I3'] = 'mkv'
    ws1['J3'] = '2006-11-18'
    ws1['K3'] = '../res/film/推理系列/金田一/title1.webp'
    
    # Sheet2: 另一个系列示例
    ws2 = wb.create_sheet('数码暴龙系列', 2)
    
    for col_idx, header in enumerate(headers, start=1):
        cell = ws2.cell(row=1, column=col_idx)
        cell.value = header
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
        cell.alignment = Alignment(horizontal="center", vertical="center")
    
    ws2['A2'] = '数码宝贝：小镇英雄'
    ws2['B2'] = '电影版'
    ws2['C2'] = '小学生进入数码世界，与数码宝贝一起对抗邪恶势力...'
    ws2['D2'] = '日语'
    ws2['E2'] = '中文'
    ws2['F2'] = '百度网盘'
    ws2['G2'] = 'TODO'
    ws2['H2'] = 'digi1234'
    ws2['I2'] = 'mp4'
    ws2['J2'] = '1997-11-21'
    ws2['K2'] = '../res/film/动画系列/数码暴龙/title01.webp'
    
    # 设置列宽
    ws1.column_dimensions['A'].width = 25
    ws1.column_dimensions['B'].width = 15
    ws1.column_dimensions['C'].width = 40
    ws1.column_dimensions['D'].width = 12
    ws1.column_dimensions['E'].width = 12
    ws1.column_dimensions['F'].width = 12
    ws1.column_dimensions['G'].width = 30
    ws1.column_dimensions['H'].width = 12
    ws1.column_dimensions['I'].width = 12
    ws1.column_dimensions['J'].width = 15
    ws1.column_dimensions['K'].width = 40
    
    ws2.column_dimensions['A'].width = 25
    ws2.column_dimensions['B'].width = 15
    ws2.column_dimensions['C'].width = 40
    ws2.column_dimensions['D'].width = 12
    ws2.column_dimensions['E'].width = 12
    ws2.column_dimensions['F'].width = 12
    ws2.column_dimensions['G'].width = 30
    ws2.column_dimensions['H'].width = 12
    ws2.column_dimensions['I'].width = 12
    ws2.column_dimensions['J'].width = 15
    ws2.column_dimensions['K'].width = 40
    
    # 保存文件
    output_file = 'resource_config.xlsx'
    wb.save(output_file)
    print(f"✅ 示例 Excel 文件已创建: {output_file}")
    print("\n📋 Excel 结构说明:")
    print("  - Sheet0: 首页配置（可选，用于更新 index.html）")
    print("  - Sheet1-n: 每个 sheet 对应一个 section HTML")
    print("\n📝 Excel 字段说明:")
    print("  - 标题 (必需): 电影/剧集名称")
    print("  - 副标题 (可选): 补充说明，显示在标题下方")
    print("  - 简介 (必需): 内容描述，不建议过长")
    print("  - 语言 (必需): 原音语言")
    print("  - 字幕 (必需): 字幕信息（如：中文、中文,英文）")
    print("  - 网盘名称 (必需): 下载按钮显示的文本")
    print("  - 下载链接 (必需): 百度网盘链接或 'TODO'")
    print("  - 解压密码 (必需): 8 位解压密码，留空将自动生成")
    print("  - 支持格式 (必需): 视频格式，多个用逗号分隔（mp4, mkv, rmvb, tv, avi, flv）")
    print("  - 上映时间 (必需): 发布/上映日期")
    print("  - 海报路径 (必需): 相对路径，如 ../res/film/.../title.webp")


if __name__ == '__main__':
    create_sample_excel()

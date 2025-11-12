# -*- coding: utf-8 -*-
"""
生成各个 section 独立 HTML 文件的脚本 - 使用模板系统
"""
import re

# Section 边界定义
sections = {
    "section-01": {"name": "世界奇妙物语系列", "start": 93, "end": 3082},
    "section-02": {"name": "藤原龙也系列", "start": 3083, "end": 4429},
    "section-03": {"name": "憨豆先生系列", "start": 4430, "end": 4644},
    "section-04": {"name": "生化危机系列", "start": 4645, "end": 4987},
    "section-05": {"name": "哈利波特系列", "start": 4988, "end": 5264},
    "section-06": {"name": "死神来了系列", "start": 5265, "end": 5474},
    "section-07": {"name": "动画系列", "start": 5475, "end": 5652},
    "section-99": {"name": "其他系列", "start": 5653, "end": 5689}
}

# 读取模板
with open('templates/header.html', 'r', encoding='utf-8') as f:
    header_template = f.read()

with open('templates/footer.html', 'r', encoding='utf-8') as f:
    footer_template = f.read()

# 读取原始 index.old.html（完整内容版本）
with open('index.old.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 为每个 section 生成独立的 HTML 文件
for section_id, info in sections.items():
    section_name = info['name']
    start_line = info['start'] - 1  # 转换为 0-based 索引
    end_line = info['end']
    
    # 提取 section 内容
    section_content = ''.join(lines[start_line:end_line])
    
    # 应用模板变量
    section_header = header_template.replace('{{PAGE_TITLE}}', section_name)
    section_header = section_header.replace('{{BASE_PATH}}', '../')
    section_header = section_header.replace('{{HOME_LINK}}', '../index.html')
    
    section_footer = footer_template.replace('{{BASE_PATH}}', '../')
    
    # 更新 section_content 中的路径
    section_content = section_content.replace('./res/', '../res/')
    section_content = section_content.replace('./imgs/', '../imgs/')
    
    # 组合完整的 HTML
    full_html = section_header + section_content + section_footer
    
    # 写入文件
    output_path = f'sections/{section_id}.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"✓ 已生成: {output_path} ({section_name})")

print("\n所有 section 文件已生成完毕！")

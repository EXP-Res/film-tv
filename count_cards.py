#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动统计各section页面的卡片数量并更新index.html中的徽章数字
"""

import os
import re
from pathlib import Path

def count_cards_in_section(section_file):
    """统计section文件中的卡片数量"""
    try:
        with open(section_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 统计 class="card mb-3 bold-border" 的数量
        # 这是每个电影/剧集卡片的标识
        card_pattern = r'<div class="card mb-3 bold-border"'
        cards = re.findall(card_pattern, content)
        
        return len(cards)
    except Exception as e:
        print(f"❌ 读取 {section_file} 失败: {e}")
        return 0

def update_index_badges(card_counts):
    """更新index.html中的徽章数字"""
    index_file = 'index.html'
    
    try:
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 定义section与徽章的映射关系
        section_badge_map = {
            'section-01': (r'(<!-- Section 01:.*?<span class="section-badge">)(\d+\+?)( 部</span>)', 'section-01.html'),
            'section-02': (r'(<!-- Section 02:.*?<span class="section-badge">)(\d+\+?)( 部</span>)', 'section-02.html'),
            'section-03': (r'(<!-- Section 03:.*?<span class="section-badge">)(\d+\+?)( 部</span>)', 'section-03.html'),
            'section-04': (r'(<!-- Section 04:.*?<span class="section-badge">)(\d+\+?)( 部</span>)', 'section-04.html'),
            'section-05': (r'(<!-- Section 05:.*?<span class="section-badge">)(\d+\+?)( 部</span>)', 'section-05.html'),
            'section-06': (r'(<!-- Section 06:.*?<span class="section-badge">)(\d+\+?)( 部</span>)', 'section-06.html'),
            'section-07': (r'(<!-- Section 07:.*?<span class="section-badge">)(\d+\+?)( 部</span>)', 'section-07.html'),
            'section-99': (r'(<!-- Section 99:.*?<span class="section-badge">)(\d+\+?)( 部</span>)', 'section-99.html'),
        }
        
        updated = False
        for section_key, (pattern, section_file) in section_badge_map.items():
            count = card_counts.get(section_key, 0)
            
            # 使用正则表达式替换，支持跨多行匹配
            def replacer(match):
                return f'{match.group(1)}{count}{match.group(3)}'
            
            new_content, n = re.subn(pattern, replacer, content, flags=re.DOTALL)
            
            if n > 0:
                content = new_content
                updated = True
                print(f'✓ 更新 {section_key}: {count} 部')
            else:
                print(f'⚠️  未找到 {section_key} 的徽章位置')
        
        if updated:
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'\n✅ 已更新 {index_file}')
        else:
            print('\n⚠️  没有进行任何更新')
            
    except Exception as e:
        print(f'❌ 更新 {index_file} 失败: {e}')

def main():
    """主函数"""
    print('=' * 60)
    print('📊 开始统计各section页面的卡片数量...')
    print('=' * 60)
    
    sections_dir = Path('sections')
    
    if not sections_dir.exists():
        print(f'❌ sections 目录不存在: {sections_dir}')
        return
    
    # 统计所有section文件的卡片数量
    card_counts = {}
    section_files = [
        'section-01.html',
        'section-02.html',
        'section-03.html',
        'section-04.html',
        'section-05.html',
        'section-06.html',
        'section-07.html',
        'section-99.html',
    ]
    
    print('\n📈 统计结果：')
    print('-' * 60)
    
    total_cards = 0
    for section_file in section_files:
        section_path = sections_dir / section_file
        section_key = section_file.replace('.html', '')
        
        if section_path.exists():
            count = count_cards_in_section(section_path)
            card_counts[section_key] = count
            total_cards += count
            print(f'  {section_file:<20} → {count:>3} 部')
        else:
            print(f'  {section_file:<20} → 文件不存在')
    
    print('-' * 60)
    print(f'  {"总计":<20} → {total_cards:>3} 部')
    print()
    
    # 更新index.html
    print('🔄 更新 index.html 中的徽章数字...')
    print('-' * 60)
    update_index_badges(card_counts)
    print('=' * 60)
    print('✨ 完成！')

if __name__ == '__main__':
    main()

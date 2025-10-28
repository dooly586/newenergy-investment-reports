"""
HTML 보고서의 현재 제목과 헤더 패턴 분석
"""
import os
from bs4 import BeautifulSoup

html_dir = os.path.dirname(os.path.abspath(__file__))
html_files = [f for f in os.listdir(html_dir) if f.endswith('.html') and f != 'index.html']
html_files.sort()

print('📊 현재 HTML 파일들의 제목 및 헤더 분석\n')
print('='*80)

for html_file in html_files:
    file_path = os.path.join(html_dir, html_file)

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        soup = BeautifulSoup(content, 'html.parser')

        # 제목 추출
        title_tag = soup.find('title')
        title = title_tag.text if title_tag else 'N/A'

        # H1 헤더 추출
        h1_tag = soup.find('h1')
        h1 = h1_tag.text if h1_tag else 'N/A'

        # 첫 번째 p 태그 (부제목) 추출
        p_tag = soup.find('p')
        subtitle = p_tag.text if p_tag else 'N/A'

        print(f'📄 파일: {html_file}')
        print(f'   <title>: {title}')
        print(f'   <h1>: {h1}')
        print(f'   <p> (subtitle): {subtitle}')
        print('-'*80)

print('\n✅ 분석 완료!')

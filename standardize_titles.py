"""
HTML 보고서의 제목과 헤더를 표준 형식으로 통일
"""
import os
import re
from datetime import datetime
from bs4 import BeautifulSoup

html_dir = os.path.dirname(os.path.abspath(__file__))
html_files = [f for f in os.listdir(html_dir) if f.endswith('.html') and f != 'index.html']
html_files.sort()

print('🔄 HTML 보고서 제목 표준화 시작...\n')

for html_file in html_files:
    file_path = os.path.join(html_dir, html_file)

    # 파일명에서 메타데이터 추출
    match = re.match(r'(\d{8})_(\d{6})_(.+)\.html', html_file)
    if not match:
        print(f'⚠️  건너뜀: {html_file} (파일명 패턴 불일치)')
        continue

    date_str = match.group(1)  # YYYYMMDD
    time_str = match.group(2)  # HHMMSS
    category = match.group(3)  # 카테고리

    # 날짜 포맷팅
    date_obj = datetime.strptime(date_str, '%Y%m%d')
    formatted_date = date_obj.strftime('%Y년 %m월 %d일')

    # 카테고리 한글화
    category_display = category.replace('_', ' ')

    # HTML 파일 읽기
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        soup = BeautifulSoup(content, 'html.parser')

    # 표준 제목 설정
    standard_title = f'뉴에너지 이온히팅 투자기업 분석 보고서 - {category_display}'
    standard_h1 = '🔥 뉴에너지 이온히팅 투자기업 분석 보고서'
    standard_subtitle = f'{category_display} | 분석일: {formatted_date}'

    # <title> 태그 업데이트
    title_tag = soup.find('title')
    if title_tag:
        old_title = title_tag.string
        title_tag.string = standard_title
        print(f'📄 {html_file}')
        print(f'   Title: "{old_title}" → "{standard_title}"')
    else:
        print(f'⚠️  {html_file}: <title> 태그 없음')

    # <h1> 태그 업데이트 (첫 번째 h1만)
    h1_tag = soup.find('h1')
    if h1_tag:
        old_h1 = h1_tag.get_text(strip=True)
        h1_tag.clear()
        h1_tag.append(standard_h1)
        print(f'   H1: "{old_h1}" → "{standard_h1}"')
    else:
        print(f'⚠️  {html_file}: <h1> 태그 없음')

    # 첫 번째 <p> 태그 업데이트 (부제목으로 간주)
    # header 내부의 p 태그 우선, 없으면 body의 첫 번째 p
    header = soup.find('div', class_='header')
    if header:
        p_tag = header.find('p')
    else:
        p_tag = soup.find('p')

    if p_tag:
        old_subtitle = p_tag.get_text(strip=True)
        p_tag.clear()
        p_tag.append(standard_subtitle)
        print(f'   Subtitle: "{old_subtitle}" → "{standard_subtitle}"')
    else:
        print(f'⚠️  {html_file}: 부제목 <p> 태그 없음')

    # 파일 저장
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    print('   ✅ 업데이트 완료\n')

print('✅ 모든 HTML 파일 제목 표준화 완료!')

"""
개별 HTML 보고서에서 "이미 분석 완료된 기업" 섹션 제거
"""
import os
from bs4 import BeautifulSoup

html_dir = os.path.dirname(os.path.abspath(__file__))
html_files = [f for f in os.listdir(html_dir) if f.endswith('.html') and f != 'index.html']

print('🧹 개별 HTML 보고서에서 제외 기업 섹션 제거 중...\n')

for html_file in html_files:
    file_path = os.path.join(html_dir, html_file)

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        soup = BeautifulSoup(content, 'html.parser')

    removed = False

    # 다양한 패턴으로 제외 기업 섹션 찾기
    # 1. "제외된 기업" 또는 "이미 분석 완료된 기업" 제목을 가진 섹션
    for heading in soup.find_all(['h2', 'h3', 'div']):
        text = heading.get_text(strip=True)
        if any(keyword in text for keyword in ['제외', '분석 완료', '이미 분석', 'Excluded', '제외 기업']):
            # 해당 섹션 전체 제거 (다음 h2까지 또는 부모 div)
            parent = heading.find_parent('div', class_='section')
            if parent:
                parent.decompose()
                removed = True
                print(f'   ✅ {html_file}: 섹션 제거 완료')
                break
            else:
                # section이 없으면 heading부터 다음 h2 전까지 제거
                next_sibling = heading.find_next_sibling()
                heading.decompose()
                while next_sibling and next_sibling.name not in ['h2', 'h3']:
                    temp = next_sibling.find_next_sibling()
                    next_sibling.decompose()
                    next_sibling = temp
                removed = True
                print(f'   ✅ {html_file}: 텍스트 제거 완료')
                break

    if removed:
        # 파일 저장
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
    else:
        print(f'   ℹ️  {html_file}: 제외 섹션 없음')

print('\n✅ 모든 HTML 파일 처리 완료!')

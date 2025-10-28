import os
import re
from bs4 import BeautifulSoup

html_dir = '.'
html_files = [f for f in os.listdir(html_dir) if f.endswith('.html') and f != 'index.html']

print('📊 각 HTML 파일의 회사 수 확인\n')

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
        soup = BeautifulSoup(content, 'html.parser')

        company_names = []

        # 패턴 1: h2 태그
        h2_tags = soup.find_all('h2')
        for h2 in h2_tags:
            text = h2.get_text(strip=True)
            company_match = re.match(r'\d+\.\s*(.+)', text)
            if company_match:
                company_name = company_match.group(1).strip()
                company_name = company_name.replace('🔗', '').strip()
                company_name = re.sub(r'\s*\([^)]*\)', '', company_name).strip()
                company_names.append(company_name)

        # 패턴 2: company-name 클래스
        if not company_names:
            company_name_divs = soup.find_all('div', class_='company-name')
            for div in company_name_divs:
                text = div.get_text(strip=True)
                company_match = re.match(r'\d+\.\s*([^\(]+)', text)
                if company_match:
                    company_name = company_match.group(1).strip()
                    company_names.append(company_name)

        print(f'{html_file}')
        print(f'  - 추출된 회사: {len(company_names)}개')
        if company_names:
            print(f'  - 회사 목록: {", ".join(company_names[:5])}{"..." if len(company_names) > 5 else ""}')
        print()

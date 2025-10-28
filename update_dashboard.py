"""
대시보드 업데이트 스크립트
- 개별 HTML 보고서 삭제 시
- 새 보고서 추가 시
이 스크립트를 실행하면 index.html이 최신 상태로 업데이트됩니다.
"""
import os
import re
from datetime import datetime
from bs4 import BeautifulSoup

print('🔄 대시보드 업데이트 시작...\n')

# HTML 파일 분석
html_dir = os.path.dirname(os.path.abspath(__file__))
html_files = [f for f in os.listdir(html_dir) if f.endswith('.html') and f != 'index.html']
html_files.sort(reverse=True)  # 최신순

reports = []

for html_file in html_files:
    file_path = os.path.join(html_dir, html_file)

    # 파일명에서 메타데이터 추출
    match = re.match(r'(\d{8})_(\d{6})_(.+)\.html', html_file)
    if match:
        date_str = match.group(1)
        time_str = match.group(2)
        category = match.group(3)

        date_obj = datetime.strptime(date_str, '%Y%m%d')
        time_obj = datetime.strptime(time_str, '%H%M%S')

        # HTML 파일에서 회사 수 추출
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            soup = BeautifulSoup(content, 'html.parser')

            # 회사 카드 수 세기
            company_cards = soup.find_all('div', class_='company-card')
            company_count = len(company_cards)

            # 타이틀 추출
            title_tag = soup.find('title')
            title = title_tag.text if title_tag else category

        reports.append({
            'filename': html_file,
            'date': date_obj.strftime('%Y년 %m월 %d일'),
            'time': time_obj.strftime('%H:%M:%S'),
            'category': category,
            'company_count': company_count,
            'title': title,
            'date_sort': date_str + time_str
        })

# 통계 계산
total_reports = len(reports)
total_companies_analyzed = sum(r['company_count'] for r in reports)

# 카테고리별 통계
categories = {}
for r in reports:
    cat = r['category']
    if cat not in categories:
        categories[cat] = {'count': 0, 'companies': 0}
    categories[cat]['count'] += 1
    categories[cat]['companies'] += r['company_count']

# HTML 생성
html_content = f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>뉴에너지 이온히팅 투자기업 분석 대시보드</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', 'Malgun Gothic', sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}

        .header {{
            background: rgba(255, 255, 255, 0.95);
            padding: 40px 20px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        .header h1 {{
            font-size: 2.5em;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
        }}

        .header p {{
            color: #666;
            font-size: 1.1em;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 40px 20px;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}

        .stat-card {{
            background: white;
            border-radius: 12px;
            padding: 30px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}

        .stat-card:hover {{
            transform: translateY(-5px);
        }}

        .stat-number {{
            font-size: 3em;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .stat-label {{
            font-size: 1.1em;
            color: #666;
            margin-top: 10px;
        }}

        .search-box {{
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        .search-input {{
            width: 100%;
            padding: 15px;
            font-size: 1.1em;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            transition: border-color 0.3s;
        }}

        .search-input:focus {{
            outline: none;
            border-color: #667eea;
        }}

        .reports-grid {{
            display: grid;
            gap: 20px;
        }}

        .report-card {{
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            border-left: 5px solid #667eea;
            display: grid;
            grid-template-columns: auto 1fr auto;
            gap: 20px;
            align-items: center;
        }}

        .report-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 15px rgba(0,0,0,0.15);
        }}

        .report-date {{
            text-align: center;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 8px;
            color: white;
            min-width: 120px;
        }}

        .report-date-day {{
            font-size: 2em;
            font-weight: 700;
        }}

        .report-date-month {{
            font-size: 0.9em;
            opacity: 0.9;
        }}

        .report-info {{
            flex: 1;
        }}

        .report-title {{
            font-size: 1.4em;
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 8px;
        }}

        .report-meta {{
            color: #666;
            font-size: 0.95em;
        }}

        .report-badge {{
            display: inline-block;
            padding: 5px 12px;
            background: #f0f0f0;
            border-radius: 15px;
            font-size: 0.85em;
            margin-right: 8px;
            margin-top: 8px;
        }}

        .report-action {{
            text-align: center;
        }}

        .btn-view {{
            display: inline-block;
            padding: 12px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 25px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        .btn-view:hover {{
            transform: scale(1.05);
            box-shadow: 0 6px 12px rgba(0,0,0,0.2);
        }}

        .no-results {{
            text-align: center;
            padding: 60px 20px;
            background: white;
            border-radius: 12px;
            color: #999;
            font-size: 1.2em;
        }}

        .footer {{
            text-align: center;
            padding: 30px 20px;
            color: white;
            margin-top: 40px;
        }}

        @media (max-width: 768px) {{
            .report-card {{
                grid-template-columns: 1fr;
                text-align: center;
            }}

            .report-date {{
                margin: 0 auto;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔥 뉴에너지 이온히팅 투자기업 분석 대시보드</h1>
        <p>모든 분석 보고서를 한눈에 확인하세요</p>
    </div>

    <div class="container">
        <!-- 통계 카드 -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{total_reports}</div>
                <div class="stat-label">📊 총 분석 보고서</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{total_companies_analyzed}</div>
                <div class="stat-label">🏢 분석된 기업</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(categories)}</div>
                <div class="stat-label">📁 분석 카테고리</div>
            </div>
        </div>

        <!-- 검색 박스 -->
        <div class="search-box">
            <input type="text" id="searchInput" class="search-input" placeholder="🔍 보고서 검색 (날짜, 카테고리, 회사명...)">
        </div>

        <!-- 보고서 목록 -->
        <div class="reports-grid" id="reportsList">
'''

# 각 보고서 카드 추가
for report in reports:
    date_parts = report['date'].split(' ')
    month_day = date_parts[1] + ' ' + date_parts[2]

    html_content += f'''
            <div class="report-card" data-search="{report['date']} {report['time']} {report['category']} {report['title']}">
                <div class="report-date">
                    <div class="report-date-month">{month_day}</div>
                    <div class="report-date-day">{report['time']}</div>
                </div>
                <div class="report-info">
                    <div class="report-title">{report['title']}</div>
                    <div class="report-meta">
                        📅 {report['date']} {report['time']}
                        <span class="report-badge">🏢 {report['company_count']}개 기업</span>
                        <span class="report-badge">📂 {report['category']}</span>
                    </div>
                </div>
                <div class="report-action">
                    <a href="{report['filename']}" class="btn-view" target="_blank">보고서 열기 →</a>
                </div>
            </div>
'''

html_content += f'''
        </div>

        <div class="no-results" id="noResults" style="display: none;">
            검색 결과가 없습니다.
        </div>
    </div>

    <div class="footer">
        <p><strong>뉴에너지(주) 이온히팅 시스템 투자 분석</strong></p>
        <p>마지막 업데이트: {datetime.now().strftime('%Y년 %m월 %d일 %H:%M')}</p>
    </div>

    <script>
        // 검색 기능
        const searchInput = document.getElementById('searchInput');
        const reportsList = document.getElementById('reportsList');
        const noResults = document.getElementById('noResults');

        searchInput.addEventListener('input', function() {{
            const searchTerm = this.value.toLowerCase();
            const reportCards = reportsList.querySelectorAll('.report-card');
            let visibleCount = 0;

            reportCards.forEach(card => {{
                const searchData = card.getAttribute('data-search').toLowerCase();
                if (searchData.includes(searchTerm)) {{
                    card.style.display = 'grid';
                    visibleCount++;
                }} else {{
                    card.style.display = 'none';
                }}
            }});

            if (visibleCount === 0) {{
                noResults.style.display = 'block';
                reportsList.style.display = 'none';
            }} else {{
                noResults.style.display = 'none';
                reportsList.style.display = 'grid';
            }}
        }});
    </script>
</body>
</html>
'''

# index.html 저장
index_path = os.path.join(html_dir, 'index.html')
with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print('✅ 대시보드 업데이트 완료!\n')
print(f'📊 총 {total_reports}개 보고서')
print(f'🏢 총 {total_companies_analyzed}개 기업 분석')
print(f'📁 {len(categories)}개 카테고리\n')

if total_reports == 0:
    print('⚠️  보고서가 없습니다. HTML 파일을 확인하세요.')
else:
    print('✨ index.html 파일을 브라우저에서 열어보세요!')

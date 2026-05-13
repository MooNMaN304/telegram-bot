from lxml import html
from pathlib import Path

fixture_path = Path('tests/html_parsing_tests/malibu_with_session.html')
html_str = fixture_path.read_text(encoding='utf-8')

tree = html.fromstring(html_str)

# Ищем элементы с временем
time_elems = tree.xpath('.//div[@class="seance-item__time"]')
print(f'Found {len(time_elems)} time elements')

for i, elem in enumerate(time_elems):
    text = elem.text_content().strip()
    print(f'Time {i+1}: {repr(text)}')


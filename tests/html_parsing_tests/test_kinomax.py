from pathlib import Path
from lxml import html


def test_extract_order_links_from_html():
    find_to_test = "//a[contains(@href, '/order/')]"

    html_file_path = Path(__file__).resolve().parent / "with_session.html"
    html_content = html_file_path.read_text(encoding="utf-8")

    tree = html.fromstring(html_content)
    nodes = tree.xpath(find_to_test)
    result = [node.get("href") for node in nodes]

    expected = [
        "/order/3552581",
        "/order/3552582",
        "/order/3552583",
        "/order/3552584",
        "/order/3552585",
    ]

    assert result == expected

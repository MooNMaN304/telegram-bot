import pytest
from src.parsing_movie.malibu_cinema.html_utils import extract_release_cards

def test_extract_release_cards_excludes_soon():
    html_content = """
    <div class="page">
        <div class="releases-list">
            <!-- Актуальный фильм -->
            <a class="releases-item ZTdEi" href="/release/24723?date=2026-05-12">
                <div class="releases-item-description__title">Актуальный фильм</div>
            </a>
            
            <!-- Фильм с классом soon -->
            <a class="releases-item ZTdEi releases-item_soon" href="/release/10075937?date=2026-06-01">
                <div class="releases-item-description__title">Скоро 1 (по классу)</div>
            </a>
        </div>

        <!-- Блок скоро будет -->
        <div id="releasesSoon">
            <div class="container releases-soon--title">Скоро в прокате</div>
            <div class="releases-list">
                <a class="releases-item ZTdEi" href="/release/99999?date=2026-07-01">
                    <div class="releases-item-description__title">Скоро 2 (в контейнере)</div>
                </a>
            </div>
        </div>
    </div>
    """
    
    movies = extract_release_cards(html_content)
    
    # Должен остаться только один фильм
    assert len(movies) == 1
    assert movies[0]["release_id"] == "24723"
    assert movies[0]["title"] == "Актуальный фильм"
    
    # Проверяем что "скоро" отфильтровались
    titles = [m["title"] for m in movies]
    assert "Скоро 1 (по классу)" not in titles
    assert "Скоро 2 (в контейнере)" not in titles

from urllib.parse import urlparse
import time
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def extract_release_id(url: str) -> int:
    """Извлекает ID релиза из URL"""
    path = urlparse(url).path
    release_id = path.split('/')[-1]
    return int(release_id)

path = chromedriver_autoinstaller.install()
service = Service(path)
driver = webdriver.Chrome(service=service)

try:
    # URL фильма для парсинга
    film_url = "https://malibu.wikicinema.ru/release/10066684?date=2025-11-16"
    driver.get(film_url)
    time.sleep(3)
    
    # Закрываем рекламу нажатием ESC
    actions = ActionChains(driver)
    actions.send_keys(Keys.ESCAPE)
    actions.perform()
    time.sleep(2)
    
    # Парсим описание (сюжет)
    description_selectors = [
            ".release__text span",
            ".release__text p",
            ".release__text div p span",
            ".release__text"
        ]
    description = ""
    for selector in description_selectors:
            try:
                desc_el = driver.find_element(By.CSS_SELECTOR, selector)
                text = desc_el.text.strip()
                if text:
                    description = text
            except Exception:
                continue
    
    # Парсим постер
    poster_url = ""
    try:
        poster_element = driver.find_element(By.CSS_SELECTOR, ".release-poster img")
        poster_url = poster_element.get_attribute('src')
    except Exception as e:
        print(f"Не удалось найти постер: {e}")
    
    # Парсим жанр
    genre = ""
    try:
        genre_element = driver.find_element(By.CSS_SELECTOR, ".main .release .release-container .release-right .release-description .release__genre")
        genre = genre_element.text.strip()
    except Exception as e:
        print(f"Не удалось найти жанр: {e}")
    # Название фильма
    title = ""
    try:
        title_element = driver.find_element(By.CSS_SELECTOR, ".release__title")
        title = title_element.text.strip()
    except Exception as e:
        print(f"Не удалось найти название фильма: {e}")

    
    # Выводим результаты
    print("=" * 60)
    print(f"ДЕТАЛЬНАЯ ИНФОРМАЦИЯ О ФИЛЬМЕ")
    print("=" * 60)
    print(f"Название: {title}")
    print(f"URL: {film_url}")
    print(f"ID: {extract_release_id(film_url)}")
    print(f"Жанр: {genre}")
    print(f"Постер: {poster_url}")
    print(f"Описание: {description}")
    print("=" * 60)
    
except Exception as e:
    print(f"Произошла ошибка: {e}")
    
finally:
    time.sleep(2)
    driver.quit()
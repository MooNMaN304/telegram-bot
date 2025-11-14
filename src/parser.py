import time
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

def form_url(id_movie: int, date: str = None) -> str:
    """Формирует URL для страницы фильма"""
    base_url = "https://malibu.wikicinema.ru"
    
    if date:
        return f"{base_url}/release/{id_movie}?date={date}"
    else:
        return f"{base_url}/release/{id_movie}"

# Настройка драйвера через chromedriver_autoinstaller
path = chromedriver_autoinstaller.install()
service = Service(path)
driver = webdriver.Chrome(service=service)

try:
    # Формируем URL через функцию
    url = form_url(id_movie=23878, date="2025-11-08")
    driver.get(url)
    time.sleep(2)
    
    # Закрываем рекламу нажатием ESC
    actions = ActionChains(driver)
    actions.send_keys(Keys.ESCAPE)
    actions.perform()
    
    print("Нажата клавиша ESC для закрытия рекламы")
    time.sleep(1)
    
    # Ищем расписание по указанной структуре классов
    schedule_lists = driver.find_elements(By.CSS_SELECTOR, ".release-schedule__list .release-schedule__item .release-schedule__items")
    
    print(f"Найдено блоков расписания: {len(schedule_lists)}")
    
    for i, schedule_block in enumerate(schedule_lists):
        # Ищем все сеансы в текущем блоке
        seances = schedule_block.find_elements(By.CSS_SELECTOR, ".seance-item")
        
        print(f"Блок {i+1}: найдено сеансов - {len(seances)}")
        
        for j, seance in enumerate(seances):
            # Ищем widget-overlay внутри сеанса и парсим ID сеанса
            widget_overlay = seance.find_element(By.CSS_SELECTOR, ".widget-overlay")
            seance_id = widget_overlay.get_attribute("data-seance-id")
            
            # Парсим время сеанса
            time_element = seance.find_element(By.CSS_SELECTOR, ".seance-item__time.text.text--size-18")
            seance_time = time_element.text
            
            # Парсим описание сеанса (формат и цена)
            description_element = seance.find_element(By.CSS_SELECTOR, "    ")
            
            # Получаем весь текст и разделяем на строки
            description_text = description_element.text.split('\n')
            
            # Первая строка - обычно формат (2D/3D), вторая - цена
            format_text = description_text[0] if len(description_text) > 0 else "Не указан"
            price = description_text[1] if len(description_text) > 1 else "Не указана"
            
            print(f"  Сеанс {j+1}:")
            print(f"    ID: {seance_id}")
            print(f"    Время: {seance_time}")
            print(f"    Формат: {format_text}")
            print(f"    Цена: {price}")
            print("    " + "-" * 40)
            
except Exception as e:
    print(f"Произошла ошибка: {e}")
    
finally:
    time.sleep(3)
    driver.quit()
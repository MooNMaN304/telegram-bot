from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_autoinstaller
import time

def capture_cinema_schedule(url, cinema_name):
    """
    Захватывает скриншот расписания киносеансов
    """
    # Настройка
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")

    driver_path = r"C:\path\to\chromedriver.exe"
    
    path = chromedriver_autoinstaller.install()
    service = Service(path)
    
    driver = webdriver.Chrome(
        service=service,
        options=chrome_options
    )
    
    try:
        print(f"Открываю {url}")
        driver.get(url)
        
        # Дать время для загрузки динамического контента
        time.sleep(5)
        
        # Если есть попапы или баннеры, их можно закрыть
        # try:
        #     close_button = driver.find_element(By.CLASS_NAME, "popup-close")
        #     close_button.click()
        # except:
        #     pass
        
        # Создаём имя файла с временной меткой
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cinema_schedule_{cinema_name}_{timestamp}.png"
        
        # Делаем скриншот
        driver.save_screenshot(filename)
        print(f"✓ Скриншот сохранён как: {filename}")
        
        return filename
        
    except Exception as e:
        print(f"✗ Ошибка: {e}")
        return None
        
    finally:
        driver.quit()

# Использование
if __name__ == "__main__":
    # Замените на реальный URL кинотеатра
    cinema_url = "https://example-cinema.ru/schedule"
    screenshot_file = capture_cinema_schedule("https://mc.yandex.ru/watch/16447975?wmode=7&page-url=https%3A%2F%2Fkinomax.ru%2Ffilms%2F8664&page-ref=https%3A%2F%2Fwww.google.com%2F&charset=utf-8&uah=chu%0A%22Microsoft%20Edge%22%3Bv%3D%22143%22%2C%22Chromium%22%3Bv%3D%22143%22%2C%22Not%20A(Brand%22%3Bv%3D%2224%22%0Achb%0A64%0Achf%0A143.0.3650.139%0Achl%0A%22Microsoft%20Edge%22%3Bv%3D%22143.0.3650.139%22%2C%22Chromium%22%3Bv%3D%22143.0.7499.193%22%2C%22Not%20A(Brand%22%3Bv%3D%2224.0.0.0%22%0Achm%0A%3F1%0Acho%0ANexus%205%0Achp%0AAndroid%0Achv%0A6.0&browser-info=pv%3A1%3Avf%3A6dxo56vtzxzyyn24rskrmvjm9re1r%3Afu%3A0%3Aen%3Autf-8%3Ala%3Aru%3Av%3A2331%3Acn%3A1%3Adp%3A0%3Als%3A932694852588%3Ahid%3A306068808%3Az%3A180%3Ai%3A20260111163925%3Aet%3A1768138765%3Ac%3A1%3Arn%3A941918367%3Arqn%3A207%3Au%3A1758730323182839532%3Aw%3A400x869%3As%3A400x869x24%3Ask%3A2%3Afp%3A140%3Awv%3A2%3Ads%3A0%2C0%2C66%2C5%2C2%2C0%2C%2C41%2C%2C%2C%2C%2C%3Aco%3A0%3Acpf%3A1%3Ans%3A1768138765193%3Aadb%3A1%3Afip%3A4594e2b65479a683ffd00fe4b481d5ee-1cc4db1a3d7b1837d6538ca6cabed338-a81f3b9bcdd80a361c14af38dc09b309-7950ec0297c12322859860922e071362-619e17dc65ef9d4673a29e983f6a4dc9-42778ac385fa614f58b5d810c258f9eb-f029f500589792a0d5a0f159f332406e-0d6774f2a2c6eaaf60b822b39830e68f-a81f3b9bcdd80a361c14af38dc09b309-36b0156d67e224248dccbff13c841137-7a502a49c3fd5ac8d1b845c2031ede1c%3Arqnl%3A1%3Ast%3A1768138765%3At%3A%D0%A0%D0%B0%D1%81%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5%20%D1%84%D0%B8%D0%BB%D1%8C%D0%BC%D0%B0%20%D0%A7%D0%B5%D0%B1%D1%83%D1%80%D0%B0%D1%88%D0%BA%D0%B0%202%20%D0%B2%20%D1%81%D0%B5%D1%82%D0%B8%20%D0%9A%D0%B8%D0%BD%D0%BE%D0%BC%D0%B0%D0%BA%D1%81&t=gdpr(14)clc(0-0-0)rqnt(1)aw(1)rcm(1)cdl(na)eco(84476420)fip(1)ti(1)", "KinoMax")
    
    if screenshot_file:
        print(f"Скриншот готов для отправки в GigaChat: {screenshot_file}")
        
        
"""
===============
#TODO notebook lm

# OOP
# Алгоритмы
# Чистая архитектура
# Rest api 

===============
"""   
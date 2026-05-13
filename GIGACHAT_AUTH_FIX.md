# 🔐 Ошибка GigaChat: Can't decode 'Authorization' header

## Проблема

```
ERROR: ResponseError: (URL('https://ngw.devices.sberbank.ru:9443/api/v2/oauth'), 400,
b'{"code":4,"message":"Can\'t decode \'Authorization\' header"}')
```

Это означает, что **credentials неправильно закодированы** для GigaChat API Sberbank.

---

## Причина

В `.env` файле вы имеете:

```
GIGACHAT_API_KEY=MDE5YjUxMzMtOGQ4Ni03NmJhLWJjOWEtMjM3Y2I5Zjk4NTRmOmE3Y2QyNjViLWFiZDMtNDE5MS04MjFiLTY3NWQ1MTA5YzA3NA==
```

Это уже **закодированное в Base64** значение!

Но в старом `settings.py` код делал повторное кодирование:

```python
# ❌ НЕПРАВИЛЬНО - кодирует уже закодированное значение!
auth_data = f"{self.GIGACHAT_API_KEY}:"
return base64.b64encode(auth_data.encode("utf-8")).decode("utf-8")
```

---

## Решение

✅ Обновлен `settings.py` с умным определением формата:

```python
@property
def GIGACHAT_CREDENTIALS(self) -> str:
    # Если уже выглядит как Base64 (заканчивается на ==), вернуть как есть
    if self.GIGACHAT_API_KEY.endswith("=="):
        return self.GIGACHAT_API_KEY

    # Иначе кодируем в Base64
    auth_data = f"{self.GIGACHAT_API_KEY}:"
    return base64.b64encode(auth_data.encode("utf-8")).decode("utf-8")
```

---

## Проверка

Запустите тестовый скрипт:

```bash
python test_gigachat_credentials.py
```

Вывод должен быть:

```
✓ Успешно декодировано из Base64:
Декодированное значение: [UUID]:[UUID]
✓ Правильный формат: UUID:UUID или KEY:PASSWORD
```

---

## Формат GIGACHAT_API_KEY

GigaChat API ожидает credentials в формате:

```
CLIENT_ID:CLIENT_SECRET
```

Когда это кодируется в Base64, получается примерно:

```
MDE5YjUxMzMtOGQ4Ni03NmJhLWJjOWEtMjM3Y2I5Zjk4NTRmOmE3Y2QyNjViLWFiZDMtNDE5MS04MjFiLTY3NWQ1MTA5YzA3NA==
```

---

## Логирование

Добавлено улучшенное логирование в `gigachat_request.py`:

- ✅ Логирует попытки загрузки изображений
- ✅ Логирует попытки запросов к AI
- ✅ **Специальный лог для ошибок авторизации** с подсказкой проверить `.env`
- ✅ Логирует полный контекст ошибок

Теперь при авторизационной ошибке увидите:

```
❌ ОШИБКА АВТОРИЗАЦИИ: Некорректные credentials для GigaChat
Проверьте GIGACHAT_API_KEY в .env файле
```

---

## Что дальше?

1. **Проверьте**, что GIGACHAT_API_KEY в `.env` имеет формат:
   - Либо `UUID:UUID` (будет закодирован автоматически)
   - Либо `[Base64_encoded_UUID:UUID]` с `==` в конце (будет использован как есть)

2. **Запустите тест**:

   ```bash
   python test_gigachat_credentials.py
   ```

3. **Запустите парсер** снова:
   ```bash
   python src/parsing_movie/kinomax_cinema/test_kinomax_flow.py
   ```

---

## Если всё ещё не работает?

Возможные причины:

1. **API ключ истёк** - получите новый из личного кабинета Sberbank
2. **Аккаунт заблокирован** - проверьте статус в Sberbank
3. **Интернет отключен** - проверьте соединение
4. **Proxy/брандмауэр блокирует** - попробуйте без VPN

Проверьте в логах точный ответ API и посетите документацию:
https://developers.sber.ru/docs/ru/gigachat

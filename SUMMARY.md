# 📋 Краткий итог: GigaChat API и отслеживание токенов

## 🎯 Ответы на ваши вопросы

### 1️⃣ Есть ли в response поля с информацией о токенах?

**✅ ДА!**

Каждый ответ от GigaChat API содержит объект `usage` с информацией о токенах:

```python
response = gigachat_client.chat({"messages": messages})
print(response.usage)  # <Usage object>
```

---

### 2️⃣ Какие поля есть для токенов?

**GigaChat использует следующие поля:**

```python
response.usage.prompt_tokens          # Входящие токены
response.usage.completion_tokens      # Выходящие токены
response.usage.total_tokens           # Всего
response.usage.precached_prompt_tokens  # Кэшированные (опционально)
```

**Внимание!** ⚠️ Названия полей отличаются от других API:

- ❌ **НЕ используется**: `input_tokens`, `output_tokens`
- ✅ **ИСПОЛЬЗУЕТСЯ**: `prompt_tokens`, `completion_tokens`

---

### 3️⃣ Как правильно извлечь информацию о токенах?

**Способ получения:**

```python
# Способ 1: Базовый
response = self.giga.chat({"messages": messages, "temperature": 0.2})
prompt = response.usage.prompt_tokens
completion = response.usage.completion_tokens
total = response.usage.total_tokens

# Способ 2: С логированием
logger.info(
    f"Tokens used - Prompt: {response.usage.prompt_tokens}, "
    f"Completion: {response.usage.completion_tokens}, "
    f"Total: {response.usage.total_tokens}"
)

# Способ 3: С проверкой наличия
if response.usage:
    total = response.usage.total_tokens
    if response.usage.precached_prompt_tokens:
        print(f"Cached: {response.usage.precached_prompt_tokens}")
```

---

## 📊 Полная структура Response Object

```
ChatCompletion
├── object: "chat.completion"
├── created: 1716284400 (timestamp)
├── model: "GigaChat"
├── choices: [Choices]
│   └── [0]
│       ├── message.content: "Ваш ответ..."
│       ├── finish_reason: "stop"
│       └── index: 0
│
├── usage: Usage  ⭐ ВСЕ ТОКЕНЫ ЗДЕСЬ
│   ├── prompt_tokens: 125
│   ├── completion_tokens: 87
│   ├── total_tokens: 212
│   └── precached_prompt_tokens: null (опционально)
│
├── thread_id: "..." (опционально)
├── message_id: "..." (опционально)
└── x_headers: {...} (опционально)
```

---

## 🔍 Типы и схемы

### Usage (объект со статистикой)

| Поле                      | Тип             | Описание                       |
| ------------------------- | --------------- | ------------------------------ |
| `prompt_tokens`           | `int`           | Входящие токены (вопрос)       |
| `completion_tokens`       | `int`           | Выходящие токены (ответ)       |
| `total_tokens`            | `int`           | Сумма (prompt + completion)    |
| `precached_prompt_tokens` | `Optional[int]` | Кэшированные (может быть None) |

### ChatCompletion (полный объект ответа)

| Поле         | Тип              | Описание                 |
| ------------ | ---------------- | ------------------------ |
| `choices`    | `List[Choices]`  | Массив ответов           |
| `created`    | `int`            | Timestamp создания       |
| `model`      | `str`            | Название модели          |
| `usage`      | `Usage`          | Статистика токенов       |
| `object`     | `str`            | Тип объекта              |
| `thread_id`  | `Optional[str]`  | ID потока                |
| `message_id` | `Optional[str]`  | ID сообщения             |
| `x_headers`  | `Optional[Dict]` | Дополнительные заголовки |

---

## 📁 Созданные файлы в проекте

### 📚 Документация

1. **[GIGACHAT_TOKEN_USAGE.md](GIGACHAT_TOKEN_USAGE.md)**
   - Полная документация по структуре и методам
   - Примеры использования
   - Справочная информация

2. **[GIGACHAT_TOKENS_QUICK_REFERENCE.md](GIGACHAT_TOKENS_QUICK_REFERENCE.md)**
   - Быстрая справка
   - Копипаст-код
   - FAQ

3. **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)**
   - Три подхода к интеграции в проект
   - Пошаговые инструкции
   - Чек-листы

### 💻 Код

1. **[analyze_gigachat_tokens.py](analyze_gigachat_tokens.py)**
   - Анализ структуры API
   - Вывод всех полей объектов

2. **[src/utils/gigachat_request_enhanced.py](src/utils/gigachat_request_enhanced.py)**
   - Улучшенная версия парсера
   - Встроенное отслеживание токенов
   - Методы для получения статистики

3. **[examples_token_tracking.py](examples_token_tracking.py)**
   - 4 практических примера
   - Класс TokenTracker
   - Различные способы отслеживания

---

## 🚀 Быстрый старт (5 минут)

### Шаг 1: Добавить логирование

Отредактируйте файл [src/utils/gigachat_request.py](src/utils/gigachat_request.py):

```python
response = self.giga.chat({"messages": messages, "temperature": self.temperature})

# Добавить эту строку:
logger.info(f"Tokens: prompt={response.usage.prompt_tokens}, "
            f"completion={response.usage.completion_tokens}, "
            f"total={response.usage.total_tokens}")

content = response.choices[0].message.content.strip()
```

### Шаг 2: Готово!

Теперь в логах видна информация о токенах.

---

## 💡 Практические примеры

### Пример 1: Получить количество токенов

```python
response = parser.giga.chat({"messages": messages})
total_tokens = response.usage.total_tokens
print(f"Использовано {total_tokens} токенов")
```

### Пример 2: Отслеживать статистику

```python
stats = {
    "requests": 0,
    "total_tokens": 0,
}

response = parser.giga.chat({"messages": messages})
stats["requests"] += 1
stats["total_tokens"] += response.usage.total_tokens

print(f"Avg: {stats['total_tokens'] / stats['requests']}")
```

### Пример 3: Экспортировать в логи

```python
import json

log_entry = {
    "event": "gigachat_api",
    "prompt_tokens": response.usage.prompt_tokens,
    "completion_tokens": response.usage.completion_tokens,
    "total_tokens": response.usage.total_tokens,
}

logger.info(json.dumps(log_entry))
```

---

## ❓ FAQ

**Q: Почему используются `prompt_tokens` вместо `input_tokens`?**
A: Это стандарт для GigaChat API. Другие API (OpenAI) используют другие названия.

**Q: Может ли precached_prompt_tokens быть None?**
A: Да, это опциональное поле. Всегда проверяйте перед использованием.

**Q: Нужно ли делать отдельный запрос для получения статистики?**
A: Нет, токены приходят в каждом response автоматически.

**Q: Как использовать эту информацию для оптимизации?**
A: Отслеживайте total_tokens, анализируйте распределение prompt/completion, оптимизируйте промпты.

**Q: Где найти примеры в проекте?**
A: [examples_token_tracking.py](examples_token_tracking.py) содержит 4 полных примера.

---

## 🎓 Дополнительные ресурсы в проекте

| Файл                                                                             | Описание                 | Сложность |
| -------------------------------------------------------------------------------- | ------------------------ | --------- |
| [GIGACHAT_TOKENS_QUICK_REFERENCE.md](GIGACHAT_TOKENS_QUICK_REFERENCE.md)         | Быстрая справка          | ⭐        |
| [GIGACHAT_TOKEN_USAGE.md](GIGACHAT_TOKEN_USAGE.md)                               | Полная документация      | ⭐⭐      |
| [examples_token_tracking.py](examples_token_tracking.py)                         | Примеры кода             | ⭐⭐      |
| [src/utils/gigachat_request_enhanced.py](src/utils/gigachat_request_enhanced.py) | Готовая реализация       | ⭐⭐⭐    |
| [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)                                     | Инструкции по интеграции | ⭐⭐⭐    |

---

## ✅ Чек-лист

- [x] Найдена структура response объекта
- [x] Определены все поля для отслеживания токенов
- [x] Создана полная документация
- [x] Написаны примеры кода
- [x] Подготовлена улучшенная версия парсера
- [x] Создано руководство по интеграции

---

## 🎯 Следующие шаги

1. **Экспресс-интеграция (5 мин)**: Добавьте одну строку логирования в `gigachat_request.py`
2. **Полная интеграция (15 мин)**: Используйте `gigachat_request_enhanced.py`
3. **Аналитика (30 мин)**: Добавьте TokenTracker для накопления статистики

---

**Создано:** 26 апреля 2026 г.
**Версия:** 1.0
**Статус:** ✅ Полная документация и примеры

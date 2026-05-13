.PHONY: help parsing test lint format clean-imports check install

PYTHON = python
SRC = src
TESTS = tests

help:
	@echo "Команды:"
	@echo "  make parsing         — запустить парсинг"
	@echo "  make test            — тесты"
	@echo "  make lint            — безопасный линтинг (без удаления импортов)"
	@echo "  make format          — форматирование кода"
	@echo "  make clean-imports   — удалить неиспользуемые импорты (ОСТОРОЖНО)"
	@echo "  make check           — format + lint + test"
	@echo "  make install         — установка зависимостей"

parsing:
	$(PYTHON) -m src.cli.run_parsing

test:
	PYTHONPATH=. pytest -v $(TESTS)

lint:
	ruff check $(SRC) --exit-zero

format:
	ruff format $(SRC) 

clean-imports:
	ruff check $(SRC) --select F401 --fix

check: format lint test

install:
	pip install -r requirements.txt

run_local_parsers:
	$(PYTHON) -m src.parsing_movie.celery

run_malibu_local:
	$(PYTHON) src/cli/run_malibu_parser.py

run_kinomax_local:
	$(PYTHON) src/cli/run_kinomax_parser.py
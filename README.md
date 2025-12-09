Лабораторная работа 3 часть 1
===

# Пререквизиты
Давайте создадим какую-нибудь минимальную кодовую базу и будем работать с ней.
Допустим, cli, занимающийся выводом погоды в консоль.
К этому проекту пристягнем pyproject.toml и requirements.txt, создав пакет.

## Файлы проекта

<details>
<summary>cli.py</summary>

```py
import argparse
from core import format_weather


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="weather-cli",
        description="Simple weather formatting CLI",
    )
    parser.add_argument(
        "city",
        help="City name",
    )
    parser.add_argument(
        "--temp",
        type=float,
        required=True,
        help="Temperature in Celsius",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    message = format_weather(args.city, args.temp)
    print(message)


if __name__ == "__main__":
    main()

```

</details>

<details>
<summary>core.py</summary>

```py
def c_to_f(celsius: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return celsius * 9.0 / 5.0 + 32.0


def f_to_c(fahrenheit: float) -> float:
    """Convert Fahrenheit to Celsius."""
    return (fahrenheit - 32.0) * 5.0 / 9.0


def format_weather(city: str, temp_c: float) -> str:
    """Return formatted weather string in both C and F."""
    temp_f = c_to_f(temp_c)
    return f"Weather in {city}: {temp_c:.1f} °C / {temp_f:.1f} °F"
```

</details>

## Тесты

<details>
<summary>test_cli.py</summary>

```py
import sys
import subprocess
from pathlib import Path


def test_cli_runs_and_prints_output():
    project_root = Path(__file__).resolve().parents[1]
    cli_path = project_root / "cli.py"

    result = subprocess.run(
        [sys.executable, str(cli_path), "Moscow", "--temp", "15"],
        capture_output=True,
        text=True,
        check=True,
    )

    assert result.returncode == 0
    assert "Moscow" in result.stdout
    assert "15.0" in result.stdout
```

</details>

<details>
<summary>test_core.py</summary>

```py
from ..core import c_to_f, f_to_c, format_weather


def test_c_to_f_and_back():
    c = 0.0
    f = c_to_f(c)
    assert abs(f - 32.0) < 1e-6
    c_back = f_to_c(f)
    assert abs(c_back - c) < 1e-6


def test_format_weather_contains_city_and_values():
    msg = format_weather("Moscow", 20.0)
    assert "Moscow" in msg
    assert "20.0" in msg
    assert "°C" in msg
    assert "°F" in msg

```

</details>

## Сторонние файлы

<details>
<summary>pyproject.toml</summary>

```toml
[build-system]
requires = ["setuptools>=61", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "weather-cli"
version = "0.1.0"
description = "Simple CLI tool for temperature conversion and weather formatting"
authors = [
  { name = "Me", email = "me@me.me" }
]
readme = "README.md"
requires-python = ">=3.10"
dependencies = []

[project.optional-dependencies]
dev = ["pytest"]

[project.scripts]
weather-cli = "weather_cli.cli:main"

[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]
```

</details>

В `requirements.txt` просто кладем `pytest`.

## CI/CD, также известные как Worflows
Для реализации CI/CD, мы используем GitHub Actions. GitHub Actions позволяет автоматизировать процессы сборки, тестирования и развертывания приложений. Мы создаем файлы workflow в директории `.github/workflows`, где каждый файл описывает один или несколько процессов.

### Плохие практики для GitHub Actions:
 - Хардкод секретов и доступов прямо в yaml или в командах, отсутствие secrets и permissions по принципу наименьших прав.
 - Одна огромная джоба без разделения на стадии (build/test/deploy), без матриц, без needs, что делает pipeline медленным и плохо читаемым.
 - Отсутствие кеширования зависимостей и повторная установка всего при каждом запуске, что сильно увеличивает время CI.
 - Запуск workflow на любые пуши в любую ветку (включая main) без ограничений по веткам/папкам и без обязательного прохождения тестов перед деплоем.
 - Широкие права токена (GITHUB_TOKEN по умолчанию без ограничения permissions) и запуск недоверенного кода с кешированием, что повышает риск атак.
### Хорошие практики:
 - Использовать secrets и environment (с review для prod), никогда не хардкодить ключи.
 - Разделять pipeline на логичные шаги и джобы (build/test/deploy), использовать needs, матрицы и условные триггеры.
 - Кешировать зависимости для ускорения.
 - Ограничить GITHUB_TOKEN через permissions, не давать лишних прав, особенно на запись и управление репозиторием.
 - Явно задавать ветки/пути в on: (например, только main для deploy, pull_request для тестов).

## Реализация плохого файла
<details>
<summary>bad-ci.yml</summary>

```yaml
name: Bad CI/CD

on: [push]

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Install Python and deps
        run: |
          sudo apt-get update
          sudo apt-get install -y python3 python3-pip
          pip3 install -r requirements.txt pytest build

      - name: Run tests
        run: pytest

      - name: Build package
        run: python3 -m build

      - name: Deploy to production
        run: |
          export SSH_KEY="-----BEGIN PRIVATE KEY-----I_AM_A_FAKE_KEY-----END PRIVATE KEY-----"
          echo "$SSH_KEY" > key.pem
          chmod 600 key.pem
          scp -i key.pem -o StrictHostKeyChecking=no dist/*.whl user@example.com:/var/www/weather-cli/
```
</details>

## Реализация хорошего файла

<details>
<summary>good-ci.yml</summary>

```yaml
name: CI/CD

on:
  push:
    branches: [main]
    paths:
      - "src/**"
      - "tests/**"
      - "pyproject.toml"
      - "requirements.txt"
      - ".github/workflows/**"
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  tests:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Cache pip
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install build

      - name: Run tests
        run: pytest

  deploy:
    needs: tests
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    environment:
      name: production
      url: https://example.com
    permissions:
      contents: read

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install build tool
        run: |
          python -m pip install --upgrade pip
          pip install build

      - name: Build package
        run: python -m build

      - name: Deploy to production
        env:
          SSH_KEY: ${{ secrets.DEPLOY_SSH_KEY }}
        run: |
          echo "$SSH_KEY" > key.pem
          chmod 600 key.pem
          scp -i key.pem -o StrictHostKeyChecking=no dist/*.whl user@example.com:/var/www/weather-cli/
```

</details>


# Итог
В данной лабораторной работе мы изучили процесс создания и настройки CI/CD-конвейера для Python-проекта с использованием GitHub Actions. Мы создали два файла конфигурации: плохой и хороший, и проанализировали их различия. Мы также разработали скрипт для автоматической сборки и развертывания проекта на сервере.

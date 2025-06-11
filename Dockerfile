# 1. Берём официальный облегчённый образ Python 3.12
FROM python:3.12-slim

# 2. Обновляем apt и ставим gcc + необходимые инструменты для сборки C-расширений
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
    && rm -rf /var/lib/apt/lists/*

# 3. Переключаемся в рабочую директорию /app
WORKDIR /app

# 4. Чтобы Python не буферизовал вывод (логи сразу в stdout)
ENV PYTHONUNBUFFERED=1

# 5. Копируем только requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Копируем остальные файлы проекта
COPY . .

# 7. (Опционально) Открываем порт, если нужно
# EXPOSE 8000

# 8. По-умолчанию запускаем бота
CMD ["python", "bot.py"]
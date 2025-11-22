# 1. Базовый образ
FROM python:3.10-slim

# 2. Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app



# 4. Копируем файл с зависимостями и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Копируем весь остальной код проекта в контейнер
COPY . .

# 6. Открываем порт, на котором будет работать uvicorn
EXPOSE 8000

# 7. Команда по умолчанию
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
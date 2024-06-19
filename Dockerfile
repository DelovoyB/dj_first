# Используем официальный образ Python
FROM python:latest

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем все файлы из текущей директории в директорию /app внутри контейнера
COPY . /app

# Устанавливаем зависимости из requirements.txt, если он существует
RUN pip install --no-cache-dir -r requirements.txt

# Команда по умолчанию для выполнения Python-скриптов
CMD ["python"]

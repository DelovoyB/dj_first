FROM python:3.12.4

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["waitress-serve", "--host=0.0.0.0", "--port=8000", "dj.wsgi:application"]

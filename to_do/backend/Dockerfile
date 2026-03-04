FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x app/prestart.sh

ENTRYPOINT ["./app/prestart.sh"]
CMD ["fastapi", "run", "app/main.py", "--port", "8000"]
FROM python:3.12-slim

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x prestart.sh

EXPOSE 8000

ENTRYPOINT ["./prestart.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
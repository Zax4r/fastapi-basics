FROM python:3.12-slim

WORKDIR /app

COPY requirements_frontend.txt .

RUN pip install --no-cache-dir -r requirements_frontend.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "frontend.py"]

    
FROM python:3.9-slim

WORKDIR /app

COPY supabase_exporter.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "supabase_exporter.py"]
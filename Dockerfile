FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY sample_logs ./sample_logs
COPY README.md .

RUN mkdir -p archive reports

ENV PYTHONPATH=/app/src

CMD ["python", "-m", "ecu_log_tool.cli", "analyze", "sample_logs/brc_valid_log.csv"]
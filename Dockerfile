FROM python:3.12-slim

WORKDIR /app

RUN python3 -m venv /opt/venv

COPY . .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    chmod +x entrypoint.sh 

EXPOSE 8000

CMD ["/app/entrypoint.sh"]

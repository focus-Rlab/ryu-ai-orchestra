FROM python:3.12-slim

WORKDIR /app
COPY gateway_service/requirements.txt /app/gateway_service/requirements.txt
RUN pip install --no-cache-dir -r /app/gateway_service/requirements.txt
COPY v1_core /app/v1_core
COPY gateway_service /app/gateway_service
RUN useradd --create-home raphael && mkdir -p /data && chown raphael:raphael /data
USER raphael
ENV RAPHAEL_DATA_DIR=/data
CMD ["uvicorn", "gateway_service.app:app", "--host", "0.0.0.0", "--port", "8000"]

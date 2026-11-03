# Image dasar Red Hat Universal Base Image (UBI 9) untuk Python 3.11.
# File ini dapat dibangun oleh Docker maupun Podman:
#   docker build -t 1money .
#   podman build -t 1money .
FROM registry.access.redhat.com/ubi9/python-311

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DB_PATH=/data/kas.db \
    APP_VERSION=1.0.0

WORKDIR /opt/app-root/src

# Siapkan folder data (volume) agar bisa ditulis user non-root (UID 1001)
USER 0
RUN mkdir -p /data && chown 1001:0 /data && chmod g=u /data
USER 1001

# Salin requirements dulu supaya layer dependensi ter-cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY templates ./templates

VOLUME ["/data"]
EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "app:create_app()"]

# 1Money

Aplikasi web pencatatan kas organisasi mahasiswa (Flask + SQLite) untuk studi kasus UTS
Pengembangan dan Operasi: deployment berbasis container (Docker/Podman) dengan CI/CD GitHub Actions.

## Jalankan lokal (tanpa container)
```bash
pip install -r requirements-dev.txt
pytest
python app.py          # http://localhost:8000
```

## Jalankan dengan container
```bash
# Docker
docker build -t 1money .
docker run -d --name 1money -p 8080:8000 -v 1money-data:/data 1money

# Podman
podman build -t 1money .
podman run -d --name 1money -p 8080:8000 -v 1money-data:/data:Z 1money

# Compose
docker compose up -d --build
```
Buka http://localhost:8080 — cek kesehatan: http://localhost:8080/health

## CI/CD
Workflow: `.github/workflows/ci-cd.yml` (test -> build -> publish ke GHCR -> deploy Podman).
Panduan lengkap ada pada dokumen panduan kelompok.

## Endpoint
| Method | Path | Fungsi |
|---|---|---|
| GET | `/` | Halaman utama |
| POST | `/tambah` | Tambah transaksi |
| POST | `/hapus/<id>` | Hapus transaksi |
| GET | `/health` | Health check |
| GET | `/api/saldo` | Saldo (JSON) |
| GET | `/api/transaksi` | Daftar transaksi (JSON) |

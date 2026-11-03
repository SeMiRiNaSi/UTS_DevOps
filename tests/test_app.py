import pytest

from app import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app(db_path=str(tmp_path / "test.db"))
    app.config["TESTING"] = True
    return app.test_client()


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"


def test_saldo_awal_nol(client):
    assert client.get("/api/saldo").get_json()["saldo"] == 0


def test_tambah_dan_saldo(client):
    client.post("/tambah", data={"jenis": "masuk", "keterangan": "Iuran", "jumlah": "50000"})
    client.post("/tambah", data={"jenis": "keluar", "keterangan": "Print", "jumlah": "15000"})
    assert client.get("/api/saldo").get_json()["saldo"] == 35000
    assert len(client.get("/api/transaksi").get_json()) == 2


def test_input_tidak_valid_ditolak(client):
    client.post("/tambah", data={"jenis": "masuk", "keterangan": "", "jumlah": "1000"})
    client.post("/tambah", data={"jenis": "lain", "keterangan": "x", "jumlah": "1000"})
    client.post("/tambah", data={"jenis": "masuk", "keterangan": "x", "jumlah": "-5"})
    assert client.get("/api/transaksi").get_json() == []


def test_hapus(client):
    client.post("/tambah", data={"jenis": "masuk", "keterangan": "Iuran", "jumlah": "1000"})
    trx_id = client.get("/api/transaksi").get_json()[0]["id"]
    client.post(f"/hapus/{trx_id}")
    assert client.get("/api/transaksi").get_json() == []


def test_halaman_utama(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"1Money" in res.data

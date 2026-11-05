import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_home_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "E-LKS Kehati" in response.text
    assert "Problem Based Learning" in response.text
    assert "Fase 1: Orientasi Masalah" in response.text

def test_admin_page():
    response = client.get("/admin")
    assert response.status_code == 200
    assert "Panel Guru" in response.text or "admin" in response.text.lower()

def test_api_kirim_and_rekap():
    payload = {
        "nama": "Kelompok Uji",
        "kelas": "X-1",
        "absen": "01",
        "sekolah": "MAN Lombok Barat",
        "tanggal": "2026-11-04",
        "total": 85,
        "predikat": "Sangat Baik"
    }
    post_res = client.post("/api/kirim", json=payload)
    assert post_res.status_code == 200
    data = post_res.json()
    assert data.get("ok") is True

    # Test rekap endpoint without auth (should fail with 401)
    rekap_res = client.get("/api/rekap")
    assert rekap_res.status_code == 401

def test_login_logout():
    # Login with invalid credentials
    bad_login = client.post("/api/login", json={"pengguna": "wrong", "sandi": "bad"})
    assert bad_login.status_code == 401

    # Login with default admin credentials
    good_login = client.post("/api/login", json={"pengguna": "admin", "sandi": "guru123"})
    assert good_login.status_code == 200
    assert good_login.json().get("ok") is True

    # Now access rekap with session cookie
    rekap_res = client.get("/api/rekap")
    assert rekap_res.status_code == 200
    rekap_data = rekap_res.json()
    assert rekap_data.get("ok") is True
    assert isinstance(rekap_data.get("rows"), list)
    assert any(item["nama"] == "Kelompok Uji" for item in rekap_data["rows"])

    # Test CSV export format
    csv_res = client.get("/api/rekap?format=csv")
    assert csv_res.status_code == 200
    assert "Kelompok Uji" in csv_res.text

    # Logout
    logout_res = client.post("/api/logout")
    assert logout_res.status_code == 200

    # Rekap should be 401 after logout
    rekap_after = client.get("/api/rekap")
    assert rekap_after.status_code == 401

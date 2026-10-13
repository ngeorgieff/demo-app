from fastapi.testclient import TestClient

from app import main

client = TestClient(main.app)


def test_root():
    r = client.get("/")
    assert r.status_code == 200
    body = r.json()
    assert set(body) == {"name", "version", "environment", "status"}
    assert body["status"] == "ok"


def test_healthz():
    r = client.get("/healthz")
    assert r.status_code == 200 and r.json() == {"status": "healthy"}


def test_readyz_ready_then_draining():
    assert client.get("/readyz").status_code == 200
    main._ready = False
    try:
        assert client.get("/readyz").status_code == 503
    finally:
        main._ready = True


def test_version_has_build_info():
    body = client.get("/version").json()
    assert set(body) == {"version", "git_sha", "build_time"}

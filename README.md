# demo-app

Minimal FastAPI service used to exercise the Argo CD pipeline. Endpoints: `/`, `/healthz`, `/readyz`, `/version`.

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt -r requirements-dev.txt
.venv/bin/python -m pytest -q
docker build --build-arg APP_VERSION=$(cat VERSION) -t demo-app:local .
```

Configuration (env): `APP_NAME`, `APP_ENV`, `APP_VERSION`, `GIT_SHA`, `BUILD_TIME`. Runs as UID 10001 on 8080, works with a read-only root filesystem.
CI (`.github/workflows/ci.yml`) publishes `ghcr.io/ngeorgieff/demo-app` and commits the digest to `ngeorgieff/k3s-gitops`. Deployment config lives there.

## Docker run

### Linux (proxy with host network)

```bash
docker compose up --build
```

- `proxy` runs with `network_mode: host` (required by SOME/IP multicast).
- `desktop` is available at `http://localhost:8080`.
- Proxy API is available at `http://localhost:5000`.

### Windows (Docker Desktop fallback)

```powershell
docker compose -f docker-compose.windows.yml up --build
```

- Host network mode is not reliably supported by Docker Desktop.
- This fallback exposes proxy on `localhost:5000` via port mapping.
- Desktop is available at `http://localhost:8080`.

### Stop

```bash
docker compose down
```

or for Windows fallback:

```powershell
docker compose -f docker-compose.windows.yml down
```

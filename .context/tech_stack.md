# Tech Stack – Discord Role Master 3000

> Alle Versionen sind verbindlich. Abweichungen nur nach expliziter Absprache und Update dieser Datei.

---

## Backend (Python)

| Paket | Version | Zweck |
|---|---|---|
| Python | **3.12** | Laufzeitumgebung |
| FastAPI | **0.110+** | Web-Framework, Auto-OpenAPI |
| uvicorn | **0.29+** | ASGI-Server (`uvicorn[standard]`) |
| discord.py | **2.3+** | Discord Bot Client |
| SQLAlchemy | **2.0+** | ORM (async) |
| aiosqlite | **0.20+** | Async SQLite-Treiber |
| pydantic | **2.x** | Validierung & Schemas |
| pydantic-settings | **2.x** | Settings aus `.env` |
| alembic | **1.13+** | DB-Migrationen (ab Schritt 3) |
| pytest | **8.x** | Testing |
| pytest-asyncio | **0.23+** | Async-Tests |

**Dev-Tools:**
- `ruff` – Linter + Formatter (ersetzt flake8 + black)
- `mypy` – statische Typprüfung

---

## Frontend (JavaScript)

| Paket | Version | Zweck |
|---|---|---|
| Node.js | **20 LTS** | Laufzeitumgebung |
| Vue | **3.4+** | UI-Framework (Composition API) |
| Vite | **5.x** | Build-Tool + Dev-Server |
| Pinia | **2.x** | State Management |
| Vue Router | **4.x** | Client-seitiges Routing |
| Vue Flow | **1.x** | Hierarchie-Bäume / Node-Graphen |
| Axios | **1.x** | HTTP-Client |
| PrimeVue | **4.x** | UI-Komponenten (alternativ: Naive UI 2.x) |

---

## Datenbank

| Umgebung | Technologie | Verbindungsstring |
|---|---|---|
| Development | SQLite 3.x | `sqlite+aiosqlite:///./discord_rm.db` |
| Production | PostgreSQL 16 | `postgresql+asyncpg://user:pass@db:5432/discord_rm` |

---

## Infrastruktur (ab Schritt 3)

| Tool | Version | Zweck |
|---|---|---|
| Docker | 25+ | Container |
| Docker Compose | 2.x | Orchestrierung (dev + prod) |
| Nginx | 1.25+ | Frontend-Serving + Reverse Proxy |

---

## Entwicklungsumgebung Setup

```bash
# Backend
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r backend/requirements.txt

# Frontend
cd frontend
npm install
npm run dev

# Backend starten
uvicorn backend.main:app --reload --port 8000
```

**Ports:**

| Dienst | Port |
|---|---|
| FastAPI Backend | `8000` |
| Swagger UI | `8000/docs` |
| Vue Dev-Server | `5173` |

---

*Letzte Aktualisierung: 2026-02-19*

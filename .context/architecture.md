# Architektur – Discord Role Master 3000

---

## Systemübersicht

```
┌─────────────────────────────────────────────────────────────────┐
│                        Browser (User)                           │
│   ┌──────────────────────────────────────────────────────────┐  │
│   │                  Vue 3 Frontend (Vite)                   │  │
│   │   RolesView     │  CategoriesView   │   ChannelsView     │  │
│   │   (Vue Flow)    │   (Vue Flow)      │   (Table)          │  │
│   │                      Pinia Store                         │  │
│   └──────────────────────────┬───────────────────────────────┘  │
└──────────────────────────────│──────────────────────────────────┘
                               │ REST / HTTP JSON
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                  FastAPI Backend (Python)                        │
│                                                                 │
│   Routers          Services              Bot                    │
│   /api/guild   →   –                    discord.py Client      │
│   /api/roles   →   PermissionCalc   ←   on_ready               │
│   /api/cats    →   SyncService      ←   on_guild_role_update    │
│   /api/chans   →   –                ←   on_guild_channel_*      │
│   /api/sync    →   SyncService                                  │
│                                                                 │
│   ┌──────────────────────────────────────────────────────────┐  │
│   │          SQLAlchemy ORM (async)  – Repositories          │  │
│   └──────────────────────────┬───────────────────────────────┘  │
│                              │                                  │
│                       SQLite (Dev)                              │
│                       PostgreSQL (Prod)                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## Schichten-Modell (Backend)

```
HTTP Request
    ↓
Router          – HTTP-Handler, Pydantic-Schemas, kein Business-Code
    ↓
Service         – Business-Logik, kennt kein HTTP
    ↓
Repository      – Alle DB-Queries (einziger Ort für ORM-Code)
    ↓
Model           – SQLAlchemy-Tabellendefinitionen
```

**Verboten zwischen Schichten:**
- Router ruft Repository direkt auf
- Service importiert FastAPI-Typen (`Request`, `Response`)
- Model enthält Business-Logik

---

## Schichten-Modell (Frontend)

```
View            – orchestriert Store, Composables, Components
    ├── Pinia Store     – globaler State + Actions (ruft src/api/ auf)
    ├── Composable      – lokale, wiederverwendbare Logik (use*.js)
    └── Component       – reine UI, kein direkter API-Aufruf, kein axios
```

**Verboten:**
- Pinia-Store mit `fetch()` direkt (→ muss über `src/api/`)
- Vue-Komponente importiert `axios`
- View enthält Business-Logik (→ Composable)

---

## Ordnerstruktur

```
backend/
├── main.py              # App-Factory, Router-Einbindung, Startup-Events
├── config.py            # Settings (pydantic-settings)
├── database.py          # Engine, SessionLocal, get_db()
├── models/              # SQLAlchemy-Modelle
├── schemas/             # Pydantic-Schemas (ein Schema = ein Zweck)
├── routers/             # HTTP-Handler (ein Router = eine Resource)
├── services/            # Business-Logik
├── repositories/        # DB-Queries
└── bot/
    ├── client.py        # Bot-Initialisierung
    └── sync.py          # initial_sync() + Event-Handler

frontend/src/
├── api/                 # Axios-Instanz + API-Calls
├── stores/              # Pinia-Stores
├── composables/         # Wiederverwendbare Logik
├── components/          # UI-Bausteine
├── views/               # Seiten
└── assets/              # CSS-Variablen, Icons
```

---

## AI-Readiness (vorbereitet, noch nicht implementiert)

| Feature | Wie vorbereitet |
|---|---|
| LLM-Tool-Nutzung | FastAPI generiert OpenAPI-Spec → jeder Endpunkt ist maschinenlesbar |
| Agent-Tools | `PermissionCalculator` ist zustandslos und isoliert → 1:1 als Tool-Funktion exportierbar |
| Interner MCP-Server | Gleiche Service-Funktionen werden später in `backend/mcp_server.py` exponiert |
| Kontext für Prompts | Alle API-Antworten nutzen Pydantic-Schemas → direkt in LLM-Prompts einfügbar |

---

*Letzte Aktualisierung: 2026-02-19*

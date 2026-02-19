# Discord Role Master 3000 – Projektplan

> **Status:** In Entwicklung (Schritt 1 abgeschlossen) · **Erstellt:** 2026-02-19
> **Kontext-Dateien:** [`tech_stack.md`](tech_stack.md) · [`architecture.md`](architecture.md) · [`data_model.md`](data_model.md) · [`api_reference.md`](api_reference.md) · [`AGENT_SYSTEM_PROMPT.md`](AGENT_SYSTEM_PROMPT.md)

---

## 1. Projektübersicht & Ziele

### Problemstellung
Die native Discord-Oberfläche macht es schwer, komplexe Berechtigungs-Overwrites über viele Rollen, Kategorien und Kanäle hinweg zu überblicken. Konflikte (z. B. Rolle erlaubt `SEND_MESSAGES`, Kanal-Overwrite verweigert es) sind unsichtbar und schwer zu debuggen.

### Vision
Eine lokal laufende Web-App, die:
- den Discord-Server-Zustand (Roles, Categories, Channels, Overwrites) in einer lokalen DB spiegelt,
- diesen Zustand grafisch (Hierarchie-Bäume via Vue Flow) und tabellarisch darstellt,
- Berechtigungs-Konflikte **explizit visuell hervorhebt**,
- Änderungen über einen eigenen Discord-Bot zurück zu Discord pusht,
- so modular ist, dass KI-Assistenz nahtlos ergänzt werden kann.

### Nicht-Ziele (Schritt 1)
- Kein Multi-Server-Support
- Kein Docker / keine Container
- Keine KI-Features (nur architektonisch vorbereitet)
- Kein Produktions-Deployment

---

## 2. Taskliste

### ✅ Schritt 1 – Prototyp (lokal, kein Docker)

**Ziel:** Backend + Frontend laufen lokal. Bot verbindet sich mit Discord. Browser zeigt Servername, Kategorien und Kanäle aus der DB.

#### Setup
- [x] Git-Repository vorhanden
- [x] `/backend`, `/frontend`, `/docs` Ordner anlegen
- [x] `.gitignore` (Python + Node), `.env.example` (`DISCORD_BOT_TOKEN`, `GUILD_ID`, `DATABASE_URL`)
- [x] `README.md` mit lokalem Setup-Guide

#### Backend – Grundgerüst
- [x] Python `venv` + `requirements.txt` (Anpassung: Python 3.14 Support, `discord.py>=2.4.0`)
- [x] `backend/config.py` – Settings aus `.env` (pydantic-settings)
- [x] `backend/database.py` – Async SQLAlchemy Engine, `get_db()`
- [x] `backend/main.py` – App-Factory, CORS für `localhost:5173`, Router einbinden

#### Backend – Modelle (Subset Schritt 1)
- [x] `backend/models/guild.py` – `Guild`
- [x] `backend/models/category.py` – `Category`
- [x] `backend/models/channel.py` – `Channel`
- [x] `backend/models/__init__.py` – alle importieren, `create_all()` beim Start

#### Backend – Discord Bot
- [x] `backend/bot/client.py` – Bot-Client initialisieren
- [x] `backend/bot/sync.py` – `initial_sync(guild)`: Guild, Kategorien, Kanäle in DB schreiben
- [x] `on_ready` → `initial_sync()` aufrufen
- [x] Bot als asyncio Background-Task in FastAPI integrieren

#### Backend – API (siehe [`api_reference.md`](api_reference.md))
- [x] `backend/schemas/` – Pydantic Response-Schemas für Guild, Category, Channel
- [x] `backend/routers/guild.py` – `GET /api/guild`
- [x] `backend/routers/categories.py` – `GET /api/categories`
- [x] `backend/routers/channels.py` – `GET /api/channels`

#### Frontend
- [x] Vue 3 + Vite initialisieren (`npm create vue@latest frontend`)
- [x] Dependencies installieren (siehe [`tech_stack.md`](tech_stack.md))
- [x] `src/api/index.js` – Axios-Instanz mit `baseURL`
- [x] `src/stores/serverStore.js` – State: `guildInfo`, `categories`, `channels`
- [x] `src/views/DashboardView.vue` – Servername, Kategorien-Liste, Kanäle gruppiert
- [x] `App.vue` – Sidebar-Layout, dunkles Theme (Discord-Farbpalette)

#### Abnahme-Kriterien Schritt 1
- [x] `uvicorn backend.main:app --reload` läuft fehlerfrei
- [x] Bot loggt `on_ready`, SQLite-Datei `discord_rm.db` wird befüllt
- [x] `/docs` (Swagger) zeigt alle 3 Endpunkte, Antworten korrekt
- [x] `npm run dev` läuft, Browser zeigt Servername + Kategorien + Kanäle

> **Abweichungen:**
> - Python 3.14 erfordert `discord.py>=2.4.0` und `sqlalchemy>=2.0.36`.
> - VS Code Tasks & Wrapper-Scripts hinzugefügt.

---

### 🚀 Schritt 2 – Vollausbau Berechtigungen

#### Backend – Modelle & Sync
- [ ] `backend/models/role.py` – `Role`
- [ ] `backend/models/permission_overwrite.py` – `PermissionOverwrite`
- [ ] `initial_sync()` für Rollen und Overwrites erweitern
- [ ] Bot-Events: `on_guild_role_*`, `on_guild_channel_*`

#### Backend – API-Erweiterung
- [ ] `GET /api/roles`, `PATCH /api/roles/{role_id}`
- [ ] `GET|PUT|DELETE /api/channels/{id}/overwrites/{role_id}`
- [ ] `GET /api/conflicts`

#### Backend – PermissionCalculator Service
- [ ] `backend/services/permission_calculator.py`
- [ ] `calculate_effective_permissions(member, channel, guild_state)`
- [ ] `detect_conflicts(role_id, channel_id, guild_state)`
- [ ] `explain_permission(permission_bit, context)` ← KI-Vorbereitung
- [ ] Unit-Tests mit `pytest`

#### Frontend – Views
- [ ] `RolesView.vue` – Vue Flow Baum + List-View mit Inline-Editing + Konflikt-Markierung
- [ ] `CategoriesView.vue` – Vue Flow Baum (Kategorie → Kanäle) + Overwrite-Editor
- [ ] `ChannelsView.vue` – Tabelle + allow/deny-Checkboxen + Konflikt-Highlight

---

### 🐳 Schritt 3 – Docker & PostgreSQL

- [ ] `docker-compose.yml`: Backend, Frontend (Nginx), PostgreSQL
- [ ] Dockerfiles für Backend + Frontend
- [ ] SQLAlchemy `DATABASE_URL` → PostgreSQL
- [ ] Alembic einrichten + erste Migration generieren

---

### 🤖 Schritt 4 – KI-Integration

- [ ] FastAPI-Endpunkte als LangChain/OpenAI Tools strukturieren
- [ ] Interner MCP-Server: `backend/mcp_server.py`
- [ ] Frontend Chat-Widget „KI-Assistent"
- [ ] Prompt-Templates: Konflikt-Erklärung, Rollen-Erstell-Assistent

---

*Letzte Aktualisierung: 2026-02-19*

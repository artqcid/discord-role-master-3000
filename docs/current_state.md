# Projektstatus: Discord Role Master 3000
**Stand:** 19.02.2026 – *Schritt 1 (Prototyp) abgeschlossen*

## Überblick
Ein lokales Dashboard zur Verwaltung von Discord-Rollen und Berechtigungen, basierend auf einer synchronisierten Datenbank.
Der aktuelle Prototyp (Schritt 1) implementiert die Grundstruktur, die Synchronisation von Gilden-Daten (Kategorien, Kanäle) und ein Read-Only Dashboard.

## Architektur
- **Backend (Python/FastAPI):**
  - Layered Architecture: `Router` → `Repository` → `Model` (SQLAlchemy).
  - Datenbank: SQLite (`discord_rm.db`) mit `aiosqlite`.
  - Discord-Integration: `discord.py` Client läuft als `asyncio.Task` innerhalb der FastAPI-App (`Lifespan`).
- **Frontend (Vue 3/Vite):**
  - Store: Pinia (`serverStore`) lädt Daten vom Backend.
  - UI: Custom CSS/Variables im Discord-Look (Dark Theme).
  - API-Kommunikation: Axios.

## Tech-Stack & Besonderheiten
Aufgrund der lokalen Python-Version (3.14.0) mussten Versionen angepasst werden:
- **Python:** 3.14.0
- **discord.py:** `>=2.4.0` (Fix für `FastIntFlag` Bug)
- **SQLAlchemy:** `>=2.0.36` (Fix für `FastIntFlag` Bug)
- **Node.js:** (v20+ empfohlen)

## Projektstruktur
```
/backend
  /bot          # Discord Client & Sync-Logik
  /models       # SQLAlchemy Modelle (Guild, Category, Channel)
  /repositories # DB-Zugriff (CRUD)
  /routers      # FastAPI Endpunkte
  /schemas      # Pydantic Response Models
  config.py     # Settings (Pydantic)
  database.py   # DB Session & Engine
  main.py       # App Entrypoint

/frontend
  /src
    /api        # Axios Calls
    /stores     # Pinia State
    /views      # Vue Pages (DashboardView)
  App.vue       # Layout & Sidebar

/scripts        # PowerShell Start-Wrapper
.vscode         # VS Code Tasks Integration
```

## Features (Aktuell implementiert)

### Backend
1. **Discord Sync (On Startup):**
   - Der Bot verbindet sich, lädt Gilden-Infos, Kategorien und Kanäle.
   - Speichert/Aktualisiert alles in der lokalen SQLite-DB (`upsert`).
2. **API Endpunkte:**
   - `GET /api/guild` – Zeigt Server-Icon und Name.
   - `GET /api/categories` – Liste aller Kategorien (sortiert nach Position).
   - `GET /api/channels` – Liste aller Kanäle (mit Typ, Position, NSFW-Flag).

### Frontend
1. **Dashboard:**
   - Zeigt Server-Header.
   - Listet Kanäle gruppiert nach Kategorien auf.
   - Authentisches Discord Look & Feel (Farben, Sidebar).
2. **Setup:**
   - `.env` Konfiguration für API-URL.
   - Automatische Router-Konfiguration.

## Bedienung (VS Code Integration)
Das Projekt nutzt VS Code Tasks und Wrapper-Scripts für komfortables Arbeiten:

- **Starten:** `Strg+Shift+P` → "Tasks: Run Task" → `Backend + Frontend`
- **Stoppen:** Über Task `Stoppe Alles` oder `Stoppe Backend`/`Stoppe Frontend`.
- **Terminals:** Öffnet dedizierte Tabs mit klarer Statusanzeige.

## Nächste Schritte (Schritt 2)
- Implementierung von `Role` und `PermissionOverwrite` Modellen.
- Berechnungslogik für Berechtigungen (`PermissionCalculator`).
- Frontend-Ansichten für Rollen-Matrix.

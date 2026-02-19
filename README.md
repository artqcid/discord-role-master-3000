# Discord Role Master 3000

Lokale Web-App zur Visualisierung und Verwaltung von Discord-Server-Berechtigungen.

## Voraussetzungen

- Python 3.12
- Node.js 20 LTS
- Discord Bot Token (mit `guilds` Intent)

## Setup

### 1. Umgebungsvariablen konfigurieren

```powershell
Copy-Item .env.example .env
# .env mit echtem DISCORD_BOT_TOKEN und GUILD_ID befüllen
```

### 2. Python Virtual Environment

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r backend/requirements.txt
```

### 3. Frontend Dependencies

```powershell
cd frontend
npm install
cd ..
```

### 4. Backend starten

```powershell
# Im Workspace-Root, venv aktiviert
uvicorn backend.main:app --reload --port 8000
```

Swagger UI: http://localhost:8000/docs

### 5. Frontend starten (separates Terminal)

```powershell
cd frontend
npm run dev
```


Frontend: http://localhost:5173

### 6. Alternative: Starten mit VS Code Tasks (Empfohlen)

Das Projekt enthält vordefinierte Tasks für VS Code (Taskmanager Plugin):

1. Drücke `Strg+Shift+P` (oder `F1`)
2. Wähle **"Tasks: Run Task"**
3. Wähle **"Backend + Frontend"**

Dadurch werden Backend und Frontend parallel in dedizierten Terminals gestartet.
Zum Beenden nutze den Task **"Stoppe Alles"**.

## Projektstruktur

```
backend/
├── main.py           # App-Factory
├── config.py         # Settings (pydantic-settings)
├── database.py       # Async DB Engine
├── models/           # SQLAlchemy-Modelle
├── schemas/          # Pydantic-Schemas
├── routers/          # HTTP-Handler
├── repositories/     # DB-Queries
└── bot/
    ├── client.py     # Discord Client
    └── sync.py       # initial_sync()

frontend/src/
├── api/              # Axios-Instanz
├── stores/           # Pinia-Stores
├── views/            # Seiten
└── components/       # UI-Bausteine
```

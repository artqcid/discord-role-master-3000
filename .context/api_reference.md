# API Reference – Discord Role Master 3000

> Base URL (Dev): `http://localhost:8000/api`
> Interaktive Docs: `http://localhost:8000/docs` (Swagger UI)
> Alle Antworten: `application/json`

---

## Endpunkte

### Guild

| Methode | Pfad | Beschreibung |
|---|---|---|
| `GET` | `/guild` | Guild-Info (Name, ID, Icon) |
| `POST` | `/sync` | Manuellen vollständigen Sync triggern |

**`GET /guild` – Response:**
```json
{
  "id": "123456789",
  "name": "Mein Server",
  "icon_url": "https://cdn.discordapp.com/icons/..."
}
```

---

### Rollen

| Methode | Pfad | Beschreibung |
|---|---|---|
| `GET` | `/roles` | Alle Rollen, sortiert nach Position (absteigend) |
| `PATCH` | `/roles/{role_id}` | Rollenberechtigungen ändern (pusht zu Discord) |

**`GET /roles` – Response:**
```json
[
  {
    "id": "987654321",
    "name": "Moderator",
    "color": 3447003,
    "position": 5,
    "permissions": "1071698660929",
    "is_everyone": false,
    "mentionable": true,
    "hoist": true
  }
]
```

**`PATCH /roles/{role_id}` – Body:**
```json
{
  "permissions": "1071698660929"
}
```

---

### Kategorien

| Methode | Pfad | Beschreibung |
|---|---|---|
| `GET` | `/categories` | Alle Kategorien, sortiert nach Position |

**`GET /categories` – Response:**
```json
[
  {
    "id": "111222333",
    "name": "Allgemein",
    "position": 0
  }
]
```

---

### Kanäle

| Methode | Pfad | Beschreibung |
|---|---|---|
| `GET` | `/channels` | Alle Kanäle (inkl. `category_id`) |
| `GET` | `/channels/{channel_id}/overwrites` | Alle Overwrites für einen Kanal |
| `PUT` | `/channels/{channel_id}/overwrites/{role_id}` | Overwrite setzen oder aktualisieren |
| `DELETE` | `/channels/{channel_id}/overwrites/{role_id}` | Overwrite entfernen |

**`GET /channels` – Response:**
```json
[
  {
    "id": "444555666",
    "name": "general",
    "type": "text",
    "position": 0,
    "category_id": "111222333",
    "nsfw": false
  }
]
```

**`PUT /channels/{channel_id}/overwrites/{role_id}` – Body:**
```json
{
  "allow": "1024",
  "deny": "2048"
}
```

---

### Konflikte

| Methode | Pfad | Beschreibung |
|---|---|---|
| `GET` | `/conflicts` | Alle erkannten Berechtigungs-Konflikte |

**`GET /conflicts` – Response:**
```json
[
  {
    "role_id": "987654321",
    "role_name": "Moderator",
    "channel_id": "444555666",
    "channel_name": "general",
    "permission": "SEND_MESSAGES",
    "role_allows": true,
    "overwrite_denies": true
  }
]
```

---

## HTTP-Fehlercodes

| Code | Bedeutung |
|---|---|
| `400` | Ungültige Anfrage (Validierungsfehler) |
| `404` | Ressource nicht gefunden |
| `409` | Konflikt (z. B. Sync läuft bereits) |
| `502` | Discord API nicht erreichbar |
| `503` | Bot nicht verbunden |

---

## Implementierungsstand

| Endpunkt | Schritt 1 | Schritt 2 |
|---|---|---|
| `GET /guild` | ✅ | – |
| `GET /categories` | ✅ | – |
| `GET /channels` | ✅ | – |
| `POST /sync` | – | ✅ |
| `GET /roles` | – | ✅ |
| `PATCH /roles/{id}` | – | ✅ |
| `GET /channels/{id}/overwrites` | – | ✅ |
| `PUT /channels/{id}/overwrites/{role_id}` | – | ✅ |
| `DELETE /channels/{id}/overwrites/{role_id}` | – | ✅ |
| `GET /conflicts` | – | ✅ |

---

*Letzte Aktualisierung: 2026-02-19 (Schritt 1 geplant, Schritt 2 Entwurf)*

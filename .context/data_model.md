# Datenmodell – Discord Role Master 3000

> ORM: SQLAlchemy 2.x (async) · Treiber: aiosqlite (Dev), asyncpg (Prod)
> Alle Discord-IDs werden als `String` gespeichert (Discord Snowflakes sind 64-Bit-Integer, sicherer als String).
> Berechtigungs-Bitfelder (`permissions`, `allow`, `deny`) als `String` – SQLite unterstützt kein natives vorzeichenloses 64-Bit-Integer.

---

## Tabellen

### `guilds`
| Feld | Typ | Beschreibung |
|---|---|---|
| `id` | String (PK) | Discord Guild Snowflake |
| `name` | String | Servername |
| `icon_url` | String \| null | URL zum Server-Icon |
| `synced_at` | DateTime | Zeitpunkt des letzten Syncs |

### `roles`
| Feld | Typ | Beschreibung |
|---|---|---|
| `id` | String (PK) | Discord Role Snowflake |
| `guild_id` | String (FK → guilds) | |
| `name` | String | Rollenname |
| `color` | Integer | Farbe als HEX-Zahl (0 = keine Farbe) |
| `position` | Integer | Hierarchie-Position (höher = mehr Rechte) |
| `permissions` | String | Berechtigungs-Bitfeld |
| `is_everyone` | Boolean | True für `@everyone` |
| `mentionable` | Boolean | |
| `hoist` | Boolean | Separat in Mitgliederliste anzeigen |

### `categories`
| Feld | Typ | Beschreibung |
|---|---|---|
| `id` | String (PK) | Discord Category Snowflake |
| `guild_id` | String (FK → guilds) | |
| `name` | String | Kategoriename |
| `position` | Integer | Reihenfolge |

### `channels`
| Feld | Typ | Beschreibung |
|---|---|---|
| `id` | String (PK) | Discord Channel Snowflake |
| `guild_id` | String (FK → guilds) | |
| `category_id` | String (FK → categories) \| null | Übergeordnete Kategorie |
| `name` | String | Kanalname |
| `type` | String | `text`, `voice`, `forum`, `stage`, `announcement` |
| `position` | Integer | Reihenfolge innerhalb Kategorie |
| `nsfw` | Boolean | |

### `permission_overwrites`
| Feld | Typ | Beschreibung |
|---|---|---|
| `id` | Integer (PK, autoincrement) | |
| `guild_id` | String (FK → guilds) | |
| `target_type` | String | `role` oder `member` |
| `target_id` | String | Discord Snowflake der Rolle/des Members |
| `channel_id` | String (FK → channels) \| null | Zugehöriger Kanal |
| `category_id` | String (FK → categories) \| null | Zugehörige Kategorie |
| `allow` | String | Explizit erlaubte Berechtigungen (Bitfeld) |
| `deny` | String | Explizit verweigerte Berechtigungen (Bitfeld) |

---

## Beziehungen

```
guilds 1──n roles
guilds 1──n categories
guilds 1──n channels
guilds 1──n permission_overwrites
categories 1──n channels
channels 1──n permission_overwrites
categories 1──n permission_overwrites
```

---

## Berechtigungs-Logik (PermissionCalculator)

Discord berechnet effektive Berechtigungen stufenweise:

```
1. Basis: @everyone-Rollenberechtigungen
2. + Vereinigung aller weiteren Rollen des Members
3. + Kategorie-Overwrites (deny zuerst anwenden, dann allow)
4. + Kanal-Overwrites (deny zuerst anwenden, dann allow)
```

Ein **Konflikt** liegt vor, wenn:
- Eine Rolle `permission X` erlaubt (`allow`-Bitfeld der Rolle gesetzt)
- Ein Kanal- oder Kategorie-Overwrite `permission X` **verweigert** (`deny`-Bitfeld gesetzt)

→ Implementierung in `backend/services/permission_calculator.py`

---

## Migrations-Strategie

| Phase | Tool | Beschreibung |
|---|---|---|
| Schritt 1 | `create_all()` | Tabellen beim App-Start automatisch angelegen |
| Schritt 3+ | Alembic | Versionierte Migrationen für PostgreSQL-Prod |

---

*Letzte Aktualisierung: 2026-02-19*

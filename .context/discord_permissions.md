# Discord Permissions – Referenz

> Referenz für die Implementierung des `PermissionCalculator`-Service und die Darstellung im Frontend.

---

## Berechtigungs-Bitfelder

Discord kodiert Berechtigungen als 64-Bit-Integer (als String übertragen).
Jedes Bit entspricht einer Berechtigung.

### Wichtige Berechtigungen (Auswahl)

| Name | Bit (hex) | Beschreibung |
|---|---|---|
| `VIEW_CHANNEL` | `0x400` | Kanal sehen |
| `SEND_MESSAGES` | `0x800` | Nachrichten senden |
| `READ_MESSAGE_HISTORY` | `0x10000` | Nachrichtenverlauf lesen |
| `MANAGE_CHANNELS` | `0x10` | Kanäle verwalten |
| `MANAGE_ROLES` | `0x10000000` | Rollen verwalten |
| `ADMINISTRATOR` | `0x8` | Alle Berechtigungen (überschreibt alles) |
| `CONNECT` | `0x100000` | Sprachkanal betreten |
| `SPEAK` | `0x200000` | Im Sprachkanal sprechen |
| `MUTE_MEMBERS` | `0x400000` | Mitglieder stummschalten |
| `KICK_MEMBERS` | `0x2` | Mitglieder kicken |
| `BAN_MEMBERS` | `0x4` | Mitglieder bannen |
| `MENTION_EVERYONE` | `0x20000` | @everyone/@here erwähnen |

---

## Berechnungsreihenfolge (Discord-Spec)

```
1. Basis = @everyone Rollenberechtigungen
2. + ODER-Verknüpfung aller Rollenberechtigungen des Members
   (ADMINISTRATOR-Flag → sofort volle Rechte, Berechnung endet hier)
3. Kategorie-Overwrites für jede Rolle des Members:
   permit &= ~deny   (deny-Bits löschen)
   permit |= allow   (allow-Bits setzen)
4. Kanal-Overwrites für jede Rolle des Members (gleiche Logik)
5. Member-spezifische Overwrites (höchste Priorität)
```

---

## Overwrite-Typen

| `target_type` | Bedeutung |
|---|---|
| `role` | Gilt für alle Member mit dieser Rolle |
| `member` | Gilt nur für einen spezifischen User |

Ein Overwrite hat drei Zustände je Berechtigung:
- **Neutral** (weder `allow` noch `deny` gesetzt) → Eltern-Berechtigung gilt
- **Allow** (`allow`-Bit gesetzt) → explizit erlaubt
- **Deny** (`deny`-Bit gesetzt) → explizit verboten (überschreibt Rollen-Erlaubnis)

---

## Konflikt-Definitionen (für UI-Highlighting)

| Konflikt-Typ | Beschreibung |
|---|---|
| **Role-Channel-Conflict** | Rolle erlaubt X, Kanal-Overwrite verweigert X |
| **Category-Channel-Conflict** | Kategorie-Overwrite erlaubt X, Kanal-Overwrite verweigert X |
| **Role-Overlap** | Zwei Rollen eines Members haben widersprüchliche Overwrites im selben Kanal |

---

## Bitfeld-Operationen (Python)

```python
# Berechtigung prüfen
def has_permission(bitfield: str, permission_bit: int) -> bool:
    return bool(int(bitfield) & permission_bit)

# Berechtigung setzen
def add_permission(bitfield: str, permission_bit: int) -> str:
    return str(int(bitfield) | permission_bit)

# Berechtigung entfernen
def remove_permission(bitfield: str, permission_bit: int) -> str:
    return str(int(bitfield) & ~permission_bit)

# Overwrite anwenden
def apply_overwrite(base: int, allow: str, deny: str) -> int:
    base &= ~int(deny)
    base |= int(allow)
    return base
```

---

*Letzte Aktualisierung: 2026-02-19*

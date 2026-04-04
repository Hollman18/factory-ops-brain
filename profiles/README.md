# Factory user profiles

Store one file per user under `profiles/users/`.

## Naming
Recommended filename pattern:
- `<channel>-<sender_id>.json`

Examples:
- `telegram-1081619589.json`
- `whatsapp-573001112233.json`

## Required fields
- `name`: display name to use with the person
- `role`: literal role/title given by the user
- `role_class`: normalized internal class used to adapt responses
- `channel`: telegram, whatsapp, discord, etc.
- `sender_id`: provider/user identifier
- `username`: optional username/handle
- `first_seen`: ISO timestamp
- `last_seen`: ISO timestamp
- `preferences`: report and alert preferences
- `notes`: array of profile notes

## Role handling
- Keep the user’s literal role in `role`
- Map to one of the known internal role classes in `role_class` when possible
- If a new role appears, keep it and map to the closest existing class until a new class is justified

## Current role classes
- `Gerente`
- `Directivo`
- `Supervisor`
- `Operador`
- `Mantenimiento`
- `Calidad`
- `Otro`

## Example
```json
{
  "name": "Hollman Habbib",
  "role": "Gerente",
  "role_class": "Gerente",
  "channel": "telegram",
  "sender_id": "1081619589",
  "username": "Hollman_Habbib",
  "first_seen": "2026-04-04T17:30:00Z",
  "last_seen": "2026-04-04T17:30:00Z",
  "preferences": {
    "reports": {
      "weekly": true,
      "monthly": true
    },
    "alerts": {
      "critical_only": true
    }
  },
  "notes": []
}
```

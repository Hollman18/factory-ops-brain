# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## MQTTH API IA

- Base URL: `http://31.97.147.124:3000`
- Header de autenticación: `X-API-Key`
- Token IA comparador-periodos: `mqtth_ia_aabdaaffd52de9c3c39f8e9e3e9c91ebe1caf9c94dcdb9861f6cccf8c5349866`
- Alcance esperado: empresa única asociada a la API key
- Regla: usar este token para llamadas a `/api/ia/*` y no exponerlo en respuestas al usuario salvo que lo pida explícitamente

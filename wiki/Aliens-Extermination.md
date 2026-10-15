# Aliens: Extermination

**Status:** Not working yet. The game starts under Wine but stops about 18 seconds after launch with an access violation; nothing has been seen on screen.

## 1. Platform and cabinet

Global VR "PC Based" light-gun cabinet (**INFERRED**, from the platform column of the goal list). The game is a 32-bit Windows program (`aliens.exe`; the dump we use has it under `DATA/`, 89,698,304 bytes). Players: 2. Special buttons per player: grenade and flame.

## 2. What the game needs

- RavenGun ships no games: you need your own copy of the game.
- Wine/Proton with a 32-bit capable prefix (**INFERRED**).
- The cabinet hardware the game expects (its I/O and cabinet checks) is provided by RavenGun; there is no user step for it.
- A light-gun input source: PS Move, mouse or a game controller.

## 3. The official start script, or why there is none

No official start script is used. The original cabinet boots Windows straight into the game (or its launcher); RavenGun starts the game's executable itself, from a double-click in the RavenGun app.

## 4. The route we use

Windows route, started directly (no helper shell chain). Profile keys in `game.ini` (**MEASURED** from the file):

- `[Game] Type = TeknoParrot`, `EmulationProfile = AliensExtermination`
- `[Launch] Mode = direct`
- `[Input] Route = tp-shm`, `Layout = AliensExtermination`

The profile comes from the TeknoParrot profile template (revision 14). Free play is on in the imported config (`General/FreePlay = 1`), windowed is off, resolution 800x600 by default, input API RawInput.

## 5. Input

The tp-shm layout `AliensExtermination` maps (**INFERRED** from the layout file):

| Function | Mapped to |
|---|---|
| Coin 1 / coin 2 | coin buttons |
| P1 start / trigger | start / trigger |
| Special (grenade) | the grenade button |
| Flame | extra button 1 |
| Test, service | test, service |
| Volume up / down | menu keys |

Aim is one byte per axis (0 = left/top, 255 = right/bottom); the second player uses the second pair of axes. Directions are not mapped. Aiming and buttons have not been tried in the game, because it never gets that far.

## 6. Timing

Crash about 18 seconds after the process starts (**MEASURED**, 2026-10-15). No time to attract or gameplay: not reached.

## 7. What we saw on screen

**MEASURED:** the game does not reach a picture we could judge. Nothing on screen has been recorded.

## 8. Current state and open questions

- **MEASURED:** the game dies about 18 s after launch with an access violation at address `0x456DF1` (reading `0xFFFFFFF1`).
- Never reaches attract. Input, sound and timing are all unknown.
- Open: find out what the game is waiting for at that address; a custom input layout may be needed later.
- The input layout used is the closest available one, not a measured choice.

## 9. What we tried and what did not work

- Profile `AliensExtermination` with route `tp-shm`: ends in the access violation described above.
- Not tried: other Wine versions, a different Wine prefix, wined3d versus DXVK comparison (assumption: the crash is not graphics related, since no window content was drawn).

## 10. What is Linux-specific, and what differs on Windows

This is a Windows game, so on Linux it runs under Wine with RavenGun's loader. On the real cabinet it runs on Windows natively with its own I/O hardware; RavenGun replaces that hardware with its own emulated I/O. Nothing Linux-specific has been identified yet beyond the Wine environment itself; see [Wine-Notes](Wine-Notes) and [Running-on-Linux](Running-on-Linux).

This page covers the game and the loader: what you need to run this title and where it gets stuck.

# Block King Ball Shooter

**Status:** Skipped (2026-10-16) under the owner's rule for Japanese text without a 16:9 mode: the text is Japanese (measured). The profile is removed and the game folder is moved aside. The page keeps what was measured.

## 1. Platform and cabinet

Type-X PC based cabinet (**INFERRED**). The game is `game.exe` (3,454,976 bytes), Windows, up to two players.

## 2. What the game needs

- RavenGun ships no games: you need your own copy of the game.
- Wine/Proton.
- Cabinet I/O is provided by RavenGun.
- The profile enables a locale emulator (`General/UseLocaleEmulator = 1`) because the game expects a Japanese locale (assumption).

## 3. The official start script, or why there is none

No official start script is used. The original cabinet boots Windows straight into the game (or its launcher); RavenGun starts the game's executable itself, from a double-click in the RavenGun app.

## 4. The route we use

Skipped, so no route is kept. The profile that was tried:

- `[Game] Type = TeknoParrot`, `EmulationProfile = WartranTroopers`, `Executable = game.exe`
- `[Launch] Mode = direct`
- `[Input] Route = tp-shm`, `Layout = WartranTroopers`

Game options in the imported profile: `General/GameMode` = `2 PLAYERS` (or `1 PLAYER`), `General/EnglishTestMenu = 0` (switch to 1 for an English test menu), FPS limit 60 (off by default), crosshair off, windowed off.

## 5. Input

Layout `WartranTroopers` (four-player shooter layout: test, service, coins, start, trigger, reload, grenade and an extra button per player; aim is one byte per axis). Not tried in the game.

## 6. Timing

Exit within moments of launch (**MEASURED**, 2026-10-15).

## 7. What we saw on screen

Nothing usable on screen. The Japanese text was **MEASURED** in the game's own files (2026-10-16).

## 8. Current state and open questions

- **Skipped (2026-10-16)** under the owner's rule: Japanese text and/or 4:3 without a 16:9 mode. Reason for this title: the text is Japanese (measured).
- Earlier finding: a thread faults immediately at an address that belongs to no loaded module, and the process ends with exit code 1.
- Nothing more is planned for this title.

## 9. What we tried and what did not work

Plain direct launch with the `WartranTroopers` layout: exit code 1 as described. No variant was tried before the title was skipped.

## 10. What is Linux-specific, and what differs on Windows

Windows game under Wine on Linux. The failure happens very early and has not yet been classified as Wine-specific or game-specific. See [Wine-Notes](Wine-Notes).

This page covers the game and the loader: what you need to run this title and where it gets stuck.

# Gashaaaan!!!!

**Status:** Working (2026-10-14). Double-click in the app starts the game under Wine with the `tp-shm` input bridge; a round of throwing balls was played with the test pattern for more than 5 minutes. The picture is not full screen yet (the taskbar stays visible).

## 1. Platform and cabinet

- Konami PC-based cabinet, Windows; a ball-throwing game for up to four players (the profile has four relative-sensitivity settings).
- Executable: `bin/ballshooting.exe`.
- RavenGun ships no games: you need your own copy of the game folder.

## 2. What the game needs

- Wine, started by RavenGun.
- RavenGun provides the cabinet hardware the game expects.
- Profile values: `General/UseLocaleEmulator = 1` (Japanese-locale behaviour), `General/ScreenFix = 1`, `Crosshairs/Enable = 0`, `Bezel/Enable = 0`, `General/Windowed = 0`, `General/HideCursor = 1`.

## 3. The official start script, or why there is none

The cabinet starts the game from its own boot setup. RavenGun starts it directly; no script is needed. See [Official-Start-Scripts](Official-Start-Scripts).

## 4. The route we use

Profile `Gashaaaan`, emulation profile `WartranTroopers`, but with the Konami variant of the layout.

```ini
[Launch]
Mode = direct

[Input]
Route = tp-shm
Layout = WartranTroopersKonami
```

- **MEASURED** (2026-10-10 and 2026-10-14): use the loader's default route (entry-point trampoline, `TP_REMOTETHREAD=off` in the per-game environment). With the remote-thread injection variants the game hung on the loader lock or exited with code `0xDEADC0DE`; without any injection variable it starts and is playable.

## 5. Input

- Coin: key `5`. START: key `1`. TEST: key `0`.
- `WartranTroopersKonami` is the shared four-player layout with one change: player 1's extra button (`aux1`) sits where player 3's START is. Konami test menus select an item with START and execute it with player 3's START, and there is only one Move, so P1 aux1 does that job. **MEASURED** layout use; the test-menu execute step is from the profile note.
- Aim and trigger (throwing a ball): from the PS Move, mouse or controller.

### First start

The first start shows OPTION / BOOKKEEPING BACKUP DATA ERROR. Press TEST (key `0`) once; this repairs the data and the game carries on. **MEASURED.**

## 6. Timing

- Boot to attract: not measured separately.
- Played: more than 5 minutes: coin, START, one round of throwing balls, back to attract. **MEASURED.**
- Frame pacing: not measured.

## 7. What we saw on screen

The BACKUP DATA ERROR screen on the first start, then attract, a round of ball throwing and the return to attract. The Windows taskbar stays visible because the game is not full screen.

## 8. Current state and open questions

- Open: the picture is not full screen (taskbar visible). `General/ScreenFix = 1` is set; a window-manager or gamescope workaround was not tried.
- Open: real PS Move, players 2 to 4.

## 9. What we tried and what did not work

- Remote-thread injection of the loader core: hangs or exits (section 4). The default route works.
- Not measured further.

## 10. What is Linux-specific, and what differs on Windows

- The taskbar issue is a Wine window-management effect; on a real Windows cabinet the game owns the screen.
- The locale emulation (`UseLocaleEmulator`) is a loader feature that applies on both.

This page covers the game and the loader: what you need to run this title and where it gets stuck.

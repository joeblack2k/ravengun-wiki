# Infinity Blade FX

**Status:** Starts (2026-10-17). With DXVK and `Windowed = 1` under gamescope the game passes its start-up check and shows its attract ("ARE YOU READY?", 0/4 credits). The cabinet I/O (coins, keypad, tickets) still fails and play has not been measured.

## 1. Platform and cabinet

Adrenaline PC based cabinet (**INFERRED**). The game is `SwordGame.exe` (32-bit Windows, 49,878,016 bytes), an Unreal Engine 3 title with touch-style swipe input mapped to a light gun.

## 2. What the game needs

- RavenGun ships no games: you need your own copy of the game.
- Wine with DXVK (with wined3d the picture stays black).
- A RavenGun-provided stand-in module for the cabinet hardware component the game checks at start; no user step.
- The cabinet hardware the game expects is provided by RavenGun's own layer in a drop-in folder.

## 3. The official start script, or why there is none

No official start script is used. The original cabinet boots Windows straight into the game (or its launcher); RavenGun starts the game's executable itself, from a double-click in the RavenGun app.

## 4. The route we use

- `[Game] Type = TeknoParrot`, `EmulationProfile = InfinityBlade`, `Executable = SwordGame.exe`
- `[Launch] Mode = direct`, `Dxvk = true`
- `[Display] Gamescope = true` with `Windowed = 1` (with `Windowed = 0` the picture stayed white)
- `[Input] Route = tp-shm`, `Layout = TimeCrisis5` (the same layout family covers this game)

**How the start-up check passes (2026-10-16):** the game checks a cabinet hardware component at start and used to stop with an error message. RavenGun's stand-in module now offers the entry points the original module has, so the check passes and the Unreal Engine 3 start-up screen appears.

Profile option: `Crosshair Display` (Always / OnTouch / Never).

## 5. Input

Layout `TimeCrisis5` (aim bytes at offsets 12/16; trigger, reload, test, service, coin, start bits). Not measured in the game. The cabinet's own I/O ("Kaboom": coins, keypad, tickets) is a separate path that still fails, see section 8.

## 6. Timing

Not measured: the time to the attract and a five-minute run have not been recorded.

## 7. What we saw on screen

**MEASURED** (2026-10-17): the Unreal Engine 3 start-up screen, then the attract with "ARE YOU READY?" and 0/4 CREDITS. Earlier: wined3d gave black with GL errors, DXVK gave white until `Windowed = 1`.

## 8. Current state and open questions

- The game starts and shows its attract; it is not yet called working.
- Open: the cabinet I/O ("Kaboom"): the game's own `CKaboomCom` code opens a serial port for coins, keypad and tickets, and the log says "Kaboom: InitLib() failed". Play is not measured.

## 9. What we tried and what did not work

- 32-bit loader core injecting after 3 s: the game freezes on a loader lock (Wine "loader_section wait timed out"). The direct route avoids this.
- wined3d: black with GL errors; DXVK without `Windowed = 1`: white. Fixed by DXVK plus `Windowed = 1`.
- The start-up error about the cabinet hardware component was fixed by the stand-in module (2026-10-16).

## 10. What is Linux-specific, and what differs on Windows

Wine-specific: the loader lock and the Wine Mono requirement are Wine matters. On Windows the game runs directly. See [Wine-Notes](Wine-Notes).

This page covers the game and the loader: what you need to run this title and where it gets stuck.

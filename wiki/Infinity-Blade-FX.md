# Infinity Blade FX

**Status:** Not working yet (parked). Unreal Engine 3 starts, then the picture is white or black and the log stops at "Kaboom: InitLib() failed".

## 1. Platform and cabinet

Adrenaline PC based cabinet (**INFERRED**). The game is `SwordGame.exe` (32-bit Windows, 49,878,016 bytes), an Unreal Engine 3 title with touch-style swipe input mapped to a light gun.

## 2. What the game needs

- RavenGun ships no games: you need your own copy of the game.
- Wine plus **Wine Mono**, and a first-run dialog for the loader's DLL must be answered once.
- A 32-bit loader core (the game is 32-bit).
- The cabinet hardware the game expects is provided by RavenGun's own layer in a drop-in folder; no user step.
- `steam_api.dll` is present in the game folder (**INFERRED**: the game is related to a Steam release).

## 3. The official start script, or why there is none

No official start script is used. The original cabinet boots Windows straight into the game (or its launcher); RavenGun starts the game's executable itself, from a double-click in the RavenGun app.

## 4. The route we use

- `[Game] Type = TeknoParrot`, `EmulationProfile = InfinityBlade`, `Executable = SwordGame.exe`
- `[Input] Route = tp-shm`, `Layout = TimeCrisis5` (the same layout family covers this game)
- Parked: no direct-launch settings recorded as working.

Profile option: `Crosshair Display` (Always / OnTouch / Never).

## 5. Input

Layout `TimeCrisis5` (aim bytes at offsets 12/16; trigger, reload, test, service, coin, start bits). Not tried in the game.

## 6. Timing

Not measured yet.

## 7. What we saw on screen

**MEASURED** (round 10): the engine starts, then a white or black picture; the log stops at `Kaboom: InitLib() failed`. Graphics: wined3d gives black with GL errors, DXVK gives white (earlier note).

## 8. Current state and open questions

- Open: what `Kaboom: InitLib()` is and why it fails; graphics are a separate problem to solve after that.
- Known extra step: Wine Mono and a first-run dialog for the loader DLL.

## 9. What we tried and what did not work

- 32-bit loader core injecting after 3 s: the game freezes on a loader lock (Wine "loader_section wait timed out").
- Injection from the entry point loads the core but the core ends the process after about 17 s (exit code).
- wined3d: black with GL errors; DXVK: white.

## 10. What is Linux-specific, and what differs on Windows

Wine-specific: the loader lock and the Wine Mono requirement are Wine matters. On Windows the game runs directly. See [Wine-Notes](Wine-Notes).

This page covers the game and the loader: what you need to run this title and where it gets stuck.

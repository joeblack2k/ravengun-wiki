# Lost Land Adventure

**Status:** Starts (2026-10-16). A double-click shows the attract ("DEMO PLAY", dome picture) after about 2 minutes of loading. The text is Japanese although English is set, and coin and START have not been measured.

## 1. Platform and cabinet

Namco ES3X cabinet (PC based, the same family as [Time Crisis 5](Time-Crisis-5)). The game is a 64-bit Windows program started through `RSLauncher.exe`.

## 2. What the game needs

- RavenGun ships no games: you need your own copy of the game.
- Wine/Proton with 64-bit support.
- The 64-bit Visual C++ 2010 MFC runtime (`mfc100u.dll`): `RSLauncher.exe` imports it; RavenGun's redistributable setup step installs it from Steam's vcredist (`NativeDlls`).
- The same cabinet-side runtime as Time Crisis 5 (provided by RavenGun).

## 3. The official start script, or why there is none

The cabinet starts `RSLauncher.exe`. RavenGun starts the same executable itself, from a double-click.

## 4. The route we use

Route like [Time Crisis 5](Time-Crisis-5) (same platform and runtime):

- `[Game] Type = TeknoParrot`, `EmulationProfile = LostLandAdventures`, `Executable = RSLauncher.exe`, 64-bit
- `[Launch] Mode = direct`
- `[Input] Route = tp-shm`, `Layout = LostLandAdventures`

## 5. Input

Layout `LostLandAdventures` (TeknoParrotUi's LostLandPipe): triggers and aiming. Coin and START are not measured.

## 6. Timing

**MEASURED** (2026-10-16): about 2 minutes of loading before the attract.

## 7. What we saw on screen

**MEASURED** (2026-10-16): the attract with "DEMO PLAY" and a dome-shaped picture. The text is Japanese.

## 8. Current state and open questions

- The game starts and shows its attract; it is not yet called working.
- Open: the text is Japanese although `[Arguments] Text Language = English` is set in the game's config (the dump also carries language setup scripts); coin and START are not measured.

## 9. What we tried and what did not work

Without `mfc100u.dll` the launcher could not start; installing the 64-bit MFC runtime fixed that. No other variants were needed to reach the attract.

## 10. What is Linux-specific, and what differs on Windows

Windows game under Wine; the 64-bit MFC runtime has to be provided as a native DLL. See [Running-on-Linux](Running-on-Linux).

This page covers the game and the loader: what you need to run this title and where it gets stuck.

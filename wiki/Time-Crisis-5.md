# Time Crisis 5

**Status:** Not working yet on the direct route. The game starts, shows attract and accepts a coin, but aim, trigger and pedals do not reach it; an earlier route through the TeknoParrot UI reached playable.

## 1. Platform and cabinet

Namco ES3X cabinet (PC based). The game is 64-bit Windows: the launcher `RSLauncher.exe` starts `TimeCrisisGame-Win64-Shipping.exe` (version 1.0.10897.0, Unreal Engine). One player; two foot pedals.

## 2. What the game needs

- RavenGun ships no games: you need your own copy of the game.
- Wine/Proton with 64-bit support.
- A loader runtime from the TeknoParrot distribution (`[Loader] Build = teknoparrot`): Time Crisis 5 uses Namco's card/I/O DLLs next to the loader, which RavenGun's own core does not have yet.
- The cabinet hardware the game expects is provided by RavenGun's drop-in layer; no user step.

## 3. The official start script, or why there is none

The cabinet starts `RSLauncher.exe`. RavenGun starts the same executable directly.

## 4. The route we use

- `[Game] Type = TeknoParrot`, `EmulationProfile = TimeCrisis5`, `Executable = RSLauncher.exe`, `Is64Bit = true`
- `[Launch] Mode = direct`, `WorkingDirectory = .`
- `[Loader] Build = teknoparrot`, `PostStartMs = 3000` (injection after 3 s; injection at the entry point makes even the coin fail)
- `[Input] Route = tp-shm`, `Layout = TimeCrisis5`, `CoinKeys = lshift,t`

Route chain on the direct route: double-click in RavenGun, daemon, a Wine launch of the 64-bit OpenParrot loader, then the game; a helper mirrors `/dev/shm/ravengun_JvsState` into the game's `TeknoParrot_JvsState` mapping (64 bytes).

## 5. Input

Layout `TimeCrisis5` (control word at offset 8; aim at offset 12 = X, 16 = Y, one byte each):

| Function | Bit |
|---|---|
| Test | 0x1 |
| Service | 0x4 |
| Coin | 0x8 (the game reads the coin from the keyboard: **Shift+T**; the daemon sends it for the Move coin button) |
| Trigger | 0x10 |
| Gun button (reload) | 0x20 |
| Left pedal (middle button / grenade) | 0x40 |
| Right pedal (extra button 1) | 0x80 |
| Start (Enter) | 0x400 |

Offscreen rule: the core treats an axis byte of 0/1 or 254/255 as off-screen, so aim stays within 2..253 on screen. In the menu, shoot "1-player solo".

## 6. Timing

Not measured on the direct route beyond the attract and the tutorial instruction.

## 7. What we saw on screen

**MEASURED** (2026-10-14): attract with the Bink logo and "INSERT 1 CREDIT(S)"; a coin leads to "SELECT A GAME MODE" and then the instruction. The pedal prompts ("Step on the left pedal to move!", "Hold down the right pedal to attack!") do not react; ammunition stays at 9.

## 8. Current state and open questions

- **Contradiction between sources:** `game.ini` and the compatibility page say playable (aim, trigger and left pedal work; right pedal unchecked). That was measured on the older TeknoParrotUi route. The newer direct route (2026-10-14/15) does not deliver aim, trigger or pedals; the board image in shared memory is correct (trigger 0x10, gun 0x20, pedals 0x40/0x80 seen while held), the mirror is active, yet the game ignores them.
- Open: whether the core sees the bytes inside Wine; the pipe helper (`pipehelper.exe` instead of the RavenGun bridge); how the core fills its USB I/O input for this game. The core is closed and its code is not readable, so this needs a memory dump of the running game.

## 9. What we tried and what did not work

- Zeroing the source file at start: the bytes are clean, no effect.
- Cabinet drop-in layer switched off: no effect (it is not the cause).
- Entry-point injection (`RemoteThread = off`): the coin stops working too; reverted.
- A mouse and a Move on the same player wiped each other's held button; fixed in the loader (inputs now OR per source).

## 10. What is Linux-specific, and what differs on Windows

Wine-specific: the game's input reaches it through a shared-memory block that the Linux daemon writes and a Wine-side helper mirrors; that bridge is the part under investigation. On Windows the TeknoParrot UI writes the same block directly. See [Wine-Notes](Wine-Notes) and [Loader-Architecture](Loader-Architecture).

This page covers the game and the loader: what you need to run this title and where it gets stuck.

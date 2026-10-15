# House of the Dead: Scarlet Dawn

**Status:** Working (2026-10-14). A double-click in the RavenGun app starts the platform daemon and the game through `rg-direct` (two executables), without the TeknoParrot front-end. Measured on the TV: START, title, MODE SELECT, STORY MODE, ITEMS, a level, CONTINUE, GAME OVER and the ranking, 8 min 44 s without a break.

RavenGun ships no games; you need your own copy of the game folder.

## 1. Platform and cabinet

- Sega ALLS (UX variant, platform id `ACA0`), 2018, built in Unreal Engine 4.18.1. Both programs are 64-bit Windows programs. Two-player lightgun game. **MEASURED** from the game files.
- Game executable `Hodzero-Win64-Shipping.exe` (54,128,128 bytes, code name "Hodzero", game id `SDET`) plus Sega's platform daemon `amdaemon.exe` (console program, `Ver.2437`).
- The cabinet configuration (`AMDaemon/config.json`) describes two players, each with `start`, `gun_select` and `gun_special` buttons, plus cabinet `test` and `service` switches, coin input, `max_credit = 24`, 1920x1080 video and `error.auto_reset = true` (a restart after an error is normal behaviour). **MEASURED** from the file.
- The TeknoParrot template is `GameProfiles/HOTDSD.xml` revision 21 (`EmulationProfile = ALLSHOTDSD`, `HasTwoExecutables = true`, `LaunchSecondExecutableFirst = true`).

## 2. What the game needs

- Your own dump of the game folder: 2,081 files, about 13 GB. One Unreal package of 7.8 GB plus loose video and asset files (577 loose files exist nowhere in the package, so copy the whole folder). **MEASURED.**
- Both executables must start, daemon first. RavenGun provides the cabinet hardware the game expects; the cabinet's I/O board is emulated.
- A Wine prefix with the usual Visual C++ runtimes (`vcruntime140`, `msvcp140`, `msvcp110`/`msvcr110` for the daemon). RavenGun's shared prefix (`~/.local/share/ravengun/prefixes/shared/wine`) already has all 44 libraries the two programs import. **MEASURED.**
- Direct3D 11 and a display server; the game does not run without one.
- A case-insensitive view of the folder: the engine asks for `HodZero_v1` while the disk folder is `Hodzero_V1`. RavenGun's local view handles that; on a plain case-sensitive copy this can break the 577 loose files. **MEASURED** (works on a case-insensitive mount), the breakage on ext4 is **INFERRED**.
- Free play is on in the profile (`General/FreePlay = 1`).

## 3. The official start script, or why there is none

The cabinet chain is `game.bat`, then `App/Startup/AppStartup.bat`, which calls `05_SetVideoPort.bat`, `10_SetResolution.bat` (`SetResolution.exe 1920 1080 0`), `20_SetAudioVolume.bat` (`SetAudioVolume.exe 85 75`), `99_StartApp.bat` and finally `App/Hodzero/StartApp.bat`. The last one starts the daemon, waits five seconds (`DAEMON_WAIT_SECONDS=5`), starts the game with `-launch="cabinet" ... -NotInstalled -UNATTENDED` and cleans up. **MEASURED** from the files.

The chain also changes registry values, sets the desktop resolution and runs `rmdir /S /Q "Y:\"` at every start. **Do not run it on your PC**; RavenGun reads it and takes over only the order (daemon first, five seconds, then the game) and `-UNATTENDED`. See [Official Start Scripts](Official-Start-Scripts).

`-UNATTENDED` matters: after a fatal Unreal error, a run without it sat for 60 seconds on a modal error window before the process ended. **MEASURED** for the gap, mechanism **INFERRED**.

## 4. The route we use

Double-click in the app, then daemon, `rg-direct` and Wine with the OpenParrot loader, two executables:

```ini
[Game]
Type = TeknoParrot
EmulationProfile = ALLSHOTDSD
Executable = Hodzero-Win64-Shipping.exe
Executable2 = amdaemon.exe
HasTwoExecutables = true
LaunchSecondExecutableFirst = true
[Launch]
Mode = direct
Arguments = -UNATTENDED
[Wine]
Prefix = shared
Runner = wrapper
[Env]
RG_UNSET_REMOTETHREAD = 1
```

- `rg-direct` starts `amdaemon.exe` first, waits 5 s, then the game. Neither program gets the cabinet's own arguments (the daemon none; the game only `-UNATTENDED`).
- **The remote-thread trap (MEASURED):** under Wine the TeknoParrot front-end sets `TP_REMOTETHREAD`, and the loader's remote-thread injection then fails with "Failed to find kernel32.dll in target process". `RG_UNSET_REMOTETHREAD = 1` with `[Wine] Runner = wrapper` removes it, and the loader takes its default entry-point route (`Have fun :)` in the log). Without that the core does not attach.
- The daemon on its own dies after about 1 s with `amPlatformGetPlatformInformation(). ErrCode 0`. Started through the loader (with any injected library) it stays alive; with the real core it proceeds to `Process state: Advertise`. **MEASURED**; the causal reading is **INFERRED**.
- Run it from a local view of the game folder (real copies of what gets written, links for the 12 GB read-only bulk) so the daemon's 8.4 MB app-data file and `teknoparrot.ini` do not land in your game folder.

## 5. Input

All input comes from the RavenGun engine, through two channels (**MEASURED**):

- Triggers and aim: shared memory, layout `HOTDSDPipe` (`[Input] Route = tp-shm`, `Layout = HOTDSDPipe`): button field at offset 8 (bit 0 = P1 trigger, bit 1 = P2 trigger), aim bytes at offsets 12/16/20/24.
- START, sub-trigger (grenade), controller select, test and coin: a 64-byte ALLS USB-IO report on `\\.\pipe\TeknoParrotPipe` (`ControlPipe = AllsUsbIo`), refreshed about every 15 ms.

| Action | Key / button |
|---|---|
| Coin | key 5 |
| START | key 1 |
| Test | key 0 or F2 |
| Trigger | left button |
| Sub-trigger | grenade button |
| Controller select | aux1 |

The game reports once per session `"aimeId" is invalid` when the login screen opens; that is the absent card reader and does not block play (guest path). **MEASURED.** Per-player gun calibration values are written by the game (for example `P2_LeftX 42`, `P2_RightX 890`). Sub-trigger and controller select have not been checked separately.

## 6. Timing

- Loading into the first level: about 1.5 minutes after START. Level maps load in 2 to 5 s once the game is up. **MEASURED.**
- Double-click run, 2026-10-14: 8 min 44 s of continuous play on the TV. **MEASURED.**
- An earlier run stopped after about 3 minutes with exit code 3 while a mouse injection was clicking on the desktop; cause not established.
- Earlier sessions on plain Wine: of eight runs with a picture on one day, four reached attract and four stopped during start-up with the same error; the best run held 363 s of attract. Those were before the double-click route. **MEASURED.**
- Frame pacing: not measured yet.

## 7. What we saw on screen

**MEASURED** on the TV: attract with "FREE PLAY", START, title, MODE SELECT, STORY MODE, ITEMS, then play in the level with the crosshair following the aim, CONTINUE, GAME OVER and the ranking. The game's own log shows `Match State Changed from WaitingToStart to InProgress` and all sublevels (`SL_Stage0_ENEMY`, `_BG`, `_EFFECT`, ...) activating.

## 8. Current state and open questions

- Working via double-click (2026-10-14).
- Not yet played with the real PS Move.
- Open: sub-trigger and controller select checked separately; player 2.
- Open: the single early stop with exit code 3, and the earlier start-up failures (not seen on the double-click route).
- Open: `DebugWithoutAMDaemon` in the game's `Game.ini` is `false`; whether the game plays without the daemon with it on `true` is untested.

## 9. What we tried and what did not work

- **Starting `amdaemon.exe` on its own**: dies after 1 s. Adding its `-c`/`-l` arguments, or a bare copy of the folder, changed nothing.
- **Headless runs**: the game stopped logging after 0.8 s and we could not tell stuck from killed. Stop a game cleanly if you want to read its log; `SIGTERM` loses buffered lines.
- **Treating one crash as a property of a place**: a crash exactly when the first level finished loading did not repeat; the next session ran 105 s longer with 22 GB of memory free.
- **Comparing runs with different launcher binaries**: two launcher builds were in play and it was nearly missed. Have the launcher print its own path and hash at the top of the log ([Loader Architecture](Loader-Architecture)).

## 10. What is Linux-specific, and what differs on Windows

- Runs under Wine (Proton build used as plain Wine) with a shared prefix; the daemon is a console program and starts without a display, the game needs one.
- Wine-only: the remote-thread variable must be removed (section 4).
- Drive letters `X:`, `Y:`, `D:` are created by the cabinet chain on Windows; RavenGun does not run that chain and the game plays without them. On Windows you would probably start the daemon, wait five seconds, start the game with `-UNATTENDED` and make the letters with `subst`. Not tested by us.
- Case sensitivity: a network mount is usually case-insensitive; on ext4 copy through a view.
- `SetResolution.exe` and `SetAudioVolume.exe` are not run; gamescope or the display server decides the resolution.
- See [Wine Notes](Wine-Notes) and [Running on Linux](Running-on-Linux).

This page covers the game and the loader: what you need to run this title and where it gets stuck.

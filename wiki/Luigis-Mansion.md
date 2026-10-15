# Luigi's Mansion Arcade

**Status:** Not working yet. A double-click in the RavenGun app starts the game and it runs full screen in attract mode (about 6 min 9 s of continuous attract and demo was seen on the TV, 2026-10-13), but it is not playable: coin and TEST do not reach the game, so START without credits does nothing.

RavenGun ships no games; you need your own copy of the game folder.

## 1. Platform and cabinet

- Sega Nu 1.1 (Sega Amusements, Nintendo licence): a PC running Windows with a normal 1920x1080 display. The game is a **64-bit Windows program**: `exe/x64/VACUUM.exe`, 3,436,544 bytes, PE32+ GUI, image base `0x140000000`, Direct3D 11 and DirectInput. Game id `SDCF`. **MEASURED** from the file.
- The cabinet controls are a **lightgun combined with a vacuum handle**: aim with the gun, pull the trigger/handle to vacuum, a separate button for the Strobulb flash, a select switch, screen-out button. A second player is possible. **INFERRED** from the profile and the game's tutorial screens; nobody here has seen the cabinet.
- The TeknoParrot template is `GameProfiles/LuigisMansion.xml` revision 19 (`EmulationProfile = LuigisMansion`).

## 2. What the game needs

- Your own dump of the game folder, with the data under `DataGlobal/EN/Data/` and the program in `exe/x64/`. **MEASURED:** the game looks for its data relative to its own folder under two roots: `..\..\DataGlobal\EN\Data\...` and `..\..\Data\...` (for example `Data\System\Model\cube.bin`). RavenGun makes a view in which `Data` points to `DataGlobal/EN/Data`.
- **Working directory must be `exe/x64`.** With the top folder as working directory the game stops with an access violation. **MEASURED.**
- **Movies.** The `.wmv` films (`Data/Movie/*.wmv`) go through Wine's GStreamer backend. Without an ASF demuxer and a WMV decoder (`libgstasf.so`, `libgstlibav.so`) the game exits at the first movie. RavenGun supplies them through `[Wine] GStreamerPlugins` (`~/.local/share/ravengun/tools/gst-extra/plugins`, fetched with `scripts/fetch-gst-wmv.sh`). **MEASURED.**
- Write access to `Ram/` and `Log/` (settings, credits, logs).
- RavenGun provides the cabinet hardware the game expects.
- gamescope for full screen.

## 3. The official start script, or why there is none

Next to the game is `game.bat`:

```bat
set GAMEID=SDCF
if not exist Y:\%GAMEID% (
    rmdir /S /Q Y:\
    mkdir Y:\%GAMEID%
)
start /wait sendFlash COM1 LMAIO.bin
start /wait x:\exe\x64\VACUUM.exe
```

**Do not run it.** `rmdir /S /Q Y:\` wipes a whole drive if `Y:\SDCF` is missing (on a cabinet that is a dedicated volume; on your PC `Y:` may be yours), it throws away the app-data folder, and `sendFlash` talks to a serial port. RavenGun takes over only the working directory, the data roots and the movies. Each of the four steps was tested on its own, and none changed the result (section 9). See [Official Start Scripts](Official-Start-Scripts).

## 4. The route we use

Profile (`patches/LuigisMansion/game.ini`):

```ini
[Game]
Type = TeknoParrot
EmulationProfile = LuigisMansion
Executable = VACUUM.exe
[Launch]
Mode = direct
WorkingDirectory = .
[Loader]
Core = ravengun
[Display]
Gamescope = true
[Wine]
GStreamerPlugins = ~/.local/share/ravengun/tools/gst-extra/plugins
[Input]
Route = tp-shm
Layout = LuigisMansion
```

- Double-click: the engine starts `rg-direct`, which runs gamescope, Wine, the OpenParrot loader and `VACUUM.exe`. The loader is built from the public OpenParrot source. `[Loader] Core = ravengun` selects RavenGun's own OpenParrot core, together with a RavenGun drop-in library (`rg-pe-hook.dll`) in the game's `exe/x64`. **MEASURED:** with the stock TeknoParrot core and no gamescope the loader stops after about 13 s with exit code 9 and the game is gone.
- The core is the loader's first argument (the loader appends `.dll`), so cores can be swapped by changing only that argument.
- Standard loader route: leave `TP_REMOTETHREAD` out of the environment entirely. Setting it to `off` is still "present" and puts the loader on a remote-thread route that does not work for this game.
- Start the loader from its own runtime folder; set the game's working directory with `WorkingDirectory`, not by `cd`.
- An extra drive letter is a symbolic link in `<prefix>/dosdevices/`. Create it only after the Wine server has started (Wine rewrites `dosdevices` at startup), and remove it afterwards so later runs are unchanged. **MEASURED.**

## 5. Input

Layout `LuigisMansion` (a shared board image, **MEASURED** from the profile): a 32-bit control field at offset 8: start (bits 0/3 for P1/P2), vacuum button = Strobulb (bit 1/4; mapped to grenade), vacuum handle (bit 2/5; mapped to trigger), test (bit 8), select switch P1 (bit 9; mapped to aux1), service (bit 10), screen-out (bit 16/17; mapped to reload). Aim: four bytes at offsets 12..15 (P1Y, P1X, P2Y, P2X), calibration X 3..252 and Y 6..250, left/top = 0. An aim of 0.8 / 0.3 came out as x byte 202 and y byte 79 with a real controller. **MEASURED.**

**Coins are not part of this block.** On the double-click route, with mouse mode:

- Coin (key 5): no credits.
- TEST (key 0): set in the board image (byte 9 = 0x01) but the game opens no test menu.
- START without credits: nothing (expected).

So the board image does not reach the game with the RavenGun core yet, or the core does not read it for this title. **MEASURED** (2026-10-14).

The game never touches COM1: with a pseudo-terminal on `com1` there were 0 COM names in 86 file-open lines. The flash step belongs to the separate tool in the start script. **MEASURED.**

## 6. Timing

- With the RavenGun core and gamescope, 2026-10-13: loading screens at 17:42:27 and 17:42:42, first attract picture at 17:42:57 ("Please Insert Coin(s)", CREDIT(S) 0), last attract picture at 17:49:06: **6 min 9 s** of continuous attract and demo, game still alive when our 420 s limit stopped it. **MEASURED** on the TV.
- Headless runs on a core without that drop-in: the game process ended 5 to 7 s after it appeared. **MEASURED.**
- The same moment in the same start measured 4.8 s and 6.0 s on different runs; a full file trace (`WINEDEBUG=+file`) stretched a 5 to 7 s life to 25 to 30 s. Never compare instrumented with plain runs.
- Frame pacing: not measured.

## 7. What we saw on screen

**MEASURED** on the TV: loading screen, then attract: Luigi in the hall with "Please Insert Coin(s)", gameplay clips, tutorial screens ("Aim > Strobulb > Aim > Vacuum", "Tactics", "Charge The Strobulb For A Stronger Flash", "Power Surge", "Strobomb", "Continue ... Power Boost 15 Sec"), and the title screen. No error message was on screen in the 6-minute window.

## 8. Current state and open questions

- Not working yet: **no coin and no TEST reach the game** on the double-click route, so it cannot be started. Status in the profile is `playable` (attract only).
- Next step: find out which input path the game uses on Sega Nu (input protocol `shared-luigi-mansion`) in RavenGun's core and fill it from the I/O bridge state; coins separately (not through the shared block).
- Open: whether START works once credits exist; aim and trigger in play; the test menu.

## 9. What we tried and what did not work

- **The stock TeknoParrot core, no gamescope**: the loader stops after about 13 s with exit code 9. Switching to the RavenGun core with gamescope fixed it.
- **The four start-script steps, one at a time** (same setup, core hash checked each time): `set GAMEID=SDCF` no effect (process ends at 6.0 s); `sendFlash COM1 LMAIO.bin` inert (exit 0, 35 bytes sent, the firmware file is never sent); preparing `Y:\SDCF` no effect; starting from `X:\exe\x64\` no effect. All four are crossed off.
- **An exit code chased as meaningful**: a `32` turned out to be a leftover register value.
- **A sampler that recognised the game by command line only** reported it never saw the game when it was started from a drive letter. A run where the process was never found says nothing about the game.
- **Headless runs** say nothing about how the game looks; the picture evidence comes from the TV run.

## 10. What is Linux-specific, and what differs on Windows

- Wine itself: an ordinary Wine build (we use a Kron4ek `wine-proton-11.0-2` build), not Proton; a prefix with 64-bit loader and core, because the game is PE32+.
- Drive letters are links in `dosdevices`; the Wine-server warm-up rule above is Linux-only. On Windows `X:` is a partition, mapped drive or `subst`.
- Movies need GStreamer ASF and libav plug-ins through `GST_PLUGIN_PATH`; on Windows the system codecs do it.
- COM1 under Wine maps to `/dev/ttyS0`, which is `root:uucp 0660` on a Steam Deck, so the game gets ACCESS_DENIED instead of "does not exist". Put a pseudo-terminal on `dosdevices/com1` to test.
- Make a view of links for a read-only source: a real `exe` folder with links inside, not one link to the source, or a launcher that wants to place files fails silently.
- Absolute timings on Windows will differ (assumption).

See [Wine Notes](Wine-Notes) and [Running on Linux](Running-on-Linux).

This page covers the game and the loader: what you need to run this title and where it gets stuck.

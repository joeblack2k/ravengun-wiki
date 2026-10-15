# Transformers: Shadows Rising

**Status:** Working (2026-10-15). A double-click in the RavenGun app starts the Sega "Game Shell" and the game under Wine. After about 2 minutes of loading it was played for 6.5 minutes in mouse mode: coin, START, aim and shoot, continue, a boss, score 29402. The freeze seen about a minute after START on 2026-10-14 did not come back in two runs. The cabinet lever ("PUSH THE LEVER") is not emulated; the game carries on without it.

RavenGun ships no games; you need your own copy of the game folder.

## 1. Platform and cabinet

- Sega RingEdge 2 title from 2018, built as a "Game Shell": not one program but a small Sega environment (`shell/`) that starts the real game (`Transformers2/`) and stays alive next to it. Both are 32-bit Windows programs (PE32). Two-player lightgun shooter. **MEASURED** from the files.
- `shell/Shell.exe` (Game Shell build 180605, 1,438,720 bytes) starts `Transformers2/Transformers2.exe` (9,332,736 bytes, window title `TF2_Gun | Release`). There is also `Launcher/SystemLauncher.exe` (reads `Launcher.ini`, `ShellDirectory=c:\sega\shell`).
- The shell expects a fixed install layout: `C:\Sega\Shell` and `C:\Sega\Transformers2`, asset directory `C:\sega\shelldata`. **MEASURED** from the ini files.
- The cabinet has two unrelated input devices. **MEASURED** from the code:
  1. **The gun**: a DirectInput joystick. `Transformers2.exe` opens the system's first joystick (`GUID_Joystick`, no filter on vendor or product), sets every axis to -1000..1000 and reads an 80-byte `DIJOYSTATE`. Horizontal comes from axis `lY`, vertical from `lX` (player 2: `lRx` and `lZ`); left/top is the low end.
  2. **The cabinet I/O board**: a HID device that `Shell.exe` looks for through `HID.DLL` and SetupDi. It drives lamps, the key panel and hardware recoil. The shell recognises it by HID usage (Generic Desktop / Game Pad, `0x0001`/`0x0005`), not by vendor id or name, and writes a 3-byte report `00 <a> <b>`.
- `Transformers2.exe` also contains LED-tracking and camera code (`LED.obj`, `TF2LED.obj`); not used on our route (**INFERRED**).

## 2. What the game needs

- Your own dump: the `Sega` folder with `shell/`, `Transformers2/` and `Launcher/`.
- A Wine prefix with native `d3dx9_43`, `d3dcompiler_43` and `d3dcompiler_47`. Without them the game stops with the Windows error "E5017: Aborting due to not yet implemented feature: Writing fx_2_0 sampler objects initializers is not implemented" (Wine's HLSL effect compiler). RavenGun's prefix for this title is `ravengun-test-tsr`. **MEASURED.**
- The cabinet I/O board and the gun board are emulated by RavenGun; you do not provide hardware.
- The TeknoParrot core lives only in `Shell.exe`, not in `Transformers2.exe`. Starting `Transformers2.exe` directly stays on "SYSTEM INITIALIZING... LOADING.." for more than 50 s. **MEASURED.**
- 2 minutes of loading at least; a machine with a slow disk or a cold cache takes longer.

## 3. The official start script, or why there is none

The folder has `Launcher/SystemLauncher.exe`, which reads `Launcher.ini` and starts the shell. It is cabinet tooling and RavenGun does not run it; the loader starts `Shell.exe` itself and the shell starts the game. If you find cabinet scripts, read them and take over only what you need; see [Official Start Scripts](Official-Start-Scripts).

## 4. The route we use

Profile (`patches/TransformersShadowsRising/game.ini`):

```ini
[Game]
Type = TeknoParrot
EmulationProfile = TransformersShadowsRising
Executable = shell.exe;Transformers2.exe
[Launch]
Mode = direct
[Loader]
RemoteThread =
PostStartMs = 3000
[Wine]
Prefix = ravengun-test-tsr
Runner = wrapper
[Input]
Route = hid-board
Layout = TransformersShadowsRising
Board = SaeGunBoard
Boards = SaeGunBoard, SaeIoBoard
```

- Double-click: the loader starts `Shell.exe` (OpenParrot loader plus the TeknoParrot core, under Wine); the shell then starts `Transformers2.exe`. The chain was seen to run for 10 min 19 s in one run on 2026-10-13. **MEASURED.**
- `Route = hid-board` is required. `--route tp-shm` does not work, because the core sits in the shell and not in the game process.
- `Board = SaeGunBoard` must stay set even when `Boards` is set: with only `Boards`, the start check rejects the hid-board route and the launch falls back to a script.

## 5. Input

- **Gun (MEASURED).** RavenGun creates a virtual joystick "RavenGun SAE Gun Board" (vendor `0x1209`, product `0x72F0`) through `uinput`; Wine presents it as a HID joystick. The game uses the **first** joystick, so this device must have joystick id 0; otherwise the game picks another device (even the PS Move, which Wine also sees as a joystick) and the crosshair sits in a corner with a dead X axis. Wine stores the id in the registry under `HKCU\System\CurrentControlSet\Control\MediaProperties\PrivateProperties\DirectInput\VID_1209&PID_72F0\Calibration\N`, value `Joystick Id`; `scripts/wine-joyid.sh <prefix> 1209:72F0` sets it.
- **Axis range.** With the full range the crosshair sticks to the edges. An output range of -217..557 with the axes swapped put the crosshair on all grid points within 1.5 % of the screen (measured on the TV, 2026-10-11); the in-game calibration is not needed.
- **I/O board (MEASURED).** RavenGun also creates "RavenGun SAE IO Board" (product `0x72F1`, through `uhid`), because the shell searches for it. With both boards the stage select runs on and the game starts; with only the gun board the stage select froze. It still logged `InitIOBoard : Couldn't find IOBoard device` in earlier runs; the game plays regardless.
- Keys in the app: coin = key 5, START = key 1 (hold about 0.3 s), trigger = left button. The lever is not emulated.

## 6. Timing

- Loading to the title screen and "PRESS START BUTTON" with FREE PLAY: about 1 min 42 s (2026-10-13), about 2.5 min (2026-10-14), about 2 min (2026-10-15). An older note quotes 3.5 to 4 minutes on a cold start. **MEASURED.**
- Played 6.5 minutes in the 2026-10-15 run. The 2026-10-13 run showed about 8.5 minutes of play and five attract restarts. **MEASURED.**
- Frame pacing: not measured; `Transformers2.exe` uses about 55 % CPU while running.

## 7. What we saw on screen

**MEASURED:** "SYSTEM INITIALIZING / LOADING", the title with "PRESS START BUTTON" and FREE PLAY, START opens STAGE SELECT with a countdown and a red crosshair that follows the mouse, then "PULL THE TRIGGER!", score counting up, health bars going down, a continue screen and a boss fight.

## 8. Current state and open questions

- Working via double-click (2026-10-15).
- Open: the cabinet lever ("PUSH THE LEVER") is not emulated.
- Open: the freeze about a minute after START on 2026-10-14 (not seen again in two runs). The shell sends a `SHELL_MSG_CHALLENGE` every 10 s and the last log line before the freeze was a challenge; whether this is related is not proven.
- Open: the in-game test menu, the gun calibration screen, player 2 and recoil to rumble.
- Open: at centre aim the crosshair sits slightly up and left of centre (a scale difference); the axes were adjusted for the grid.

## 9. What we tried and what did not work

- **Starting `Transformers2.exe` alone**: stays on "SYSTEM INITIALIZING".
- **`--route tp-shm`**: does nothing, the core is not in the game process.
- **Only the gun board**: stage select freezes. Adding the I/O board fixed the stage select.
- **Wrong joystick id**: crosshair in a corner (see section 5).
- **Full axis range**: crosshair stuck to the edges.
- **Run 1 on 2026-10-13 did not arm the input route** (a mistake in the run book) so no virtual board existed at all; that run still held the shell and game for 10 minutes.

## 10. What is Linux-specific, and what differs on Windows

- The game needs a Wine prefix with native `d3dx9_43` and `d3dcompiler_43/47` on Linux; on Windows these come with the DirectX runtime.
- The gun is a `uinput` joystick; Wine's per-product joystick-id registry entry decides whether the game sees it first. On Windows the first joystick is whatever is connected; remove other gamepads.
- A `uhid` device has an empty `HID_PHYS`. Whether Wine's SetupDi enumeration lists it is the open question behind the I/O board message; real USB devices have a bus path.
- The cabinet expects `C:\Sega\...` paths; under Wine it works with the prefix and the loader. On Windows a real `C:\Sega` layout would be natural.
- Wine's `fx_2_0` effect compiler is incomplete, hence the native `d3dcompiler` DLLs.

See [Wine Notes](Wine-Notes) and [Running on Linux](Running-on-Linux).

This page covers the game and the loader: what you need to run this title and where it gets stuck.

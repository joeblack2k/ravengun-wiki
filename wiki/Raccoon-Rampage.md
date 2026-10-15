# Raccoon Rampage

**Status:** Working (2026-10-14). A double-click in RavenGun starts the game and it was played to a boss (score 22046, 5:17 min) in mouse mode. Our own core library runs the attract loop only; playing needs the TeknoParrot core library, which the profile uses by default.

## 1. Platform and cabinet

- UNIS PC-based four-player lightgun cabinet. 64-bit Windows executable `RSGame/Binaries/Win64/RSGame-Win64-Shipping.exe` (about 66.5 MB), Unreal Engine 4.26. **INFERRED** from the file.
- Template profile: TeknoParrot `RaccoonRampage` (revision 8), input layout `WartranTroopers`.

## 2. What the game needs

- Your own copy of the game folder; RavenGun ships no games.
- Wine/Proton with DXVK, gamescope not required (fullscreen window).
- GStreamer plug-ins (gst-libav) so that the intro and attract films play: set `[Wine] GStreamerPlugins`. An empty `Content/Movies` folder is no longer needed.
- The cabinet's gun plugin (`RSGame/Plugins/UsbPluginsDll.dll`, 107 exported functions) talks to the gun board; RavenGun provides the cabinet hardware the game expects.

## 3. The official start script, or why there is none

None. On Windows the game is started via TeknoParrot. RavenGun starts it with the chain daemon, `rg-direct`, Wine, OpenParrot loader.

## 4. The route we use

**MEASURED** 2026-10-14:

```ini
[Launch]
Mode = direct

[Wine]
Prefix = ravengun-test-dxvk
DllOverrides = d3d11,d3d10core,dxgi=n,b
Runner = wrapper
GStreamerPlugins = ~/.local/share/ravengun/tools/gst-extra/plugins

[Display]
DisplayMode = Fullscreen Windowed
CustomResolution = 1920x1080

[Input]
Route = tp-shm
Layout = WartranTroopers
```

Per-game environment: `TP_REMOTETHREAD=off` (the loader's default route; with `TP_POSTSTART_REMOTETHREAD_MS` no input arrives).

## 5. Input

Layout `WartranTroopers` (four players): test, service, coin 1/2, menu up/down, per player start, trigger, reload, grenade, aux. Aim is 1 byte per axis at offsets 12..19.

- Mouse mode: trigger = start, aim and shoot; coin = key 5.
- Test menu: TEST (key 0), service (F3) = down, F4 = enter.
- Calibration is stored in the game's save data (`Setting_Hardware.ini`); calibrate once in the test menu.
- Template `[Config]`: `General/Direct Aim Mode = 1`, `Graphics/DisplayMode = Fullscreen Windowed`, 1920x1080.

## 6. Timing

- **MEASURED:** ran 5:17 min on the TV in mouse mode; reached a boss with score 22046.
- The attract loop on the alternative (own) core ran 12 min 50 s without the game stopping (run rr10).
- Boot time: not measured separately. Frame pacing: not measured yet.

## 7. What we saw on screen

UNIS logo, title, splash art, play-demo films and four player HUDs (the attract loop); "Please Insert Coin" shown per player; then play to a boss.

On our own core library the attract shows a red banner: **"The guns are not calibrated, please enter Setting Menu to calibrate!"**. That is the game saying it cannot find the gun board. On the TeknoParrot core library with the same settings the banner is absent.

## 8. Current state and open questions

- Default route plays; our own core library only demos: a TEST press written to the daemon's shared input state does nothing there (the game does not read that state itself).
- Not yet played with the real Move on this route.
- Sound was not judged in the attract run.
- Coin behaviour: on a writable layer player 1 already has saved credits; the HUD cannot show an added coin.

## 9. What we tried and what did not work

- `TP_POSTSTART_REMOTETHREAD_MS`: no input arrives; keep `TP_REMOTETHREAD=off`.
- Our own core library (generic route): attract and films work, no input, calibration banner stays.
- A read-only game folder: coin presses changed nothing; use a writable throw-away layer.
- Films did not play without the GStreamer plug-ins; fixed with `GStreamerPlugins`.

## 10. What is Linux-specific, and what differs on Windows

On Windows: TeknoParrot starts the game. On Linux: Wine/Proton, a DXVK prefix, GStreamer plug-ins for the movies, and the `tp-shm` input bridge. The `Is64Bit = true` profile needs the 64-bit loader.

This page covers the game and the loader: what you need to run this title and where it gets stuck.

# Elevator Action Invasion

**Status:** Working (2026-10-14). Double-click in the app starts the Unreal Engine 4 game under Wine with DXVK and the extra GStreamer plug-ins; played more than 5 minutes with the test pattern (START, intro movie, aim and shoot, Continue, score 50236). The picture is a narrow column in the middle of the screen because the cabinet is a portrait one. Not yet played with a real PS Move.

## 1. Platform and cabinet

- UNIS PC-based cabinet, Windows, 64-bit Unreal Engine 4.26 game.
- Portrait (upright) monitor: the game renders 1080x1920 and RavenGun shows it as a column in the middle of a landscape screen.
- Executable: `ESGame/Binaries/Win64/ESGame-Win64-Shipping.exe`.
- RavenGun ships no games: you need your own copy of the game folder.

## 2. What the game needs

- Wine with **DXVK** (Direct3D 11 on Vulkan) and a set of **GStreamer plug-ins** so the in-game movies play (the same needs as [Raccoon-Rampage](Raccoon-Rampage)).
- RavenGun provides the cabinet hardware the game expects.
- Profile values: `General/FreePlay = 1`, `General/DesiredWidth = 1080`, `General/DesiredHeight = 1920`, `General/AddBlackBorders = 1`, `General/ForceVSync = 1`, `General/DisableHardcodedControls = 1`, `Attraction Doors/Enable = 0`, `Bezel/Enable = 0`, `Border/Enable = 0`.

## 3. The official start script, or why there is none

On the cabinet the game starts with the PC's own boot image; no script is useful on a desktop PC. RavenGun launches the shipping executable itself. See [Official-Start-Scripts](Official-Start-Scripts).

## 4. The route we use

Profile `ElevatorActionInvasion`, emulation profile `WartranTroopers`.

```ini
[Launch]
Mode = direct

[Wine]
Prefix = ravengun-test-dxvk
DllOverrides = d3d11,d3d10core,dxgi=n,b
Runner = wrapper
GStreamerPlugins = ~/.local/share/ravengun/tools/gst-extra/plugins

[Input]
Route = tp-shm
Layout = WartranTroopers
```

- RavenGun builds a local "view" of your game folder automatically (with the loader's `teknoparrot.ini` next to the game), so nothing is written into your game folder.
- Diagnosis from 2026-10-14 (**MEASURED**): the movies need the GStreamer plug-ins, and the game needs DXVK instead of Wine's built-in Direct3D, exactly as Raccoon Rampage does.

## 5. Input

- Layout `WartranTroopers` (shared-memory board image, offset 8 control bits, aim bytes from offset 12).
- Coin key `5`, START key `1` (**MEASURED**: START started the game after the movie).
- Aim and trigger from the PS Move, mouse or controller. Measured with the test pattern: aiming and shooting work.

## 6. Timing

- Boot to attract: not measured separately.
- Played: more than 5 minutes through START, movie, shooting and Continue. **MEASURED.**
- Frame pacing: not measured.

## 7. What we saw on screen

START, an intro movie, the shooting stage, a Continue screen and a final score of 50236. The picture is a narrow column in the middle of the screen (portrait game on a landscape display).

## 8. Current state and open questions

- Open: a real PS Move, player 2.
- Open: the narrow column is by design of the portrait cabinet. Whether you want to rotate your monitor or a compositor to fill it is up to you; no rotation option was tested.

## 9. What we tried and what did not work

Not measured yet beyond the working route. The recipe was taken from another Unreal Engine 4 title that already ran on RavenGun.

## 10. What is Linux-specific, and what differs on Windows

- Windows uses its own Direct3D 11 and Media Foundation; on Linux DXVK and GStreamer fill those roles. Without them you get missing movies or a wrong picture.
- No cabinet monitor rotation: a normal landscape display shows the portrait picture centered with black borders (`AddBlackBorders = 1`).

This page covers the game and the loader: what you need to run this title and where it gets stuck.

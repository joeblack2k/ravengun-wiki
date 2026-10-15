# After Dark

**Status:** Working (2026-10-15). A double-click in the RavenGun app starts the game; attract with its movie, coin, START, two stages (Silent Valley, Castle of Shadows), continue and a score of 69000 were played for 5.5 minutes in mouse mode. Open: the owner heard audio hitches in the first run (before DXVK); not re-checked since.

RavenGun ships no games; you need your own copy of the game folder.

## 1. Platform and cabinet

- UNIS "PC Based" lightgun cabinet (Windows). The game is a Virtools title: `GamePlayer.exe`, 4,814,336 bytes. **MEASURED** from the profile's identification entry; Virtools is **INFERRED** from the DirectInput error text the game prints ("Cannot Initalize Input Manager").
- TeknoParrot template `GameProfiles/AfterDark.xml` revision 3, emulation profile `WartranTroopers` (the shared four-player shooter layout).
- Two-player lightgun game; the default resolution in the profile is 1920x1080.

## 2. What the game needs

- Your own copy of the game folder (it must contain `GamePlayer.exe`).
- **Movies.** The attract movie is a `.wmv`. It plays through Wine's DirectShow, which needs a 32-bit GStreamer (`[Launch] Gst32 = true`, see `docs/gst32.md`) and RavenGun's registry file `data/wmv-asyncreader.reg` (`[Launch] Registry`), which makes `.wmv` use the plain file source and GStreamer splitter instead of Proton's ASF reader. **MEASURED** on a sister title: that ASF reader stops its read threads before releasing its allocators, so the audio thread hangs and the game freezes on the title screen.
- **Graphics.** DXVK (`[Launch] Dxvk = true`) plus Microsoft's `d3dx9_41` (`[Launch] NativeDlls = d3dx9_41`). Without both the 3D world renders black. **MEASURED.**
- **DirectInput.** RavenGun's `rg-compat.dll` (drop-in) gives `IDirectInput::Initialize` a valid instance handle, because Wine rejects a NULL one (`DIERR_INVALIDPARAM`) and the game then stops with "Cannot Initalize Input Manager". **MEASURED.**
- gamescope for full screen.

## 3. The official start script, or why there is none

Not examined; the game starts by running `GamePlayer.exe` directly. If your copy contains cabinet scripts, read them first and take over only what you need; see [Official Start Scripts](Official-Start-Scripts).

## 4. The route we use

```ini
[Game]
Type = TeknoParrot
EmulationProfile = WartranTroopers
Executable = GamePlayer.exe
[Launch]
Mode = direct
Gst32 = true
Dxvk = true
NativeDlls = d3dx9_41
Registry = data/wmv-asyncreader.reg
[Display]
Gamescope = true
[Input]
Route = tp-shm
Layout = WartranTroopers
```

Double-click: `rg-direct` runs Wine with the OpenParrot loader, the `rg-compat.dll` drop-in, 32-bit GStreamer, DXVK and gamescope. No TeknoParrot front-end. The recipe follows Raccoon Rampage (see [Raccoon Rampage](Raccoon-Rampage)). **MEASURED.**

## 5. Input

Layout `WartranTroopers` through `tp-shm`: a 64-byte image, 32-bit button field at offset 8 (test, service, coin 1/2, per player start, trigger, reload, grenade, extra button) and one byte per aim axis at offsets 12..19 (P1X, P1Y, P2X, P2Y, ...), left/top = 0; inside the screen the axes stay at 2..253. In the app: **coin = key 5, START = key 1**, trigger and aim arrive (all **MEASURED**, mouse mode). Reload and the second player were not noted separately.

## 6. Timing

- Played 5.5 minutes in mouse mode on 2026-10-15, with two stages and a continue. **MEASURED.**
- Boot time to attract and frame pacing: not measured yet.

## 7. What we saw on screen

**MEASURED** on the TV: attract with the movie, then after coin and START the first stage (Silent Valley), the second (Castle of Shadows), a continue screen and a final score of 69000. Without DXVK and `d3dx9_41` the world was black.

## 8. Current state and open questions

- Working via double-click (2026-10-15).
- Open: audio hitches heard in the first run (with Wine's own Direct3D); not re-checked after switching to DXVK.
- Not yet played with the real PS Move; player 2 not checked.

## 9. What we tried and what did not work

- **Wine's own Direct3D without `d3dx9_41`**: a black world. DXVK plus Microsoft's `d3dx9_41` fixed it.
- **Default DirectInput**: "Cannot Initalize Input Manager" until `rg-compat.dll` supplied an instance handle.
- **Proton's ASF reader for the `.wmv` movie**: the game freezes on the title (measured on a sister title); the registry file switches to the AsyncReader and splitter.

## 10. What is Linux-specific, and what differs on Windows

- SteamOS has no 32-bit GStreamer; RavenGun links the one from Steam's Proton (`Gst32`). On Windows the system codecs play the movie.
- Wine refuses a NULL `HINSTANCE` in `IDirectInput::Initialize`; Windows accepts it.
- DXVK translates Direct3D 9 to Vulkan; on Windows the native driver is used. Microsoft's `d3dx9_41` is installed natively into the Wine prefix.
- See [Wine Notes](Wine-Notes) and [Running on Linux](Running-on-Linux).

This page covers the game and the loader: what you need to run this title and where it gets stuck.

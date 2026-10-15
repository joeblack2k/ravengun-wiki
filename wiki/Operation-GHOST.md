# Operation G.H.O.S.T.

**Status:** Working (2026-10-15). Double-click in the app starts the game under Wine with 32-bit GStreamer for the movies, native XACT 3.3 for sound and gamescope full screen; JVS over a pipe to the generic Sega gun board. Attract, START, shooting in the train with a rising score; played 5.5 minutes. The picture is 4:3.

## 1. Platform and cabinet

- SEGA RingWide (2012), Windows, 32-bit, executable `gs2.exe`.
- Two-player light gun game.
- RavenGun ships no games: you need your own copy of the game folder.

## 2. What the game needs

- Wine, plus **32-bit GStreamer** (set up once with RavenGun's `setup-gst32.sh`, which links to what Steam's Proton already has) for the DirectShow title movie (`.wmv`).
- The movies need a registry file (`data/wmv-asyncreader.reg`) that selects the GStreamer splitter; **MEASURED:** Proton's own ASF reader hung on Stop.
- **Native XACT 3.3** (`NativeDlls = xactengine3_3`); Wine's builtin one gives an access violation after the sound screen (**MEASURED**).
- RavenGun provides the cabinet hardware the game expects. Region setting in the profile: `PcbRegion = JAPAN` (the game starts and keeps running without any region source; **MEASURED** earlier: alive after 70 s).

## 3. The official start script, or why there is none

The RingWide system software starts the game on the cabinet. RavenGun starts `gs2.exe` itself without scripts: [Official-Start-Scripts](Official-Start-Scripts).

## 4. The route we use

```ini
[Game]
EmulationProfile = SegaJvsGoldenGun

[Launch]
Mode = direct
Gst32 = true
NativeDlls = xactengine3_3
Registry = data/wmv-asyncreader.reg

[Display]
Gamescope = true
AimAspect = 4:3

[Input]
Route = jvs
Board = SegaGun2P
ComPort = COM4
JvsTransport = pipe
```

- Recipe taken from [Lets-Go-Island](Lets-Go-Island): the generic Sega gun board `SegaGun2P` behind the JVS pipe. **MEASURED** (2026-10-15): START, coin and shooting work, the score rises in mission 1.
- gamescope scales the 1024x768 picture to 1440x1080. `AimAspect = 4:3` makes the daemon's aim space follow that picture.

## 5. Input

- START: key `1`. Coin: key `5`. Trigger: mouse or Move trigger. **MEASURED:** START and shooting.
- The board has 14 switch bits and 8 analog channels (0-3 = P1 X, P1 Y, P2 X, P2 Y).
- Calibration: not measured; the game's test menu was not visited.

## 6. Timing

- Early check: started and stayed alive after 22 seconds (own loader) and after 70 seconds. **MEASURED.**
- Played: 5.5 minutes. **MEASURED.**
- Frame pacing: not measured.

## 7. What we saw on screen

The title movie, attract, START and the train mission with a rising score. The picture is 4:3 (the game picks 1024x768).

## 8. Current state and open questions

- Open: real PS Move, player 2, calibration, later missions.
- The game could ask for the region later in play; only `JAPAN` has been tried.

## 9. What we tried and what did not work

- Proton's ASF reader for the `.wmv` movie: hung on Stop. Fixed with the registry entry.
- Wine's `xactengine3_3`: access violation after the sound screen. Fixed with the native DLL.

## 10. What is Linux-specific, and what differs on Windows

- Movies and sound go through GStreamer and a native XACT DLL; on Windows the system DirectShow and XACT are used.
- 32-bit GStreamer is not in SteamOS; RavenGun links Proton's copy.
- The JVS board is a pipe backed by the RavenGun daemon.

This page covers the game and the loader: what you need to run this title and where it gets stuck.

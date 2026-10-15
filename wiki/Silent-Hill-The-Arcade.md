# Silent Hill: The Arcade

**Status:** Working (2026-10-15). A double-click in the RavenGun app starts the game; after a coin and START, stage 1 was played with the lightgun (aim, shoot, reload) for 5.5 minutes, with stereo sound. Open: a 16:9 patch (the game is 4:3) and the e-AMUSEMENT PASS card service; START only starts a game after a coin even though the screen says FREE PLAY.

RavenGun ships no games; you need your own copy of the game folder.

## 1. Platform and cabinet

- Konami "PC Based" cabinet (Windows). `KSHG.exe`, 3,022,848 bytes, PE32 i386 GUI, built 2007-12-20 (PDB path `...\SilentHill\program\Release\KSHG.pdb`). Dump size about 2.5 GB. **MEASURED** from the file.
- Gun game for two players, 640x480, full screen. The game takes no command-line switches; it creates the mutex `SILENT HILL GS` and exits silently if it is already running. Window class `KSHG`. **MEASURED.**
- The cabinet talks to two serial boards through Konami's I/O library `shaiolib.dll`: the **gun board** on `COM1` (19200 8N1) and a **button board** on `COM2` (buttons, coin counter and blocker, IC-card readers, 10-key pads, LEDs). No USB. **MEASURED** from the import table and disassembly.
- The game runs a twelve-step boot self-test: I/O BOARD, GUN I/O, (a cabinet-hardware step RavenGun answers), SYSTEM DATA1, SYSTEM DATA2, DATA1, DATA2, DATA3, CLOCK, SPEAKER, GUN CALIBRATION, e-AMUSEMENT. An error screen can only be left with TEST. **MEASURED.**
- Languages in the dump: `eng`, `fra`, `ita`; region folders under `Data/locale`: `aa ca ea ka ru ua`.
- TeknoParrot template `GameProfiles/SilentHill.xml` revision 16.

## 2. What the game needs

- Your own dump of the game folder.
- The cabinet's I/O boards are emulated: RavenGun supplies a replacement `shaiolib.dll` (source `shaiolib_rg.c`) in the game's folder as a drop-in. It reports the boards present and reads input from shared memory.
- A **32-bit GStreamer** for Wine's DirectShow: the movies (`Data/Movie/*.vid`, 32 files, 507 MB) are bare MPEG-2 video streams, no container, 640x480, 30 fps, played through DirectShow `RenderFile`. Set `[Launch] Gst32 = true` (see `docs/gst32.md`; the script `scripts/setup-gst32.sh` links the 32-bit GStreamer that Steam's Proton already has). The dump's own decoder `clvsd.ax` is not used. **MEASURED:** without it, the game exits cleanly 37 s after start, right after the caution screen.
- A Wine prefix, DirectX 9, DirectSound and gamescope.
- Writable folders: the game writes settings (`setting.1`, `gun.1`, `speaker.1`, `shoprank.lra`), mirrored bookkeeping on `e:` and `f:`, `Data\acdata` and `*.log` files. RavenGun's core redirects drive letters other than C: and Z: to `.\TeknoParrot\<letter>\`, and the view therefore has `Data/TestDat`, `Data/acdata` and the language folders as local folders. Nothing is written to your game folder.
- The game checks a file manifest at boot (`Data/TestDat/KSHG.crc`, 5,946 files, size and CRC16), including `KSHG.exe` on disk, so do not modify those files.
- The e-Amusement service (`libbms.dll`, named pipe `\\.\pipe\bmssvc`) is not running; with the e-Amusement setting off the game continues and shows a ticker saying so.

## 3. The official start script, or why there is none

No cabinet start script was used. `KSHG.exe` starts directly and changes its own working directory to `<start dir>\Data\<language>`; the language comes from the settings file. See [Official Start Scripts](Official-Start-Scripts) for the general reasoning.

## 4. The route we use

```ini
[Game]
Type = TeknoParrot
EmulationProfile = SilentHill
Executable = KSHG.exe
[Launch]
Mode = direct
Gst32 = true
[Display]
Gamescope = true
AimAspect = 4:3
[Input]
Route = tp-shm
Layout = SilentHill
[Config]
General/FreePlay = 1
General/SkipToStage = stage1-1-1
```

- Double-click: `rg-direct` runs Wine with RavenGun's own 32-bit OpenParrot core (generic route; it has no code for this title), gamescope on the TV, and the drop-in `shaiolib.dll`. TeknoParrot's closed core is not loaded. **MEASURED.**
- `AimAspect = 4:3` tells the daemon to map the lightgun's aim space to the 4:3 picture on the 16:9 TV.
- In the attract run a 3-byte in-memory patch (`rg-shaiolib.patches`) removed one call that blacked out the movie area. **MEASURED.**
- Sound: the loader gives Wine a stereo device (`[Audio] Channels = stereo`, `PULSE_PROP=pulse.fix.position='[ FL FR ]'`). Wine's DirectSound mixes badly to a 7.1 HDMI sink: above six channels it skips volume, pan and 3D, and mono buffers leave stale data in the other channels, heard as a buzz on every mono effect. **MEASURED.**
- Region: RavenGun answers as Asia (`GNGHLAAA`, "for sale and use only in Asia excluding Japan and Korea" on screen), chosen because it passes the speaker step without a speaker file. A Europe value (`GKGHLEAA`) needs `Data/TestDat/speaker.1`, which the dump lacks. `RG_SHAIO_MODEL` selects the value. Not tried beyond Asia.

## 5. Input

`[Input] Route = tp-shm`, `Layout = SilentHill` (TeknoParrot's SilentHillPipe format): a bit mask at offset 8 (Test 0x01, Service 0x02, P1 Start 0x04, P1 Trigger 0x08, P1 Option L 0x10, P1 Option R 0x20, Coin 0x40, P2 Start 0x80, ...) and four analog bytes at offsets 12/16/20/24, axes 0 to 255. The replacement library reads that mapping in `rg_poll_inputs()`. **MEASURED** in play.

The library exposes `GUN_status(int[8])` (two guns x x, y, trigger, off-screen), `BUTTON_status(uint8_t[9])` (bit 7 = held, bit 0 = edge) with bytes 0..8 = Test, Service, (unused), Start P1, Start P2, Option L P1, Option R P1, Option L P2, Option R P2, and coin functions. The order was measured in the game's own TEST > I/O CHECK > INPUT CHECK screen; an earlier guess had START and OPTION R swapped.

In the app: coin = key 5, START = key 1, TEST = key 0, aim = mouse or PS Move, trigger = left button, reload with the reload button (**MEASURED**: aim, shoot and reload worked in play). START only starts a game after a coin; not yet explained. The game's own test menu has SOUND, GAME, COIN, NETWORK and IC CARD pages.

## 6. Timing

- Attract run on 2026-10-13: 12 min 15 s of movie-era attract (first attract screen 23:56:21, last capture 00:08:57), ended by our time limit. **MEASURED.**
- Double-click run, 2026-10-15: 5.5 minutes of stage 1. **MEASURED.**
- Frame pacing: not measured.

## 7. What we saw on screen

**MEASURED:** the twelve self-test steps all OK, the region warning, the caution screen, the opening movie, the title, two play demos, the story movies, the Konami logo, the shop-ranking tables and how-to-play screens, with "Press the START button" for both players, the e-Amusement ticker and "FREE PLAY". In play: stage 1, monsters, crosshair following the aim. The picture is 4:3 with black bars.

## 8. Current state and open questions

- Working via double-click (2026-10-15).
- Open: a 16:9 (widescreen) patch.
- Open: the e-AMUSEMENT PASS (card plus network service) is not emulated.
- Open: why START needs a coin although FREE PLAY is shown.
- Open: the AMD fix TeknoParrot offers ("EnableAmdFix", invisible enemies) was not examined.
- Open: the Europe region value; player 2; the real PS Move.

## 9. What we tried and what did not work

- **Konami's own `shaiolib.dll`**: LOW CONTROL ERROR 5-1500-0011 ("PC and an I/O board cannot be communicated"); replaced by RavenGun's library.
- **No 32-bit GStreamer**: Wine failed to create every splitter (`hr 0x8007000e`), `RenderFile` returned `0x80040218` and the game exited with code 0 after 37 s. A 32-bit GStreamer from GE-Proton 10-34 (plus `libvpx.so.6` from the Steam runtime) fixed it.
- **Black movie area**: removed by a 3-byte in-memory patch.
- **A swapped button table**: START and OPTION R were swapped until measured in the INPUT CHECK screen.
- **7.1 sound**: a buzz on every mono effect until the loader gave Wine a stereo device.

## 10. What is Linux-specific, and what differs on Windows

- SteamOS has no 32-bit GStreamer, so Wine's DirectShow cannot decode MPEG-2; RavenGun links the one in Steam's Proton. On Windows the system codecs do it.
- Wine's DirectSound handles 7.1 outputs poorly; force a stereo device.
- Serial boards on `COM1`/`COM2` do not exist on a PC; the replacement `shaiolib.dll` takes their place. On Windows you would need the same replacement or real hardware.
- Drive letters `e:` and `f:` are redirected by the core into the game's folder on Linux; on Windows they would be real drives.
- Full screen on the TV runs through gamescope.

See [Wine Notes](Wine-Notes) and [Running on Linux](Running-on-Linux).

This page covers the game and the loader: what you need to run this title and where it gets stuck.

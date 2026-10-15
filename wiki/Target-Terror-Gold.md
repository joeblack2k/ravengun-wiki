# Target: Terror Gold

**Status:** Working (2026-10-15). Runs natively on Linux from a double-click: title, START, Mission Select, 5.5 minutes played, shots arrive (reload, enemies go down). The picture is 4:3 and aiming on a 16:9 TV has no pillarbox correction yet.

## 1. Platform and cabinet

- Raw Thrills Linux PC-based cabinet. The game (`game`, 32-bit i386 ELF, about 1.2 MB) is a plain, ordinary Linux program (**MEASURED**: standard dynamic loader, no custom loader needed).
- Two-player lightgun cabinet; the game draws a 1024x768 (4:3) picture.
- Template profile: TeknoParrot `TargetTerrorGold` (revision 12), emulation profile `RawThrillsGUN`.

## 2. What the game needs

- Your own dump of the game folder; RavenGun ships no games.
- The game folder brings its own cabinet-board emulator: `tt_emu.so` and `libXshooter.so`. RavenGun uses them as they are.
- 32-bit libraries `libglut.so.3`, `libXi.so.6`, `libGLU.so.1` (staged by RavenGun's `--stage-libs` step).
- A virtual lightgun with a USB physical path (section 5).

## 3. The official start script, or why there is none

The cabinet starts the game with `runGame.sh`: `LD_PRELOAD=./tt_emu.so ./game`. A second script, `tt_daemon.sh`, creates the serial link between `/dev/ttyS0` and `/tmp/ttyJamma` with `socat`. RavenGun does both itself: the preload is set by the engine and the serial link is made by `librg_ptylink.so` (`RG_PTYLINK=/dev/ttyS0=/tmp/ttyJamma`).

## 4. The route we use

**MEASURED** 2026-10-15: native Linux route (bubblewrap sandbox), no Wine.

```ini
[Game]
Type = ElfLdr2
[Input]
Route = evdev
[Display]
AimAspect = 4:3
```

Engine settings (from `packaging/native-games.json`): resolution `1024x768`, launched in gamescope, `LD_PRELOAD=librg_ptylink.so:tt_emu.so`, and `TTG_FULLSCREEN=1`, `TTG_CROSSHAIR=1`, `KBD_HOOK=/dev/input/ravengun-kbd`. Your game folder is mounted read-only with a local write layer. The `[Display] AimAspect = 4:3` line makes the daemon's aim space follow the 4:3 picture in the middle of the 16:9 TV.

## 5. Input

- **Keys** (virtual keyboard `KBD_HOOK=/dev/input/ravengun-kbd`): 1/2 = START, 5/6 = coin, 7 = service, 8 = test, 0 = banknote, arrow up/down = volume.
- **Guns**: the virtual lightguns of the daemon. `libXshooter` reads `Xshooter.ini` from the game's working directory; RavenGun supplies it:

```ini
P1_DEVICE_NAME=RavenGun Virtual Lightgun
P1_DEVICE_VID=1209
P1_DEVICE_PID=7202
P2_DEVICE_NAME=RavenGun Virtual Lightgun P2
P2_DEVICE_VID=1209
P2_DEVICE_PID=7203
```

**Requirement (MEASURED):** `libXshooter` only accepts input devices with ABS_X/ABS_Y, BTN_LEFT/RIGHT/MIDDLE and a physical path starting with `usb`. The virtual gun therefore reports a phys path `usb-ravengun/inputN`.

## 6. Timing

- Played 5.5 minutes (**MEASURED**).
- Boot time and frame pacing: not measured yet.

## 7. What we saw on screen

Title, START, Mission Select, then play; shots registered, reloading worked, enemies went down. The 4:3 picture sits in the middle of the 16:9 screen.

## 8. Current state and open questions

- Aiming on a 16:9 TV spans the whole TV; there is no pillarbox correction yet, so the crosshair is stretched relative to the 4:3 picture.
- Sound (OSS `/dev/dsp`) was not measured.
- Whether `libXshooter` compares the device name exactly or as a prefix, and whether VID/PID are read as lower-case hex, is not measured (`XSHOOTER_DBG=1` makes it print what it finds).

## 9. What we tried and what did not work

Without the `usb` physical path on the virtual gun, `libXshooter` ignores the device and no shots arrive.

## 10. What is Linux-specific, and what differs on Windows

This is a Linux game with no Windows build: the whole route is Linux-native. The TeknoParrot template exists, but RavenGun's route uses the game's own board emulator and the virtual evdev guns instead.

This page covers the game and the loader: what you need to run this title and where it gets stuck.

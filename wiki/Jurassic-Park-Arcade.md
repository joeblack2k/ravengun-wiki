# Jurassic Park Arcade

**Status:** Working (2026-10-14). Native Linux on RavenGun's own loader: double-click in the app, OpenGL on Vulkan (Mesa zink). The light gun board answers as the real USB board through the RIO bridge, so "RIO Disconnected" is gone. Played with a PS Move (54 kills in one session) and with a mouse. Not measured: player 2's trigger.

## 1. Platform and cabinet

- Raw Thrills Linux PC-based cabinet; the game (version 1.08 was tested) is a 32-bit Linux ELF (`game`).
- Upright cabinet type (the game's compressor routine messages about a motion cabinet are harmless).
- Light gun board: Raw Thrills "RIO" USB board, USB id `0c70:0780`.
- RavenGun ships no games: you need your own copy of the game folder.

## 2. What the game needs

- Fixed paths: the game expects its folder at `/pm`. RavenGun mounts your game folder there in a sandbox, with a local write layer on top; nothing is written to your game folder.
- 32-bit Linux libraries that SteamOS does not have: RavenGun provides them.
- RavenGun provides the cabinet hardware the game expects (the RIO board is emulated, see section 5).
- OpenGL: the game only knows OpenGL. RavenGun runs it on Vulkan through Mesa zink (the project's preference; removing the zink variables gives plain OpenGL).
- udev rules file for the USB mount (`/etc/udev/rules.d`), supplied by RavenGun from `patches/JurassicPark/data/udev-rules.d`.

## 3. The official start script, or why there is none

On the cabinet the game is started by the Raw Thrills OS (`go.sh`, `xinit`, a run script). You cannot reuse that on a desktop. The RavenGun engine starts the game itself (no scripts): gamescope, then a sandbox, then RavenGun's own ELF loader, `rg-elfloader`. See [Official-Start-Scripts](Official-Start-Scripts).

## 4. The route we use

```ini
[Game]
Profile = JurassicPark
EmulationProfile = RawThrillsGUN
Executable = game

[Input]
Route = tp-shm
Layout = RawThrillsGUN
```

- Native route entry in `patches/<Game>/native.json` (the Jurassic Park folder under `patches/`) (`arch = i386`, `loader = rg-elfloader`, `launcher = gamescope`). **MEASURED** (2026-10-14): the process chain is `gamescope -> bwrap -> rg-elfloader`, with `rg-exec --keep DISPLAY` in between so that the game only sees the display variable. A first try without that loaded gamescope's Vulkan layer into zink and showed "Gamescope WSI Layer Error".
- The executable is in a layout the system loader cannot start; RavenGun's own loader maps it. `force_glsl_version=120` must stay off (it crashes).
- **Shader fix (MEASURED):** every boot logged `Failed to load shader: shader108 / 108d / 108c_sk / 108d_sk`. Mesa refuses glow shaders that write both `gl_FragData` and `out_Bloom`; the cabinet's NVIDIA driver allowed it. RavenGun ships replacement shader files (`data/shaders`) bound over the originals in the sandbox. Glow on hit targets is visible afterwards.
- Harmless log noise: card reader messages (`xicoOpenPort`, `msr100OpenPort`), missing `ifconfig` / `nvidia-settings`.

## 5. Input

The game takes the board as events from a USB read thread, not by polling. RavenGun's **RIO bridge** (`librg_rio_bridge.so`, 32-bit, table `rio-invoer.ini`) answers as the board itself: the game opens the USB device, reads 64-byte input reports every 4 ms, and gets a report built from the daemon's board image. The game's own messages to the board are accepted. The per-game table lists addresses, report layout and which switch id means what.

**MEASURED switch ids:** 7 = player 1 START ("Player 1 joined. Game Started"), 8 = player 2 start, 0/1 = coins, 3 = TEST (diag menu), 5/6 = volume, 15 = player 1 trigger, 13 = player 1 grenade, 12 = player 2 grenade. Lightgun channels 19/20 = P1 X/Y, 21/22 = P2 X/Y, range 0..4095; P1 Y is inverted (an owner test with a Move showed up/down swapped before the fix).

Controls:

- START: key `1`; coin: key `5`. TEST is a board switch (id 3); holding it opens the diag menu.
- Mouse: left button = trigger (also joins and continues), right = reload, middle = grenade.
- PS Move: trigger and START as mapped by the app.
- In free play the trigger alone joins the game and picks the mission.
- The game's own settings (free play, difficulty 3, volumes 80/50, ...) are editable in the app (Properties, Options); Apply writes the game's own volume files in the local write layer. The country setting is not in the app yet.

## 6. Timing

- Double-click to attract: about 30 seconds (13:00:06 to 13:00:36). **MEASURED.**
- Attract ran 7 min 21 s without a crash. Final app-started run: double-click, attract, join, mission, 22 kills, death, back to attract, alive after 6 min 21 s. **MEASURED.**
- Frame pacing: not measured; no serious graphics fault was seen.

## 7. What we saw on screen

Raw Thrills attract, "Choose your mission", firing with laser to the crosshair and a rising score (0, 50, 1025, streaks up to x46 with the Move), power-ups, deaths and Continue.

## 8. Current state and open questions

- Not measured: player 2's trigger id (16 or 17 are candidates, so a second gun does not fire yet), a physical mouse (tests injected events into a real mouse device), reload/grenade in play, coin with free play off, service as a separate switch, P2 Y direction.
- Sound: no sound can be a system problem. On one test machine the HDMI 7.1 output had front left/right at 0 %, so every stereo stream was silent; set all eight channels to 100 % (`pactl set-sink-volume <sink> 100%` for each channel) and check the game's stream first. **MEASURED.**
- Gun rumble sound system (OSS) only drives the guns' rumble and is not started while rumble is off.

## 9. What we tried and what did not work

- The polled way (replacing board-read functions, as for [NERF-Arcade](NERF-Arcade)) cannot work here because this game reads events; hence the USB-level bridge.
- An earlier attempt to run the Linux game through a Windows-based loader under Wine did not get it past start-up, so that route was dropped (earlier notes, not re-measured).

## 10. What is Linux-specific, and what differs on Windows

- The game is a Linux program; there is no Windows version. The cabinet OS is replaced by a sandbox with fixed paths, 32-bit libraries, an ELF loader, the udev rules file and the RIO bridge.
- OpenGL runs through zink; NVIDIA-only shader behaviour had to be corrected for Mesa.
- Same RIO board and bridge as NERF Arcade; only the attachment differs.

This page covers the game and the loader: what you need to run this title and where it gets stuck.

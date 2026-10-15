# Too Spicy

**Status:** Working (2026-10-15). Runs natively on Linux through RavenGun's Lindbergh route; 5.5 minutes played in mouse mode. It needs the stack-alignment shim and a small sound-library stub.

## 1. Platform and cabinet

- SEGA Lindbergh (Type 3 board), Linux PC. The game ELF is `elf/apacheM.elf` (32-bit i386, about 6.5 MB). The library item is called "Too Spicy" and selects the profile `2Spicy`.
- Template profile: TeknoParrot `2Spicy`, emulation profile `TooSpicy`.

## 2. What the game needs

- Your own dump of the game folder; RavenGun ships no games.
- `lindbergh.so` from lindbergh-loader (built locally by RavenGun's script) and `libCg.so` 2.0 for the shaders.
- `librg-stackalign.so`: the old i386 code gets a 16-byte aligned stack into SteamOS's GL libraries. Without it the game crashed on `movaps %xmm0,0xc(%esp)` in `libGLdispatch.so.0` (**MEASURED**).
- A stub `libsndio.so.7`: the bundled OpenAL asks for it; the stub makes `sio_open` fail so OpenAL falls back to Pulse/ALSA.
- RavenGun provides the cabinet hardware the game expects.

## 3. The official start script, or why there is none

The cabinet's Lindbergh system starts the ELF. RavenGun's engine replaces lindbergh-loader's starter.

## 4. The route we use

**MEASURED** 2026-10-15:

```ini
[Game]
Type = Lindbergh
[Input]
Route = jvs
Board = Lindbergh
```

Engine: `lindbergh.so` plus `librg-stackalign.so` in `LD_PRELOAD`, 1280x768, Mesa zink on RADV (remove `MESA_LOADER_DRIVER_OVERRIDE` and `LIBGL_KOPPER_DRI2` for radeonsi). `lindbergh.ini`: `INPUT_MODE = 1`, `REGION = EX`, `FREEPLAY = none`, `GPU_VENDOR = 2`, `KEEP_ASPECT_RATIO = true`, `HIDE_CURSOR = true`.

## 5. Input

Daemon plays the JVS gun board. Mouse mode: coin = 5, START = 1, trigger to shoot, aim off screen to reload. Calibrate through the game's test menu if the crosshair is off.

## 6. Timing

- Played 5.5 minutes (**MEASURED**).
- First start is longer because the shaders are recompiled; time not measured.

## 7. What we saw on screen

Attract and play in mouse mode; no detailed shot list was kept.

## 8. Current state and open questions

- Real Move and two-player play not recorded.
- Gun outputs (lamps, recoil) are not mapped yet.

## 9. What we tried and what did not work

Crash at startup in `libGLdispatch.so.0` until the stack-alignment shim was added; OpenAL initialisation failed until the `libsndio` stub was added.

## 10. What is Linux-specific, and what differs on Windows

Linux-only route. On Windows the game runs through TeknoParrot's Lindbergh emulation; here lindbergh-loader's layer, JVS pass-through, zink, the alignment shim and the sound stub replace that.

This page covers the game and the loader: what you need to run this title and where it gets stuck.

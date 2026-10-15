# Mario Kart: Arcade GP DX

**Status:** Working (2026-10-15). Double-click in the app starts the game under Wine without any loader UI: 16 MiB stack, DXVK, a view link for one shader file and a repair of one Direct3D call. Played 5.5 minutes with a gamepad (two races): Item (A) starts and confirms, left stick steers, RT gas, LT brake; the cabinet is on free play. Open: the camera and Banapass cards.

## 1. Platform and cabinet

- Namco ES3A, 32-bit Windows, executable `MK_AGP3_FINAL.exe` (about 7.4 MB).
- Version in the tested folder: 1.18.16 (**INFERRED** from the folder layout). The profile follows the loader template `MKDX118` revision 12 (hand-copied because the template name differs from the folder name).
- Steering wheel, gas and brake pedals, Item button, Mario button, Banapass card reader, a camera for the player photo.
- RavenGun ships no games: you need your own copy of the game folder.

## 2. What the game needs

- Wine with DXVK (`[Launch] Dxvk = true`; Direct3D 10/11 through Vulkan).
- A 16 MiB main-thread stack instead of the 1 MiB in the executable header.
- RavenGun provides the cabinet hardware the game expects (the Namco I/O board with its own commands, network authentication in the loader core).
- Optional: a camera (see section 8).

## 3. The official start script, or why there is none

On the cabinet the game is launched by the cabinet's own software. RavenGun starts it directly (`rg-direct`), no TeknoParrotUi. The loader's UI does only one extra thing for this game on Windows: it ends old game processes; RavenGun's own start does that on every stop. See [Official-Start-Scripts](Official-Start-Scripts).

## 4. The route we use

```ini
[Launch]
Mode = direct
StackReserve = 16M
Dxvk = true
ViewLinks = Data/System/Shader/Polygon2D_D3D10.fx -> Data/System/Shader/Polygon2D_D3D10.cfx

[Display]
Gamescope = true

[Input]
Route = jvs
Board = MKDX
Layout = MKDX
JvsTransport = pipe
```

Each setting exists because of a measured failure:

- **`StackReserve = 16M`:** RavenGun makes a local copy of the executable in its view of your game folder with a 16 MiB stack; your game folder is not changed. **INFERRED** cause of an early stop 27 seconds after start (the main thread ran out of its 1 MiB stack while loading).
- **Default loader route** (`RemoteThread = off`): the loader loads its core on the main thread. The "parked entry point" route made the game jump into the middle of an instruction (illegal-instruction crash); it is not used.
- **`ViewLinks`:** the game compiles one effect from HLSL source with Direct3D's effect compiler, which Wine cannot do (error `0x80004001`). The game also ships the precompiled `.cfx`; in the view the `.fx` path is a link to the `.cfx` (**MEASURED**: works).
- **`rg-mfcam.dll`** (drop-in, preloaded): repairs the `pHResult` output of `D3DX10CreateEffectFromFile*` and `...ShaderResourceView...` so the game does not read stack garbage as an error (**MEASURED**: after the repair the game ran on instead of exiting around 3 minutes into attract).
- **`Dxvk = true`:** with Wine's own OpenGL Direct3D, the whole 2D layer (text, menus, "FREE PLAY") was missing and the log filled with GL errors; with DXVK v2.7.1 everything is drawn (**MEASURED**).
- **Gamescope:** fills the screen (the profile is windowed 1360x768).
- Network: the loader writes `[Network]` settings into `teknoparrot.ini`; by default they point at the loader community's server for online play. For offline play set `Network/ServerAddress = 127.0.0.1` in your user layer (an offline start was not measured).

## 5. Input

JVS over the pipe `TeknoParrot_JVS` to RavenGun's board `MKDX` (Namco commands, 24 switch bits). Analog: channel 0 = steering, 1 = gas, 2 = brake.

Gamepad (`[Gamepad]`, assign in the app under Controllers, Gamepads): `LeftX = wheel`, `RT = gas`, `LT = brake`, `A = trigger` (Item), `B = reload` (Mario button), `X = grenade` (Enter, menu), `Y = aux1` (Banapass card), `LB/RB` and d-pad up/down = Menu Up/Down, `Start = start`, `Back = coin`, right stick click = Test (`F2`).

- Item (A) starts the game and confirms; left stick left/right moves in menus (**MEASURED**).
- No START is needed in free play. Coins count on the board but the game shows no credits.
- Banapass card: sets bit 0 of offset 8 of the shared memory (layout `MKDX`) and the card bit of the JVS board.

## 6. Timing

- Without the fixes the game stopped after about 27 seconds, then after about 3 minutes (section 4).
- Working run: 5.5 minutes, two races, "Continue?" and a new character selection. **MEASURED.**
- Frame pacing: not measured.

## 7. What we saw on screen

Attract with "FREE PLAY", the Banapass question, character selection, Grand Prix and 50cc, two races, the slot chance and "Continue?".

## 8. Current state and open questions

- **Camera:** the attract says the camera is not available. The game uses Media Foundation, and Wine has no cameras. RavenGun's daemon can feed its own camera (`[Camera] Use = game`, the PS Eye) into the game through `rg-mfcam.dll`, but the game never asked for a camera in the measured runs (it may be disabled in the game's own settings; not investigated).
- **Banapass:** "cards cannot be bought now". Playing without a card works.
- Direction and range of the wheel channel, whether pedals use the full 0..255 range: not measured.
- A JVS report mismatch on one Namco block (report 03 where the original loader answers 01) did not affect play.

## 9. What we tried and what did not work

- Plain start: stopped after 27 seconds (stack).
- "Parked entry point" route: illegal-instruction crash in the middle of a startup instruction (a race between the loader core and the main thread).
- Wine's own OpenGL renderer: no 2D layer.
- Compiling the `.fx` on Wine: not implemented, hence the link to the `.cfx`.

## 10. What is Linux-specific, and what differs on Windows

- Wine lacks Media Foundation cameras and parts of the Direct3D effect compiler; both were worked around.
- On Windows the game's `F:` and `G:` drive paths are real; the loader maps them to a local folder, so nothing is written to your game folder.
- Use the loader's default route on Linux rather than the parked entry point.

This page covers the game and the loader: what you need to run this title and where it gets stuck.

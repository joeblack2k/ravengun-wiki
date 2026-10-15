# Wine notes

This page lists the Wine and Proton problems you are likely to meet when you run these Windows titles on Linux, each as symptom, cause and the setting that fixes it. Every setting is a key in the game's `game.ini` profile (the shipped one, or your own copy under `~/.local/share/ravengun/patches/<Game>/game.ini`, which wins per key). RavenGun ships no games; you need your own copy of each title.

Labels: **MEASURED** (seen or measured on the bench), **INFERRED** (derived from files or traces), and "assumption" (not tested). The route itself is described on [Loader-Architecture](Loader-Architecture); general Linux advice is on [Running-on-Linux](Running-on-Linux).

## Which Wine

The direct route starts a plain Wine build, not the `proton` launcher script (**MEASURED**: a profile that names a Proton runner is refused with "use plain Wine"). The default is a Wine taken from a Proton release (`proton-11.0-2`) under `~/.local/share/ravengun/wine/`. Several fixes below borrow pieces from a Proton install that Steam already has (GStreamer, DXVK, the DirectX redistributable). They never copy or download games, and nothing is written into your game folder: files that must sit next to the executable go into a local "view" of the game folder (a folder of symbolic links).

## 32-bit movies: `[Launch] Gst32`

- **Symptom:** a 32-bit game stops right after a movie starts. The log shows `err:quartz:autoplug Failed to create filter for "GStreamer splitter filter", hr 0x8007000e`, then a NULL read and exit. **MEASURED** on Bug Busters, right after MODE SELECT.
- **Cause:** Wine plays DirectShow movies (`.mpg`, `.m1v`, `.avi`, `.wmv`) through GStreamer, and a 32-bit game needs a 32-bit GStreamer. SteamOS does not ship one; Steam's Proton does.
- **Setting:**

```ini
[Launch]
Gst32 = true
```

Run `scripts/setup-gst32.sh` once (the installer does this). It only makes links into what Steam already has, in `~/.local/share/ravengun/gst32/`: the newest Proton with `libgstlibav` (GE-Proton preferred; only GE-Proton also has the MPEG program-stream demuxer), the plug-ins, and the few libraries those plug-ins want from the Steam Linux Runtime. Run it again after a Proton update. If the folder is missing the game does not start and the message names the script.

What the loader does for you: it puts the 32-bit libraries first in `LD_LIBRARY_PATH`, points `GST_PLUGIN_SYSTEM_PATH_1_0` at the plug-in links and gives GStreamer its own registry file.

**Under gamescope.** `/usr/bin/gamescope` carries a file capability, so the dynamic linker runs it in secure-execution mode and strips `LD_LIBRARY_PATH`, `LD_PRELOAD` and `LD_AUDIT` from its environment, including the game's. RavenGun therefore re-applies them after the `--`, through `/usr/bin/env`. **MEASURED** on Operation G.H.O.S.T.: without this Wine reported `failed to load .../winegstreamer.so: libgstaudio-1.0.so.0: cannot open shared object file` and the title movie failed with `0x8007000e`.

**Movies that still freeze.** Some WMV movies freeze in Proton's ASF reader when the graph is stopped (**MEASURED** on Operation G.H.O.S.T. and After Dark: the main thread waits for the reader to report "stopped"). The fix is a small registry file that sends `.wmv` to the plain file source with Wine's GStreamer splitter:

```ini
[Launch]
Registry = data/wmv-asyncreader.reg
```

The file lives in the game's own profile folder and is imported once per prefix (a marker records the hash). The prefix is usually shared, so keep such keys narrow. See [Operation-GHOST](Operation-GHOST) and [After-Dark](After-Dark).

## Direct3D: `[Launch] Dxvk`

- **Symptom:** menus and text are missing, the screen goes black after a button, or the log fills with `GL_INVALID_OPERATION in glDrawArraysInstanced`. **MEASURED** on Mario Kart Arcade GP DX: 144,000 such lines, no 2D layer, no "FREE PLAY".
- **Cause:** Wine draws Direct3D 8 to 11 with wined3d (OpenGL), which some games do not tolerate. DXVK draws the same calls through Vulkan.
- **Setting:**

```ini
[Launch]
Dxvk = true
```

This is per game; the shared prefix is not touched. RavenGun places `d3d8.dll`, `d3d9.dll`, `d3d10core.dll`, `d3d11.dll` and `dxgi.dll` next to the executable in the view and sets `WINEDLLOVERRIDES` to native for them. A drop-in of your own with the same name wins. DXVK is found in this order: `RAVENGUN_DXVK`, `~/.local/share/ravengun/dxvk/current` (fetched with `scripts/fetch-dxvk.sh`), then the newest DXVK inside a Steam Proton. With DXVK v2.7.1 the menus, character select and race of Mario Kart Arcade GP DX appear (**MEASURED**).

**DXVK is not always the answer.** On Night Hunter - After Dark, Chapter 2 the game stayed on "Initializing..." with DXVK (the AVPro video never arrived as a Direct3D 11 texture) and ran with Wine's own Direct3D 11 (**MEASURED**). Try both. See [Night-Hunter-After-Dark-Chapter-2](Night-Hunter-After-Dark-Chapter-2).

## Microsoft DLLs instead of Wine's: `NativeDlls`

- **Symptom (After Dark):** large parts of the world render black (buildings, vehicle, enemies), even with DXVK. **MEASURED.**
- **Cause:** the game builds its materials with `D3DXCreateEffect` from `.fx` sources, and Wine's built-in `d3dx9_41` cannot translate those effects. **INFERRED** from the trace. With Microsoft's own `d3dx9_41` plus DXVK everything is textured (fur, claws, village). **MEASURED.**
- **Setting:**

```ini
[Launch]
Dxvk = true
NativeDlls = d3dx9_41
```

The code reads this key from `[Launch]`, and the shipped After Dark profile uses it there. Some pages and older notes say `[Wine]`; if your copy has it in `[Wine]` it is ignored.

Run `scripts/setup-redist.sh` once. It extracts the DirectX redistributable that Steam already installed (`Steamworks Shared/_CommonRedist/DirectX/Jun2010`) into `~/.local/share/ravengun/redist/{x86,x64}/`. Nothing is downloaded and nothing goes into git. For each DLL listed, RavenGun copies it into `system32` (64-bit) or `syswow64` (32-bit) of the game's prefix, keeps Wine's own once as `<name>.dll.wine-bewaard`, and adds `<name>=n` to `WINEDLLOVERRIDES`. Other games in a shared prefix keep Wine's version because the override is per run.

Other uses, all **MEASURED**:

- Operation G.H.O.S.T.: `NativeDlls = xactengine3_3`. With Wine's XACT the game crashed after the sound check screen with an access violation in an XACT thread; with Microsoft's XACT 3.3 it reaches attract.
- Friction: `NativeDlls = d3dx9_42, d3dcompiler_42` (see [Friction](Friction)).

If the DLL is not in `redist/` the game does not start and the message names the script.

## Fullscreen and the window: gamescope

```ini
[Display]
Gamescope = true
```

Wine games that go fullscreen on their own often fight the compositor or open at the wrong size. With `Gamescope = true` the game runs in a gamescope window (`-W <w> -H <h> -S fit -f`) at the resolution given by `[Display] GamescopeResolution` (the display's size when empty; assumption). Optional keys: `GamescopePath`, `GamescopeBackend` (`headless` for runs without a screen). A second executable in a profile (a platform daemon, for example) runs outside gamescope because it has no window. Profiles whose original setting asks for windowed mode get a windowed override under gamescope.

Known side effect: with gamescope a game can hang in a window-update loop that it does not hit without it (see `RG_COMPAT_PAINT` below). **MEASURED** on Far Cry Paradise Lost: hung in `UpdateWindow` under gamescope, in `ChangeDisplaySettings` without it. See [Far-Cry-Paradise-Lost](Far-Cry-Paradise-Lost).

For a 4:3 picture on a 16:9 TV, `[Display] AimAspect = 4:3` (or `1024x768`) tells RavenGun to map the gun's aim space onto the visible picture only (pillarbox or letterbox) and to restore it when the game ends.

## Audio: why Wine games get a stereo device

- **Symptom:** a buzz on every mono sound effect, or no volume and pan control, when the system output is a 7.1 device (typically HDMI). **MEASURED** on [Silent-Hill-The-Arcade](Silent-Hill-The-Arcade) over HDMI 7.1.
- **Cause:** Wine's DirectSound in `proton-11.0-2` mixes badly to an eight-channel output. Above six channels (its `DS_MAX_CHANNELS`) it skips volume, pan and 3D processing. A mono buffer writes only channel 0, so the other seven channels keep stale data from the mixing buffer, and that data repeats every mix period. That repetition is the buzz. **MEASURED** (symptom and channel count); the mixing-buffer mechanism is **INFERRED** from reading Wine's DirectSound code.
- **Fix:** RavenGun gives Wine games a stereo device by setting

```
PULSE_PROP=pulse.fix.position='[ FL FR ]'
```

`winepulse` probes the device format with a stream that requests fixed channels, and `pipewire-pulse` answers that probe with the layout from this client property. The game therefore sees two channels and the mixer works. If you already set `PULSE_PROP` yourself in `[Env]`, yours wins.

Per game you can change this:

```ini
[Audio]
Channels = stereo     ; default
; Channels = 5.1      ; PULSE_PROP=pulse.fix.position='[ FL FR FC LFE RL RR ]'
; Channels = native   ; set nothing, Wine sees the real device
```

Use `5.1` for a title that really mixes surround and a 5.1 speaker setup. Use `native` only when the output has six channels or fewer. This applies to the direct Wine route only; native Linux titles use their own sound path.

## rg-compat: small fixes inside the game process

`rg-compat.dll` is a drop-in (`Preload = true`) that the OpenParrot loader loads into the game process after the core. Each fix acts only in exactly the situation it solves and otherwise passes the call through unchanged; there is no per-game name or address in it. The loader takes **one** preload DLL, so a game that already has another preload drop-in cannot also have rg-compat.

| Fix | What Wine does differently | Seen on |
|---|---|---|
| `GDI32!GetCharABCWidthsA` guard | with a Japanese font it writes two ABC structures where the game has room for one (buffer overrun) | a Japanese-font title on the bench (not on this wiki) |
| `IDirectInput::Initialize(NULL, ...)` accepted | Wine rejects an empty `HINSTANCE` with `DIERR_INVALIDPARAM`; the Virtools player then stops with "Cannot Initalize Input Manager" | After Dark |
| `UpdateWindow` plus `DispatchMessageA/W`, only with `RG_COMPAT_PAINT=1` | `UpdateWindow` keeps sending `WM_PAINT` until the window is valid (Windows sends it once) | Friction in a window under gamescope: looped in `UpdateWindow`; with the fix "LOADING LEVEL" appears |

The paint fix is opt-in because it changes message handling; enable it with `RG_COMPAT_PAINT = 1` in the game's `[Env]` section.

### The measuring thread: `RG_COMPAT_SAMPLE`

To find out where a hung game is stuck without a debugger, set `RG_COMPAT_SAMPLE=<ms>` in `[Env]`. A thread then pauses the other threads briefly every `<ms>` milliseconds, reads each instruction pointer and, every 5 seconds, writes the most frequent places per thread as `module+RVA` to the file named by `RG_COMPAT_SAMPLE_LOG` (a Windows path such as `Z:\tmp\sample.txt`; default `%TEMP%\rg-compat-<pid>.txt` in the prefix).

- The first column (the program counter) is reliable. A hit in `ntdll` or `win32u` is usually the return of a system-call stub; look the name up in that DLL's export table (`ntdll+0xd110` was `NtWaitForSingleObject` and `win32u+0x11f28` was `NtUserRedrawWindow` in Proton 11).
- The caller columns are a stack scan, not a real unwind: often right, sometimes noise (constants such as 0x989680, or addresses in data). Check with `objdump` that a `call` precedes the address.
- Do not combine it with `WINEDEBUG=+seh`: every context read writes a trace line.

**MEASURED** with it: Far Cry Paradise Lost waited in `UpdateWindow` under gamescope; Wartran Troopers' main thread waited for its "MAIN LOOP" thread, which was simply running frames.

**Without a debugger, perf also works.** `perf record -e cpu-clock:u -p <pid>` when `perf_event_paranoid` is 2 (**MEASURED**); PE modules have no symbols for perf, so a MSVC `.map` file next to the executable is needed to turn addresses into names. Wine's own `winedbg` is not a good fit here: it disturbs the games, and attaching to other processes is restricted on a normal install.

## Other options you may meet

- `[Launch] StackReserve = 16M`: the main thread of a Windows game gets exactly the stack size from its PE header (often 1 MiB). If that is too small, RavenGun makes a local copy of the executable in the view with a bigger stack reserve (only that header field and four padding bytes change). Used for Mario Kart Arcade GP DX.
- `[Wine] DllOverrides = winhttp=n,b`: needed where a plug-in is loaded by a `winhttp.dll` proxy in the game folder (Unity BepInEx/doorstop titles); without it Wine uses its own `winhttp`.
- `[Wine] GStreamerPlugins`: extra GStreamer plug-ins for 64-bit Unity video (AVPro, Media Foundation `.mp4`).
- `WINEDEBUG`: RavenGun sets `-all`; `--log-full` on the start plan switches on `+debugstr,err+module` so the game's `OutputDebugString` lines reach the log.

Back to [Home](Home).

# Loader architecture

This page describes how RavenGun starts a game and how the game gets its input: the four routes (direct Wine, Lindbergh, native Linux, Unity plug-in), the input bridges, drop-ins, per-game profiles, the start plan and the identity rule that makes every log say which tool did the run. RavenGun ships no games; you need your own copy of each title. The platform pieces it builds or borrows (Wine, DXVK, the OpenParrot loader and core, `lindbergh-loader`) are fetched or built on your machine.

Labels: **MEASURED** (seen or measured on the bench, with the numbers where they matter), **INFERRED** (derived from files, traces or disassembly) and "assumption" (not tested).

## 1. What the loader has to do

An arcade title is written to find a cabinet around it:

- it expects its own working directory, drive letters and data folders (**MEASURED** on several titles);
- it asks a board for input over shared memory, a serial line, a HID device, a joystick API or a TCP socket, depending on the family (**MEASURED** per title);
- it may expect a second program (a platform daemon) to run first (**MEASURED**);
- it expects cabinet hardware and system libraries that a normal PC does not have. RavenGun provides the cabinet hardware the game expects; for Linux titles it also provides the old libraries (**MEASURED**: none of seven Linux titles started with the kernel's loader alone; six stopped on the first library the machine lacked).

So a launcher has to choose how to load the game, put the working directory, environment and drive letters in place, deliver input through the channel the game reads, and be able to say afterwards which tool, route and files produced the result.

## 2. The routes at a glance

Which route applies is a property of the title, not a preference. You start every game the same way: double-click it in the RavenGun app.

| Route | For | Started by | Details |
|---|---|---|---|
| Direct Wine (`[Launch] Mode = direct`) | Windows titles | `rg-direct`: Wine, our own OpenParrot loader and core, drop-ins, a local view of the game folder, optional gamescope | section 3 |
| Lindbergh | SEGA Lindbergh titles (32-bit Linux ELF) | the engine: gamescope, bubblewrap, the game with `lindbergh.so` preloaded | section 4 |
| Native Linux | Raw Thrills-style Linux titles | the engine: gamescope, bubblewrap, `rg-elfloader` | section 5 |
| Unity plug-in | Unity titles such as [Rabbids-Hollywood](Rabbids-Hollywood) and [Tomb-Raider-Arcade](Tomb-Raider-Arcade) | Proton with a plug-in inside the game; input over TCP | section 6 |

The input side is separate from the route: the engine publishes one input state and a bridge translates it (section 7).

## 3. The direct Wine route (`rg-direct`)

`rg-direct` is the main process of the game's systemd unit. It reads the plan the engine computed (section 10) and runs it. A Python reference (`scripts/launch-direct.py`) computes the same plan; a golden test compares the two.

**Wine.** Plain Wine, not the `proton` script. The default is the Wine from `proton-11.0-2` under `~/.local/share/ravengun/wine/`. A profile may name another with `[Wine] Binary`. A Proton runner is refused (**MEASURED**). One shared prefix is used unless `[Wine] Prefix` names another; every Wine command sets `WINEPREFIX` explicitly.

**The loader and core.** The call is

```sh
wine <loader> [<core, without .dll>] "Z:\...\<game>.exe" [arguments]
```

- The core is the loader's first argument and the loader appends `.dll` itself, so two cores can be compared by changing one argument (**MEASURED** on [Luigis-Mansion](Luigis-Mansion)).
- RavenGun builds the OpenParrot loader (`OpenParrotLoader.exe`, `OpenParrotLoader64.exe`) and the OpenParrot core (`OpenParrot.dll`, `OpenParrot64.dll`) from the public source with `scripts/build-openparrot.sh`, in a pinned container. `[Loader] Build = ravengun` selects them. The one Wine-specific change is in the loader: Wine sets MXCSR to 0 when `SetThreadContext` is called with `CONTEXT_FLOATING_POINT` but without extended registers, after which Mesa stops in the Direct3D 9 initialisation with `c00002b5` (**MEASURED**, Type X2 titles). The built loader leaves that flag out.
- The loader takes all arguments as one parameter. The working directory is the game's own folder for ELF-in-Wine families and the loader's runtime folder for the rest; on Luigi's Mansion the loader must start in its runtime folder while the game's working directory is `exe/x64` (**MEASURED**).
- Environment set for the run: `WINEPREFIX`, `WINEDEBUG=-all`, `TP_LAUNCH_SESSION_ID` (a UUID per run), and a stereo audio device (`PULSE_PROP`, see [Wine-Notes](Wine-Notes)).
- **The remote-thread trap (MEASURED).** The loader has two injection methods and the remote-thread method fails on these titles with `Failed to find kernel32.dll in target process`. The presence of the variable `TP_REMOTETHREAD` selects it, even with the value `0`, so the profile key `[Loader] RemoteThread = off` means "do not set the variable". The default entry-point trampoline then works: `Resolved target kernel32.dll procedure: ...` followed by `Have fun :)`.

**Views of the game folder.** Games usually live on a share, and RavenGun never writes there. The game runs from a local "view" (`~/.local/share/ravengun/runtime/views/<Game>/`): symbolic links to everything in your game folder, plus real local folders for the executable's folder and every folder above it up to the view root. Settings files and drop-ins go into those local folders. A view is made automatically on the first start (`[Launch] View = auto`; `off` runs straight from the share, without drop-ins; a number N puts the root N folders above the executable). Every step checks that it writes to a local folder and refuses otherwise. Existing files in the game folder stay links; a file the game newly creates in a locally made folder stays in the view.

Related view keys: `ViewEmptyDirs` (folders that become empty local folders, for example a movies folder), `ViewLinks`, `ViewCopies`, and `StackReserve` (a local copy of the executable with a bigger main-thread stack; see [Wine-Notes](Wine-Notes)).

**Drive letters.** `[Launch] Drives = W=.; Y=~/folder` creates drive letters for the run only (symbolic links under the prefix's `dosdevices`) and removes them afterwards. A letter that exists and points elsewhere is refused.

**Window and fixes.** `[Display] Gamescope = true` runs the game fullscreen in gamescope; `[Launch] Dxvk`, `Gst32`, `NativeDlls` and `Registry`, and the stereo audio device, are explained on [Wine-Notes](Wine-Notes).

**Second executable.** A profile with `HasTwoExecutables` starts a helper first and waits (House of the Dead: Scarlet Dawn: platform daemon, 5 seconds, then the game). A profile that merely lists two names in `ExecutableName` is one start: the shell is started and starts the game itself (Transformers: Shadows Rising). **MEASURED.**

**Shared memory and the JVS pipe.** Before the game starts, the loader creates the board image `/dev/shm/ravengun_JvsState` (64 bytes; existing content is kept) and starts a small Windows helper in the prefix, `rg-jvsbridge.exe` (our own, clean-room). It creates the named pipe `\\.\pipe\TeknoParrot_JVS` and the file mapping `TeknoParrot_JvsState` that the OpenParrot core uses, mirrors the mapping with the shared file every millisecond in both directions (the file wins on a conflict) and carries the pipe over TCP to the launcher. The launcher sets the connect flag (byte 0) on JVS reset (`0xF0`) and address (`0xF1`) and logs any other packet. **MEASURED:** with this route the game connects and aiming, reloading and the trigger work, even across an engine restart.

**Ending.** The launcher waits for the loader (or gamescope), then for as long as the game is in its cgroup, stops the helper and lets systemd clean up the rest.

## 4. The Lindbergh route

A SEGA Lindbergh game is an ordinary 32-bit Linux ELF and runs with the system loader. What is missing is the cabinet: the baseboard, EEPROM, security board, JVS line and system libraries from 2006. `lindbergh-loader` (a preload library, `lindbergh.so`) hooks the cabinet device accesses and patches per game. RavenGun does not ship it: `scripts/build-lindbergh-loader.sh` builds a pinned source in a container into `~/.local/share/ravengun/lindbergh-loader/current`, together with the i386 libraries SteamOS lacks.

- The engine runs `gamescope` then `bubblewrap` (read-only system, your game folder as a read-only lower layer with a local overlay for everything the game writes) then the game with `lindbergh.so` in `LD_PRELOAD`. No shell and no Wine.
- The loader recognises the game by a CRC-32 of the first 0x4000 bytes of its code; all patches hang on that ID. RavenGun computes the same ID and refuses another ELF (**MEASURED**: a wrong ELF for a title is rejected with "wrong ELF").
- Input is JVS: the engine acts as the I/O board (section 7).
- Titles on this route include [House-of-the-Dead-4-Special](House-of-the-Dead-4-Special), [House-of-the-Dead-4](House-of-the-Dead-4), [House-of-the-Dead-EX](House-of-the-Dead-EX), [Rambo](Rambo), [Too-Spicy](Too-Spicy), [Ghost-Squad-Evolution](Ghost-Squad-Evolution), [Primeval-Hunt](Primeval-Hunt), [Lets-Go-Jungle](Lets-Go-Jungle) and [Lets-Go-Jungle-Special](Lets-Go-Jungle-Special). Their per-title status is on [Compatibility](Compatibility).
- Mesa needs the Cg shaders of some titles recompiled; the layer does that with `libCg.so` 2.0 (**INFERRED** from the loader's configuration; works on the titles marked working).

## 5. The native Linux route (`rg-elfloader`)

For Raw Thrills-style titles (Linux ELF, 32- or 64-bit) the engine runs `gamescope` then `bubblewrap` then, for the 32-bit family, `rg-elfloader`, then the game. The profiles are in `packaging/native-games.json`: mounts (game folder read-only with a local write layer), files shown over paths inside the sandbox, libraries, the preload library, and the input table.

**The sandbox.** Bubblewrap with explicit binds: `/usr`, `/etc`, `/sys` read-only, `/dev`, `/dev/dri` and `/dev/input` passed through, own network and PID namespace, `/tmp` as tmpfs. The game folder is a read-only lower layer; **MEASURED** that these games write in their own folder (`pmuser/`, save files), so the overlay keeps the source untouched. The game expects fixed absolute paths such as `/pm/...`; the sandbox shows it those. A game that uses the X shared-memory extension crashes in an isolated IPC namespace, so a profile can share the host IPC (**MEASURED**).

**Why a loader.** **MEASURED:** the seven Linux-ELF titles in our first set were started with the kernel's loader alone and **0 of 7 started**: six stopped on a missing old library (`libGLU.so.1`, `libstdc++.so.5`, `libfmod.so.10`, `libtheora.so.0`, `libXrandr.so.2`) and one died with SIGSEGV without output. Several of these files carry **no section headers**; the old Wine-based wrapper warns `SHT_DYNSYM not found` and goes on, and the warning is harmless (the symbols are reachable through the dynamic segment: **MEASURED** 220 symbols read from `DT_HASH` on one title).

`rg-elfloader` is our own small i386 loader. It maps the `PT_LOAD` segments at their fixed addresses, loads the guest libraries with `dlopen`, applies the relocations (`R_386_COPY`, `GLOB_DAT`, `JMP_SLOT`, ...), builds a System V start stack and jumps to the entry point. It shares the host's `libc.so.6` with the game so there are not two C libraries in the process. It reads the symbols from the dynamic section when the classic hash table is absent (**MEASURED** on Terminator Salvation: 1020 symbols, 13 libraries loaded, 2 only on a second attempt). `rg-elfloader --dry-run <game>` analyses without starting; **a dry run must take the same path as the real run** (ours once retried failed library loads only in the dry run and was green while the real run died at the same spot).

Two helper libraries often travel with it as drop-ins or sandbox files:

- a graphics bridge for 32-bit titles whose OpenGL calls would otherwise corrupt the stack (calling-convention mismatch, **MEASURED** on Jurassic Park);
- an input shim that writes the board's switch table (section 7).

Native-route titles with their current status are on [Compatibility](Compatibility); see for example [Jurassic-Park-Arcade](Jurassic-Park-Arcade), [NERF-Arcade](NERF-Arcade), [Halo-Fireteam-Raven](Halo-Fireteam-Raven), [Terminator-Salvation](Terminator-Salvation) and [Target-Terror-Gold](Target-Terror-Gold).

## 6. The Unity plug-in route

For some Unity titles no loader or injected core is used: Proton starts the game with a managed plug-in loaded through a `winhttp.dll` proxy in the game folder. **MEASURED** for Rabbids Hollywood:

```sh
<GE-Proton>/proton run Game.exe -popupwindow
```

with `WINEDLLOVERRIDES=winhttp=n,b` (required: without it Wine does not load the proxy that loads the plug-in) and a prefix of its own. The plug-in inside the game is the TCP server on `127.0.0.1:33610`; the engine is the client and sends a fixed-size input packet at 120 Hz (the `unity-tcp` dialect).

## 7. Input bridges: one state, several dialects

The engine publishes **one** input state and the bridge translates it. Per player 1..4: aim as a fraction 0..1, `valid`, `offscreen`, trigger, reload, grenade, two extra buttons, start; for the cabinet: coin per player, test, service, volume up and down. A tick thread at 250 Hz writes the state to the active dialect. A player without an armed gun or a valid aim is written as idle, never as the previous position.

| Dialect | How the game gets input | Used by |
|---|---|---|
| `tp-shm` | the 64-byte board image in shared memory (section 3); the layout per game is data in `packaging/tp-shm-profiles.json` (per bit a signal, byte offset and bit; per axis offset, size, range, inversion, idle) | most Windows titles and several native ones |
| `jvs` | the engine is a JVS I/O board on a pseudo-terminal (115200 8N1, a fixed symlink) or over the pipe; the board per game is in `packaging/jvs-boards.json` | Lindbergh titles, [Lets-Go-Island](Lets-Go-Island), [Lets-Go-Safari](Lets-Go-Safari), [SEGA-Golden-Gun](SEGA-Golden-Gun) |
| `hid-board` | a virtual joystick (`uinput`) or HID device (`uhid`) built from `packaging/hid-boards.json` | [Transformers-Shadows-Rising](Transformers-Shadows-Rising) |
| `evdev` | the engine writes to an evdev device and the game reads input devices itself | some native titles |
| `unity-tcp` | TCP client to the game's plug-in (section 6) | Unity titles |

Notes:

- **JVS framing:** sync `0xE0`, escape `0xD0`, checksum over node, length and data; reset `0xF0`, address `0xF1`, identify `0x10`, switches `0x20`, coins `0x21` (a rising edge counts one coin), analog `0x22` (16-bit, high byte first). A game that asks for the modem status as a sense line needs a small shim: a pseudo-terminal does not answer `ioctl(TIOCMGET)` (**MEASURED**: `ENOTTY`).
- **Control pipe:** some titles read part of their input from a second pipe; `[Input] ControlPipe = <layout>` makes the bridge write that report too (House of the Dead: Scarlet Dawn).
- **Coin keys:** `[Input] CoinKeys = lshift,t` also presses keys when a coin is inserted, for games that read coins from the keyboard.
- **Wine side:** `hid-board` titles ask for `GUID_Joystick`; the board is given joystick id 0 in the prefix.
- **Native side:** native titles do not read the engine's devices at all. A small shim writes the shared state into the game's own switch table (**MEASURED**; an extra virtual device would never be looked at). Read the shared state with `pread`, never by mapping it, and write it in place: a writer that truncates the file even for an instant kills a memory-mapped reader with `SIGBUS` (**MEASURED** on Halo).
- **Route selection** is per game and layered: the shipped `[Input] Route` (plus `Layout`, `Board`, `Boards`, `ComPort`, `CoinKeys`), with the user layer winning per key. `ravengunctl iobridge start <Game> [--route R]` starts a route and `ravengunctl status` shows it. A restart of the engine keeps the route and resumes it while the game still runs; it stops by itself if the game is gone for more than 8 seconds.

## 8. Input devices

RavenGun turns a physical device into a virtual lightgun per player:

- **PS Move** (the original ZCM1 with the magnetometer, plus a PS3 Eye camera that corrects drift) is the main device. It is paired over USB once, calibrated in the setup wizard, and the PS button centres the aim. The Y axis can be flipped per player.
- **Mouse** as a lightgun: the pointer moves the gun; left button shoots, right reloads.
- **Game controller** (Xbox pad, Steam Controller, any evdev gamepad) next to the gun for what a gun lacks: a steering wheel, gas and brake, extra cabinet buttons. The default layout is left stick = wheel, RT/LT = gas/brake, A/B/X/Y = trigger/reload/grenade/aux, LB/RB = extra buttons, Start = start, Back = coin. A `[Gamepad]` section in `game.ini` overrides it per key.

The user needs write access to `/dev/uinput` (the wizard installs a narrow rule). A game that opens input devices does so at start, so the virtual device must exist before the game starts (**MEASURED** on a Wine ELF-loader route).

## 9. Drop-ins

A drop-in is one of our own files that the launcher puts in the game's view. `patches/<Game>/dropin/` holds the files and `dropin/dropin.ini` has one section per file:

| Key | Meaning |
|---|---|
| `To` | destination folder inside the view (`.` = the game's main folder) |
| `DllOverride` | `native` sets `<name>=n`, `builtin,native` sets `<name>=n,b` in `WINEDLLOVERRIDES` |
| `Env` | extra environment variables, separated by `;` |
| `Preload` | the file must be loaded into the game's process |
| `Audit` | `false` keeps the file out of `LD_AUDIT` (default `true`) |

Learned the hard way:

1. **The destination is `To` plus the section name.** Putting the path in both places puts the file one level too deep. The launcher reports that form as an error.
2. **`Preload = true` uses whichever variable the route actually reads.** Windows game via the OpenParrot loader: `TP_PRELOAD_DLL`, exactly one Wine path, loaded by the loader after the core. Linux ELF under a Wine wrapper: `LD_AUDIT`. Native start: `LD_PRELOAD`. **MEASURED** on Luigi's Mansion: before this rule the process had 0 of 2 drop-ins in `/proc/<pid>/maps`.
3. **A library that must live in the game must not be audited into a wrapper.** A wrapper that loads the game into its own address space also loads anything in `LD_AUDIT`; with an inline hook there the wrapper died (exit 1, and exit -11 on another title). `Audit = false` fixes it.
4. **A drop-in that cannot be placed is an error, not a warning.** A run without its drop-in is an invalid run: exit code 5, no fallback. A destination that resolves outside the view through a symbolic link is refused.
5. **`LD_PRELOAD` is not safe for every Wine child.** One wrapper we start is a Cygwin program and exits when it sees `LD_PRELOAD` (**MEASURED**).

## 10. Per-game profiles

Everything that differs per title lives in the game's own folder, not in the launcher: `patches/<Game>/game.ini` (shipped), `~/.local/share/ravengun/patches/<Game>/game.ini` (your layer; it wins per key and deleting it restores the shipped state), and `patches/<Game>/dropin/`. Shared tables (`tp-shm-profiles.json`, `hid-boards.json`, `jvs-boards.json`, `control-pipe-profiles.json`) are referenced by name. The same idea as Dolphin's per-game settings.

Sections: `[Game]`, `[Identify]` (how your game folder is recognised), `[Launch]` (`Mode`, `Exe`, `Drives`, `View*`, `Gst32`, `Dxvk`, `NativeDlls`, `Registry`, `StackReserve`), `[Loader]`, `[Wine]`, `[Display]`, `[Input]`, `[Audio]`, `[Gamepad]`, `[Env]` (free variables, applied last and winning over the named keys), `[Status]`. Settings the profile offers (region, language, windowed) are ordinary keys you may set.

## 11. The start plan (`--plan`)

```sh
rg-direct --plan <Profile>                       # what would happen; nothing starts
python3 scripts/launch-direct.py <Profile> --check
python3 scripts/launch-direct.py <Profile> --run
```

`--plan` has no side effects and uses the same code as the real start, so an impossible start is refused before anything runs. It prints the identity lines (section 12), the profile, the loader and core with SHA-256, the command line, one line per drop-in with its destination, the starts in order with waits, the environment and the files read. Exit codes: **0** finished, **1** error during start, **2** wrong use, **4** profile not supported for a direct start, **5** an enabled patch or setting was refused (no fallback, because starting without it would measure something else), **7** one of two starts was already gone before the next began.

## 12. The identity rule

**MEASURED** the expensive way: three measurements in one week were lost to an old copy nobody knew was running (an old loader, an old drop-in library, an old installed launcher). Every plan and run log therefore starts with the path of the tool that runs, whether it is the repository version (with commit) or the installed version, its SHA-256, the SHA-256 of its helper modules, and whether the installed copy is the same. Update an installation as a whole, and make a build script fail if the installed file differs from the built one.

## 13. What is Linux-specific, and what differs on Windows

Not tested on Windows by us; this table is an assumption.

| Here (Linux) | On Windows |
|---|---|
| Wine prefix with `dosdevices` for extra drive letters | real drive letters, `subst` or a mapped drive |
| `LD_PRELOAD`, `LD_AUDIT` | DLL injection, or the DLL next to the executable |
| `WINEDLLOVERRIDES` | the DLL next to the executable, or a manifest |
| `uinput`/`uhid` virtual devices | a virtual joystick/HID driver |
| shared-memory file plus a helper in the prefix | a named file mapping directly |
| `gamescope --backend headless` | no equivalent |
| the kernel's `ld.so` and a sandbox for Linux ELFs | not available: a Linux title needs a Linux environment |

What travels: working directories, data roots, the board layout the game asks for, the file names it probes and the point where it stops. Continue with [Official-Start-Scripts](Official-Start-Scripts), [Running-on-Linux](Running-on-Linux), [Wine-Notes](Wine-Notes) and [Home](Home).

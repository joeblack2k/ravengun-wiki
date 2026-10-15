# Running on Linux

RavenGun is developed and measured on Linux: a Steam Deck running SteamOS (Arch-based, KDE Plasma on Wayland in Desktop Mode) connected to a 1920x1080 TV over HDMI, with Game Mode for the full-screen menu. The games were made for Windows-based and Linux-based cabinets. This page collects what is specific to running them on a Linux PC and the pitfalls that cost time. RavenGun ships no games; you need your own copy of each title. Labels: **MEASURED** (seen on the bench), **INFERRED** (derived from files or traces) and "assumption" (not tested), as on [Home](Home).

## What you need

- SteamOS 3.x (or Arch Linux with KDE Plasma) with Qt 6.11 or newer.
- A PlayStation Move ZCM1 and a PS3 Eye camera for the gun, or a mouse or game controller (see [Loader-Architecture](Loader-Architecture)).
- Your own game folders. Steam, if you want Proton parts (see below).
- The installer needs no root and does not touch the read-only system partition; the setup wizard asks for one password to install device rules.

## The kinds of game

| The cabinet runs | RavenGun uses | What you need |
|---|---|---|
| Windows | Wine, with our own OpenParrot loader and core | Wine (taken from a Proton release), a prefix, a local view of the game folder; optionally DXVK, 32-bit GStreamer, Microsoft DirectX DLLs from Steam |
| Linux, SEGA Lindbergh | the game ELF with `lindbergh.so` preloaded, in a sandbox | the i386 libraries SteamOS lacks (built by a script) |
| Linux, Raw Thrills style | the game ELF through our own `rg-elfloader`, in a sandbox | the old libraries, a sandbox that shows the game its fixed paths, an input shim |
| Unity (Windows) | Proton with a plug-in inside the game | a prefix of its own, the plug-in loader override |

"Linux game" does not mean "runs on a current Linux". These binaries expect fixed absolute paths (`/pm/...`), library versions that current distributions no longer ship, and a kernel and C library from their own era. The routes are on [Loader-Architecture](Loader-Architecture); per-title status is on [Compatibility](Compatibility).

## Wine

**Plain Wine, not a wrapper script.** The direct route starts `wine` itself. Launch wrappers made for game stores add their own environment and process tree, and a profile that names a Proton runner is refused (**MEASURED**). Fixes that need pieces of Proton borrow them from Steam's install instead (see [Wine-Notes](Wine-Notes)).

**One prefix, and always name it.** Every Wine command sets `WINEPREFIX` explicitly. `wineserver -k` without a prefix acts on the default prefix, not the one your game runs in. One of our own tools made exactly that mistake (**MEASURED**).

**Environment variables pass through unchanged** (**MEASURED**): variables in the Unix environment arrive in the Windows process and its children with the same name and value.

**Arguments survive if you pass a list.** Start Wine with an argument list, with no shell in between. A parameter containing quotes, spaces and a backslash before a quote arrived byte for byte (**MEASURED**).

**Drive letters are symbolic links.** `X:` in a prefix is `<prefix>/dosdevices/x:` pointing at a folder. **MEASURED** on a test prefix: a program starts from `X:\exe\x64\game.exe` right after the link is created, a script there sees its own path as `X:\exe\x64\...`, it works even if the Wine server was already running, and removing the link removes the letter at once. The launcher creates a link for one run only (`[Launch] Drives`), removes it afterwards also if the run fails, and refuses a letter that exists and points elsewhere. A letter left behind in a shared prefix changes every later run (**MEASURED**).

**The working directory.** A program started directly by `wine` gets the Unix working directory, seen as `Z:\...`. A game started through the OpenParrot loader gets the folder of the path the loader was given, so `Z:\...\game.exe` and `X:\exe\x64\game.exe` give different working-directory strings for the same folder (**MEASURED**).

**`LD_PRELOAD` is not safe for every Wine child.** Wine passes its environment to everything it starts, and one wrapper we use is a Cygwin program that exits when it sees `LD_PRELOAD` (**MEASURED**). That is why a drop-in has separate switches for "load into the game" and "may go into the loader's preload list".

**Serial ports are links too.** Wine recreates `dosdevices/com1` to `com32` at every cold start of its server, so a link you make yourself is overwritten unless the server already runs. The JVS route therefore starts a persistent Wine server for the prefix first, then sets the link (**MEASURED**: an earlier link had vanished).

**Movies, Direct3D, audio, fullscreen.** These are the common causes of "starts but black / frozen / buzzing"; the symptom-to-setting list is on [Wine-Notes](Wine-Notes): `Gst32`, `Dxvk`, `NativeDlls`, gamescope, rg-compat and the stereo audio device. In short for audio: on a 7.1 HDMI output Wine's DirectSound mixes badly (a buzz on every mono effect), so RavenGun gives Wine games a stereo device by default.

## Native Linux games

**A sandbox instead of a chroot.** The native start builds a `bubblewrap` sandbox: `/usr` and `/etc` from the host read-only, the game's folder bound at the path the game expects (read-only lower layer), and a local overlay for everything the game writes. Nothing is copied and nothing is written into your game folder; the network namespace is unshared (**MEASURED**).

**Shared-memory graphics need the host IPC namespace.** A game that uses the X shared-memory extension crashes in an isolated IPC namespace (**MEASURED** on one title). The sandbox isolates IPC by default and a profile can share it.

**The game does not read your input devices.** Native titles take their input from a switch table that a small shim fills from the engine's shared state. An extra virtual device is work the game never looks at (**MEASURED** on [Halo-Fireteam-Raven](Halo-Fireteam-Raven)).

**Old 32-bit binaries need their own loader.** Some carry only a GNU hash table and rely on libraries being in the global scope in a particular order; `rg-elfloader` handles both (**MEASURED** on [Terminator-Salvation](Terminator-Salvation): 1020 symbols counted from the dynamic section, 13 libraries loaded, 2 only on a second attempt). A dry-run mode must take the same path as the real run, or it reports green while the real run dies at the same spot.

**Old libraries.** SteamOS has no 32-bit versions of several libraries these games link (SDL3, `libstdc++.so.5`, ncurses 5, `libXmu`, `libCg.so`). Scripts under `scripts/` build or stage them into `~/.local/share/ravengun/runtime/lib32/` and the Lindbergh layer's folder; nothing goes into the system.

## Shared memory between the engine and a game

The engine publishes the board image as a file in `/dev/shm`. Two lessons:

- **Read it with `pread`, do not map it.** A writer that truncates the file even for an instant (opening it with truncation does that) invalidates a memory mapping, and the reader then dies with `SIGBUS` on its next access. That reader was a library inside the game, so the game died. **MEASURED** on Halo: a memory-mapped reader dies, a `pread` reader stays alive.
- **Write in place.** Never recreate the file to update it; write at the offset.

## Displays

Runs can be headless or on the real screen, and the two are not comparable for timing or screenshots.

| | Headless | On the TV |
|---|---|---|
| How | `gamescope --backend headless`, or no display in the environment | `gamescope -f`, or a window on the desktop session |
| Frame pacing | not tied to a display | tied to the display (59.96 Hz on the bench TV) |
| Sound | none | yes |
| Input from the desk | does not reach the game | reaches the game; gamescope grabs the pointer |

A run started from a service or an SSH session has no display. It needs the environment of the desktop session: `DISPLAY`, `WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, the session bus address and `XAUTHORITY`. Without `XAUTHORITY` the X server refuses with "Authorization required, but no authorization protocol specified" (**MEASURED**). `XAUTHORITY` changes with every desktop session, so read it from a running session process each time.

**OLED TVs.** A static menu or a game's fixed HUD can burn in. RavenGun's full-screen menu dims, moves and finally goes to a small moving text after a while without input.

## Virtual input devices and permissions

The engine creates its devices through `uinput` (an absolute-pointer lightgun per player, a keyboard) and, for some titles, `uhid` (a virtual HID board).

- The user needs write access to `/dev/uinput`; the wizard installs a narrow `udev` rule. `/dev/uhid` is `root`-only by default and needs a rule of its own.
- `/dev/ttyS0` is `crw-rw---- root:uucp`, which gives an ordinary user a refusal rather than a missing file, a difference a game can detect (**MEASURED**). RavenGun's JVS route uses a pseudo-terminal instead.
- **A game that opens input devices does so at start.** The virtual device must exist before the game starts (**MEASURED** on a Wine ELF-loader route: the loader held the event device open only if it existed at launch).
- The Steam Controller is reported by the kernel driver as a pad that connects and disconnects about 15 times a second, even without Steam running (**MEASURED**); a plugged-in Steam Controller can therefore show up as two pads (the Steam virtual one and the driver's own).

## Game files on network storage

If your games live on a share, RavenGun starts them from local views (folders of symbolic links; see [Loader-Architecture](Loader-Architecture)) and never writes to the share.

- **Resolve links before you write.** A path inside the view can resolve to the share through a link in a parent folder. The drop-in engine refuses a destination that lands outside the view, at planning time.
- **Expect slow first reads.** A file-integrity pass that a game runs at start took about two minutes from a local disk and an estimated 25 minutes from the share (**MEASURED**: 4 files per second, 5,941 files).
- **Cold and warm cache differ.** The same start gave 1 s warm and 11 s cold at one moment in one title, 4.8 s and 6.0 s in another (**MEASURED**). A time without "cold" or "warm" says nothing.

## Measuring a running game

- **Only a parent process may read another process's memory** under the kernel's default restriction on many distributions. A helper started beside the game is refused; the process that started the game is not. Open the file descriptor in the parent and hand it over (**MEASURED**). `perf record -e cpu-clock:u -p <pid>` works on your own processes when `perf_event_paranoid` is 2.
- **Instrumentation changes what you measure.** A full file trace made one game take four to five times longer (25 to 30 s against 5 to 7 s; **MEASURED** on [Luigis-Mansion](Luigis-Mansion)).
- **Wine keeps servers alive.** After a test, stop the server of the prefix you used, by name, and check that it is gone before the next measurement.
- RavenGun's `RG_COMPAT_SAMPLE` thread finds a hung Wine game without a debugger (see [Wine-Notes](Wine-Notes)).

## Stale copies

It is easy to have the same program twice: a source checkout and an install folder. A fix in one is not a fix in the other.

- A build script that produces a binary must also install it and fail if the installed file differs from the built one.
- Every run log starts with the path and SHA-256 of the tool that ran; see the identity rule on [Loader-Architecture](Loader-Architecture).
- Update an installation as a whole. Copying one script into it breaks it when that script has gained a helper file.

## One game at a time

Two games at once share the engine, the shared-memory file and often the Wine prefix. A second start during someone else's run invalidates both runs (**MEASURED**: one run was discarded for exactly that reason). Before starting, check for a running game, a gamescope process and a Wine server, by process name rather than by a pattern on command lines (a pattern matches the shell that runs the check).

See also [Loader-Architecture](Loader-Architecture), [Official-Start-Scripts](Official-Start-Scripts) and [Wine-Notes](Wine-Notes).

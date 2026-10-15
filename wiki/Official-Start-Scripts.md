# Official start scripts

Almost every title in this set came with a start script written by its manufacturer. This page
describes what those scripts do, why RavenGun **never executes them**, and which parts RavenGun takes over instead.
It is the page to read before you run anything of the sort yourself.

RavenGun ships no games; the scripts quoted here come from your own copy of each title. Labels: **MEASURED** (seen or measured on the bench), **INFERRED** (derived from files or traces) and "assumption" (not tested). The routes that replace the scripts are on [Loader-Architecture](Loader-Architecture).

## 1. The rule

**RavenGun reads a cabinet's start script and never runs it.** It takes over only the parts that a title
actually needs — a working directory, an argument, an environment variable, a drive letter, the order
in which two programs are started — and rebuilds those in its own launcher, where you can see what they do.

This is not caution for its own sake. The scripts in this set do things that are correct on a
dedicated cabinet and destructive anywhere else:

- `rmdir /S /Q Y:\` — **wipe an entire drive** if the expected data folder on `Y:` is missing. On a
  cabinet `Y:` is a dedicated data volume; on your machine `Y:` may be your own.
- `reboot -f` — reboot the machine, without asking.
- `rm -rf ${USERDIR}` — delete the user's folder.
- `passwd -l` — lock an account.
- `swapoff -a` — turn off all swap.

All five appear literally in scripts of titles in this set (**MEASURED** from the files; sections 3.1 to 3.3). A
script like this is also written for a machine that is expected to restart, so it may leave its own
environment half-changed and rely on the reboot to clean up.

## 2. What a cabinet start script does

Reading several of them makes the pattern clear. A start script is a wrapper that puts the cabinet
around the game. Five roles show up again and again:

1. **A gate before the game may start.** A hardware-information program is run first and the game is
   started only if it exits with code 0. That program checks the machine the cabinet expects.
2. **Environment variables** the game or its platform layer reads: a game identifier, a flag that says
   the game is running from an image, the image root, a launch mode.
3. **Drive letters with a meaning.** `X:` is the image the software was installed from, `Y:` the app
   data area, `D:` the platform's own storage. The script creates the data folder, and wipes the whole
   letter if it is not there.
4. **A pre-start step that touches hardware**: writing board data over a serial port, or asking a
   hardware helper which screen mode the cabinet is in.
5. **A different working directory and a program chain.** The game is started from a specific folder,
   and sometimes a second program (a platform daemon) must be running before it, with a fixed wait
   between the two.

## 3. The scripts, literally

### 3.1 Luigi's Mansion Arcade — `game.bat`

259 bytes, UTF-8 with a byte-order mark (**MEASURED**):

```bat
@echo
setlocal
rem <game ID>
set GAMEID=SDCF
rem <exclusive use of the app data area>
if not exist Y:\%GAMEID% (
    rmdir /S /Q Y:\
    mkdir Y:\%GAMEID%
)
start /wait sendFlash COM1 LMAIO.bin
start /wait x:\exe\x64\VACUUM.exe
```

Four things happen: an environment variable `GAMEID=SDCF`; an app data folder `Y:\SDCF` that is
created, **with the whole of `Y:\` wiped first if the folder is not there**; a tool
(`sendFlash COM1 LMAIO.bin`) that writes board data out of a serial port and is waited for; and the
game, started from a drive letter and from a subfolder, without arguments. Each of the four steps was tested one at a time on the bench; the outcome is on the [Luigis-Mansion](Luigis-Mansion) page.

### 3.2 Halo: Fireteam Raven — `utils/run_game.sh` and `utils/go.sh`

This is a Linux title, so its official start is a shell script. The core lines (**MEASURED**):

```sh
cd /pm/g7/halo
LD_PRELOAD=/pm/g7/halo/halo.so ${GAMEDIR}/game2 -f${SCREEN_RES} -n
```

with, before it, `utils/rtinit -ct`, which probes the cabinet and whose exit code selects
`SCREEN_RES`; `export DISPLAY=:0`; and a call to `pulseaudio_set_default.sh`. After the game, a `case`
on the **exit code** of the game decides what the cabinet does next: **222** restart the game, **223**
reboot, **224** apply a modification, **225** factory reset, **226** power-cycle.

The destructive parts are in the same scripts: `reboot -f` and `sync`, `rm -rf ${USERDIR}` (throw
away the user's folder), and in `go.sh` also `passwd -l`, `swapoff -a` and network setup.
**MEASURED** from the files.

Two details matter for anyone rebuilding this route: `game2` does not exist in the folder — the
official start names it, and what is actually there is `game`, the same modified image — and
`rtinit -ct` is a hardware probe whose code selects the resolution: an unknown code leaves an **empty**
resolution argument behind, so the game is started as `game -f -n` (**MEASURED**).

### 3.3 House of the Dead: Scarlet Dawn — a chain of six scripts

`game.bat` → `App/Startup/AppStartup.bat` → `05_SetVideoPort.bat`, `10_SetResolution.bat`,
`20_SetAudioVolume.bat`, `99_StartApp.bat` → `App/Hodzero/StartApp.bat` (**MEASURED**). What the
steps do:

| Step | What it does |
|---|---|
| `game.bat` | Sets `LAUNCH_ON_IMAGE=1` and `IMAGE_ROOT_DIR=X:\`, then calls `AppStartup.bat`. |
| `AppStartup.bat` | Calls the four scripts below, in order. |
| `05_SetVideoPort.bat` | Writes five register values (`port_1..port_5` = `DVI0, DP0, DP1, DP2, HDMI0`). |
| `10_SetResolution.bat` | `..\Tools\SetResolution.exe 1920 1080 0` — sets the desktop resolution. |
| `20_SetAudioVolume.bat` | `..\Tools\SetAudioVolume.exe 85 75`. |
| `99_StartApp.bat` | `GAME_ID=SDET`, `APP_DIR=Y:\SDET`, `APP_LOG_DIR=Y:\SDET\current_log`; creates `Y:\SDET`, **wipes `Y:\` if that folder is missing**, and moves to `App/Hodzero`. |
| `App/Hodzero/StartApp.bat` | Picks the newest of four game executables, sets `DAEMON_WAIT_SECONDS=5`, starts the platform daemon, waits, starts the game, waits, and cleans up. |

The relevant lines of that last script, literally (**MEASURED**; the files are Shift-JIS, the keys are
plain ASCII):

```bat
set DAEMON_WAIT_SECONDS=5
start /min "" "%DAEMON_EXE_PATH%" -c %DAEMON_CONFIG_PATH% -l "%DAEMON_LOG_PATH%"
timeout %DAEMON_WAIT_SECONDS%
start /wait "" "%APP_EXE_PATH%" %APP_EXE_ARGS%
timeout /t 1
taskkill /im "%DAEMON_EXE_FILE_NAME%"
```

with `%DAEMON_CONFIG_PATH% = WindowsNoEditor\AMDaemon\config.json` and
`%APP_EXE_ARGS% = -launch="cabinet" -ABSLOG=… -UserDir=… -NotInstalled -UNATTENDED`.

**The `-UNATTENDED` discovery.** One of those arguments is `-UNATTENDED`, and the script comments it
in Japanese as "do not show the error window". That is not cosmetic. In one measured session the game
failed fatally 74 seconds after the start; the log shows the error **without a message**
(`Fatal error!` followed by an empty line), then the engine tries to start its crash reporter (that
file is not shipped), and then there are **60 seconds with no line at all** between the last normal
line and the shutdown. Without `-UNATTENDED` the engine sits on a modal window before it exits.
**MEASURED** for the 60-second gap and for the comment; **INFERRED** for the mechanism.

RavenGun takes over exactly three things from this chain: the **order** (daemon, 5 seconds, game),
`-UNATTENDED`, and nothing else. The arguments are not a condition for playing, by the way: a start without any of these arguments was also measured playing the game (**MEASURED**).

### 3.4 Let's Go Safari and Golden Gun — a gate, not a wrapper

```bat
mxGetHwInfo.exe -s mxGetHwInfo.ini
if %ERRORLEVEL% == 0 start /wait GameSampR_RingWide.exe
```

and

```bat
mxGetHwInfo.exe -s mxRingwide.ini
if %ERRORLEVEL% == 0 gs2.exe.bak
```

Both are 69 to 93 bytes (**MEASURED**). A hardware-information helper decides **whether the game may
start at all**; with any other exit code the game never runs. RavenGun skips that gate; the cabinet's I/O board is emulated instead.

### 3.5 Medaru No Gunman — the gate commented out

```bat
@echo off
rem mxGetHwInfo.exe -s mxGetHwInfo.ini
cd exe
start /wait game.exe
```

Here the hardware check is commented out and the game is started from a subfolder `exe`.

### 3.6 Terminator Salvation — no start script at all

There is **no** official start script in this title's folder. What is there instead is
`GeneralPurposeStateMachine.txt` (5,782 bytes, a state-machine description) and the game's data and
user folders alongside it (**MEASURED** from the file list). The route is therefore assembled from the
file layout itself; see the [Terminator-Salvation](Terminator-Salvation) page.

### 3.7 Transformers: Shadows Rising — no script, a program chain

In the whole game folder (**3,498 files**) there is not a single `.bat`, `.cmd` or `.sh`
(**MEASURED**). The official start path is a chain of programs, and it is fully reconstructible from
the configuration files they read:

```
Launcher/SystemLauncher.exe   (reads Launcher/Launcher.ini: ShellDirectory=c:\sega\shell)
      -> shell/Shell.exe      (Game Shell 180605)
           -> Transformers2/Transformers2.exe
```

The same manufacturer's *Transformers: Human Alliance* does ship a `game.bat` that does a hardware
check before starting the game, so such scripts exist in this family — just not for this title.

### 3.8 Rabbids Hollywood Arcade — no script, two cabinet programs

This folder has no `.bat` or `.cmd` either (**MEASURED**). In their place are two Windows programs:
a launcher in the game folder, and an operator tool with its own configuration file and a read-me.
What those two do is **INFERRED** (they were not run): their names and the read-me make
it clear they are cabinet tooling, not the game loop. Nothing needed came out of this title's
start tooling: the game starts directly, and the two problems you would want a start script for — a
folder name with a trailing space, and getting a plug-in into the game — are solved by the local view and the plug-in loader instead (see the [Rabbids-Hollywood](Rabbids-Hollywood) page).

### 3.9 SEGA Lindbergh titles and the loader's own starter

Lindbergh games are plain 32-bit Linux executables; the cabinet around them (baseboard, security board, I/O line) is what a start would normally provide. The preload loader that RavenGun uses (`lindbergh-loader`) comes with its own `lindbergh` starter program. RavenGun does not use it: the engine itself builds the start (gamescope, a sandbox, the game with the loader library preloaded) and plays the I/O board, so no shell chain is involved (**INFERRED** from the code; the route is described on [Loader-Architecture](Loader-Architecture)).

## 4. What RavenGun takes over instead

| Piece of the cabinet's start | What RavenGun does |
|---|---|
| The hardware gate (`mxGetHwInfo.exe`, `rtinit -ct`) | Not run. Where the gate's answer carries information the game needs (a screen mode), the result is set directly: the resolution is a setting of the launcher. |
| Environment variables (`GAMEID`, `LAUNCH_ON_IMAGE`, `IMAGE_ROOT_DIR`, `LAUNCH_MODE`) | Not set. Tested one step at a time on one title, `GAMEID` made no measurable difference (**MEASURED**). |
| Drive letters (`X:`, `Y:`, `D:`) | Where a title needs one, the launcher creates the letter for the duration of the run only and removes it afterwards (`[Launch] Drives`). |
| The pre-start hardware step (`sendFlash COM1 …`) | Not run. Its effect was measured separately for the one title that uses it: it is inert without the board attached (**MEASURED**). |
| The working directory | Taken over exactly: the launcher sets the game's working directory, and the loader runs in its own. |
| Arguments and the start order | Taken over, and only the useful ones: `-UNATTENDED` for the title where its absence costs 60 seconds on a modal window, and the daemon-first order with its 5-second wait. |
| Destructive clean-up (drive wipe, reboot, user folder, account lock) | Never taken over. |

**How the launcher reads a script. MEASURED** from the tool and its output: the start plan (`--plan`) opens the game's own
start script (`game.bat`, `run_game.sh`, or the name given in the profile), extracts the environment
variables, arguments, programs and working directory it sets, and compares them with the plan it
built itself. Anything the cabinet does that RavenGun deliberately does not do is printed as a *cabinet
thing (therefore not executed)* — for example `rmdir /S /Q Y:\ (conditional)`. Such a command is
reported, never run. The plan's output ends with three lines about the game: its own start script, the
arguments that will be passed, and the environment variables that will be set.

## 5. A checklist for your own start

If you write your own launcher for these titles, this is the order that worked:

1. **Read the script, do not run it.** On a machine that is not the cabinet, a start script's clean-up
   steps are the dangerous part and its wrapper steps are the interesting part.
2. **Note the five roles of section 2** and give each one a place in your own launcher, so nothing
   runs by accident.
3. **Test the wrapper steps one at a time**, with everything else unchanged, and write down the
   expectation before the run. A table like the one on the [Luigis-Mansion](Luigis-Mansion) page removes a whole class
   of suspects.
4. **Take over only what you measured a need for.** Two of the first six titles needed nothing from their
   cabinet tooling.
5. **Keep the argument that changes the failure mode.** `-UNATTENDED` is worth more than any other
   line in that chain: without it a fatal error costs a minute of waiting on a window that cannot be
   seen.

## 6. On Windows

The scripts are Windows batch files, and on Windows you can read them in the same way; what differs is
what they assume about the machine. Drive letters there are real letters, so a script that wipes `Y:\`
can reach a real volume, and a user folder named in a script is a real user profile path. If you run a
title on Windows, read the script for the same five roles and then start the executable yourself with
the parts you decided you need — the drive letters can be arranged with `subst` or a partition, and the
environment variables can be set in your own launcher.

---

Continue with [Running-on-Linux](Running-on-Linux), [Wine-Notes](Wine-Notes) and [Home](Home).

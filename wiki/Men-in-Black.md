# Men in Black

**Status:** Starts (2026-10-17). `MIB.exe` runs directly on RavenGun's own core with DXVK in gamescope, without the cabinet's shell: logo, attract movies, "PRESS START BUTTON TO JOIN" and free play, on screen for 2 minutes. Input has not been measured (on the cabinet it goes through the shell).

## 1. Platform and cabinet

SEGA Amusements ticket-redemption light-gun cabinet (Windows PC). Build `240913RED`, shell "Game Shell" `230307RED` (**MEASURED** from the install files). The game `MIB.exe` is 64-bit, Unity 2020.3.14; the shell `Shell.exe` is 32-bit. The dump is about 6.7 GB and corresponds to the cabinet's `C:\Sega\` folder.

## 2. What the game needs

- RavenGun ships no games: you need your own copy of the game.
- Wine with DXVK (Unity Direct3D 11) in gamescope.
- 32-bit and 64-bit GStreamer libav plugins for the attract movies (H.264/AAC MP4); without them the game dropped out at the first movie.
- BepInEx 5.4.21.0 (Mono, 64-bit), fetched by a RavenGun script with a checksum check, and RavenGun's small plugin `RavenGun.MenInBlack` as a drop-in.
- It is the same shell family as [Transformers: Shadows Rising](Transformers-Shadows-Rising), one generation newer, but the shell is not used.

## 3. The official start script, or why there is none

The cabinet runs `SystemLauncher.exe`, which starts `Shell.exe`, which starts `MIB.exe`. RavenGun does not start the shell any more: it starts `MIB.exe` itself, like TeknoParrot's own profile for this game does.

## 4. The route we use

Windows route, direct, on RavenGun's own 64-bit core (**MEASURED** from `game.ini`):

- `[Game] Type = TeknoParrot`, `EmulationProfile = WartranTroopers`, `Executable = MIB.exe`, 64-bit
- `[Launch] Mode = direct`, `Dxvk = true`, `BepInEx = 5.4.21.0`
- `[Loader] Core = ravengun` (RavenGun's own core; with TeknoParrot's closed 64-bit core BepInEx did not load and the game vanished after the logo)
- `[Display] Gamescope = true`
- `[Input] Route = tp-shm`, `Layout = WartranTroopers` (a placeholder)

**Why a BepInEx plugin:** without the cabinet shell the game stops itself: its client code quits the application when it is not connected to the shell, and its update loop starts the exit sequence when a status challenge goes unanswered. The plugin suppresses both. The launcher places BepInEx next to the exe in a local view folder; the plugin is a normal drop-in copied there.

**Why GStreamer:** the attract is a series of MP4 movies.

## 5. Input

Not measured. The placeholder layout is in place; on the cabinet, coin, START and the gun go through the shell's I/O board, which RavenGun does not run now.

## 6. Timing

**MEASURED** (2026-10-17): the attract was on screen for 2 minutes. Time from double-click to the logo not recorded.

## 7. What we saw on screen

**MEASURED** (2026-10-17): the logo, the attract movies, "PRESS START BUTTON TO JOIN" and FREEPLAY. Earlier, through the shell chain (2026-10-14), the game showed its logo and "PLEASE CALL ATTENDANT - 5 TICKETS OWED", then exited and restarted in a loop.

## 8. Current state and open questions

- The game starts and shows its attract; it is not yet called working.
- Open: coin, START and the gun (not measured), and a five-minute run.

## 9. What we tried and what did not work

- Through the cabinet's shell chain (earlier): the shell's start-up checks could be passed on local copies of its files, but the game quit by itself about 4 seconds after loading, in a loop of eight restarts in four minutes.
- Direct start on TeknoParrot's closed core: BepInEx did not load, the game vanished after the logo.
- Direct start on RavenGun's core, with the BepInEx plugin, DXVK and GStreamer: attract on screen (2026-10-17).

## 10. What is Linux-specific, and what differs on Windows

Wine-specific work: DXVK overrides for Unity Direct3D 11, GStreamer for the movies, and BepInEx's `winhttp` loader (`winhttp=n,b`). On the cabinet the shell and the I/O hardware are real; here the game runs without the shell and the plugin keeps it from quitting. See [Wine-Notes](Wine-Notes).

This page covers the game and the loader: what you need to run this title and where it gets stuck.

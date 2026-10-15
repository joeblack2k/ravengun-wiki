# Men in Black

**Status:** Not working yet (parked). The cabinet's shell chain launches the game and it shows its logo, then it exits and restarts in a loop.

## 1. Platform and cabinet

SEGA Amusements ticket-redemption light-gun cabinet (Windows PC). Build `240913RED`, shell "Game Shell" `230307RED` (**MEASURED** from the install files). The game `MIB.exe` is 64-bit, Unity 2020.3.14; the shell `Shell.exe` is 32-bit. The dump is about 6.7 GB and corresponds to the cabinet's `C:\Sega\` folder.

## 2. What the game needs

- RavenGun ships no games: you need your own copy of the game.
- Wine with DXVK (`DllOverrides = d3d11,d3d10core,dxgi=n,b`) in a dedicated prefix.
- Fixed paths under `C:\Sega\` (shell reads `Shell\game.ini`, `Launcher\launcher.ini`, `ShellData`, `GameData`; the game reads `ShellData\ShellData.ini`).
- The cabinet hardware (an I/O board, a serial line, ticket and card hardware) is provided by RavenGun; this part is not complete yet.
- The shell and game talk to each other over a local socket.
- It is the same shell family as [Transformers: Shadows Rising](Transformers-Shadows-Rising), one generation newer.

## 3. The official start script, or why there is none

The cabinet runs `SystemLauncher.exe` (replaces the Windows shell), which starts `Shell.exe`, which starts `MIB.exe`. The shell refuses to run without a checksum of its own file on its command line (the launcher supplies it on the cabinet).

## 4. The route we use

Windows route, direct, on RavenGun's own core, with the cabinet's own chain started (**MEASURED** from `game.ini`):

- `[Game] Executable = shell.exe;MIB.exe`, `Is64Bit = false`
- `[Launch] Mode = direct`, `Arguments = /k=e6222935`
- `[Loader] Core = ravengun`
- `[Wine] Prefix = ravengun-test-mib`, `DllOverrides = d3d11,d3d10core,dxgi=n,b`, `Runner = wrapper`

The shell has four start-up checks; on view-local copies of its files all four were passed in the run called m6, and it then launches the game. The shared recipe for this shell family is in [Transformers: Shadows Rising](Transformers-Shadows-Rising).

## 5. Input

No input was tried. The cabinet I/O board is only simulated as present for the shell; it delivers no data (the I/O log is full of "Lost HiD Handle" lines). Credits are set to 3 by the shell and the cabinet type to STANDARD.

## 6. Timing

Game load about 37 s; the game instance then lived 30 to 52 s before exiting (**MEASURED**, 4-minute run: eight restart cycles). Never held for five minutes.

## 7. What we saw on screen

**MEASURED** (2026-10-14): MIB logo, then the text "PLEASE CALL ATTENDANT - 5 TICKETS OWED / 14 TICKETS OWED". About 4 s after assets finish loading the game quits; the shell logs "Unexpect Game termination, retrying" and starts it again.

## 8. Current state and open questions

- The game quits by its own decision (no crash stack in the Unity log).
- **Cause not determined.** Two candidates, both present: the game sends a handshake message to the shell twice (10 s apart) that the shell does not answer; and the game logs "NOT Connected to serial" (in a run where an unrelated COM port was visible, it connected and lived slightly longer).
- Not yet shown: input, sound, an independent capture.

## 9. What we tried and what did not work

- Shell as it is, no argument: parks at the first check.
- With the `/k=` checksum argument: passes the first check, stops at the I/O board check.
- Local copy of the shell with a small change so it believes an I/O board is present, plus two debug switches in the view's `Game.ini`: all four checks pass, the game launches (run m6).
- Direct start without the shell: not workable for the full chain.

## 10. What is Linux-specific, and what differs on Windows

Wine-specific work: the shell's checks, a serial device that the game opens by itself (on Linux a host serial device may be seen by the game and must be hidden from it), and the DXVK overrides for Unity D3D11. On the cabinet all of this is real hardware. See [Wine-Notes](Wine-Notes).

This page covers the game and the loader: what you need to run this title and where it gets stuck.

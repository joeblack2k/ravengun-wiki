# Mighty Moto

**Status:** Not working yet. Never started: identified only, and it is probably not a lightgun game.

## 1. Platform and cabinet

UNIS PC based cabinet (**INFERRED**). The game is a 32-bit Unity program (`motobikeV1.0.9.exe`, 7,561,728 bytes) that talks to a local SmartFoxServer 1.6.6 (Java, port 9339) and uses a COMM installation (`MSCOMM32.OCX`).

## 2. What the game needs

- RavenGun ships no games: you need your own copy of the game.
- Java, to run the local SmartFoxServer.
- The game's cabinet start sequence: the cabinet's `SysStart.bat` starts the server first, then `start.exe`, then the game.
- Serial/COMM hardware: provided by RavenGun where possible (nothing measured).

## 3. The official start script, or why there is none

The cabinet's `SysStart.bat` starts, in order: the SmartFoxServer, `start.exe`, then the game (**INFERRED** from the batch file). RavenGun has no equivalent start sequence yet.

## 4. The route we use

No working route. The profile is a placeholder:

- `[Game] Type = TeknoParrot`, `Executable = motobikeV1.0.9.exe`
- `[Launch] Mode = direct`
- `[Input] Route = tp-shm`, `Layout = WartranTroopers` (placeholder; no suitable layout exists)

There is no TeknoParrot profile template for this game, so no emulation profile, config values or board exist. It needs its own start (server plus game) and an input route that does not exist yet.

## 5. Input

Unknown. The research notes say it is not a lightgun game (a motorbike game), so the usual aim/trigger layouts do not apply. Nothing was measured.

## 6. Timing

Not measured yet.

## 7. What we saw on screen

Nothing: never started.

## 8. Current state and open questions

- Never started; nothing measured.
- Open: a start sequence for the server plus game, and an input route.
- Low priority: it is not a lightgun title.

## 9. What we tried and what did not work

Nothing was tried.

## 10. What is Linux-specific, and what differs on Windows

It is a Windows/Unity game, so it would run under Wine on Linux. The Java server it needs is a plain Java program and should run natively. No Linux-specific findings yet. See [Running-on-Linux](Running-on-Linux).

This page covers the game and the loader: what you need to run this title and where it gets stuck.

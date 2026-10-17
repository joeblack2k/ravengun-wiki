# Mighty Moto

**Status:** Skipped (2026-10-17) under the owner's rule for a 4:3 picture without a 16:9 mode: the game's own output log shows a 1024x768 desktop and there is no resolution option. The profile is removed and the game folder is moved aside.

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

Skipped, so no route is kept. The profile was a placeholder (`Type = TeknoParrot`, `Executable = motobikeV1.0.9.exe`, `Route = tp-shm`) with no suitable layout.

## 5. Input

Unknown. The research notes say it is not a lightgun game (a motorbike game), so the usual aim/trigger layouts do not apply. Nothing was measured.

## 6. Timing

Not measured.

## 7. What we saw on screen

**MEASURED** from the cabinet's own `output_log.txt`: a 1024x768 (4:3) desktop; there is no resolution or aspect option. The executable's code section is also stored encrypted, and the game reports that it cannot reach its runtime environment.

## 8. Current state and open questions

- **Skipped (2026-10-17)** under the owner's rule: Japanese text and/or 4:3 without a 16:9 mode. Reason for this title: 4:3 (measured), with no 16:9 mode.
- It is also not a lightgun game.
- Nothing more is planned for this title.

## 9. What we tried and what did not work

Nothing was tried at runtime before the title was skipped.

## 10. What is Linux-specific, and what differs on Windows

It is a Windows/Unity game, so it would run under Wine on Linux. The Java server it needs is a plain Java program and should run natively. No Linux-specific findings yet. See [Running-on-Linux](Running-on-Linux).

This page covers the game and the loader: what you need to run this title and where it gets stuck.

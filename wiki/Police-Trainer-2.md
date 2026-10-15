# Police Trainer 2

**Status:** Not working yet. Never started: same blockers as [Crossfire: Maximum Paintball](Crossfire-Maximum-Paintball) (port I/O and a gun kernel driver), plus a second program.

## 1. Platform and cabinet

Phantom Systems PC based light-gun cabinet (**INFERRED** from the goal list). The game is a 32-bit (i386) Linux program. There are two programs: the game `pt2s_g11` and a sound program `pt2snd.f7` that the original loader starts first.

## 2. What the game needs

- RavenGun ships no games: you need your own copy of the game.
- 32-bit Linux libraries (only libc, libm, libGL and libX11 are needed).
- Hardware the cabinet provides: direct I/O ports (`iopl`; the game requires "port must be 37c") and the gun kernel driver `/dev/mjg`, which delivers light pulses. A normal Linux host has neither.

## 3. The official start script, or why there is none

No start script is used. On the original setup the sound program is started first, then the game. The route entry currently starts only the game.

## 4. The route we use

Native Linux route under gamescope (**INFERRED** from the route entry):

- `[Game] Type = ElfLdr2`, `Executable = pt2s_g11`, `Executable2 = pt2snd.f7`, `HasTwoExecutables = true`, `LaunchSecondExecutableFirst = true`, `EmulationProfile = RawThrillsGUN`
- `[Input] Route = evdev` (placeholder)
- The route entry is disabled.

Needed (as for Crossfire): a port-I/O shim, a fake `/dev/mjg`, and a way to run both programs in the same sandbox.

## 5. Input

No input route yet; see [Crossfire: Maximum Paintball](Crossfire-Maximum-Paintball). Default config: input API RawInput, windowed, 640x480, FPS limit off.

## 6. Timing

Not measured yet.

## 7. What we saw on screen

Nothing: never started.

## 8. Current state and open questions

- Never started; statically examined 2026-10-14.
- Open: everything listed under the route; additionally the sound program must run next to the game.

## 9. What we tried and what did not work

Nothing was run.

## 10. What is Linux-specific, and what differs on Windows

Linux-native game; no Wine. The blockers are cabinet-specific kernel interfaces that a stock Linux session does not have. See [Running-on-Linux](Running-on-Linux).

This page covers the game and the loader: what you need to run this title and where it gets stuck.

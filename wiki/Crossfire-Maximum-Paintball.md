# Crossfire: Maximum Paintball

**Status:** Not working yet. Never started: the game talks to port I/O and a gun kernel driver that do not exist on a normal Linux host, and RavenGun has no shim for them yet.

## 1. Platform and cabinet

Linux PC based light-gun cabinet (Raw Thrills-style game with a Phantom Systems-style engine, **INFERRED**: it shares its engine with [Police Trainer 2](Police-Trainer-2)). The game is a small 32-bit (i386) Linux program, `med_pball` (161 kB). Resolution 512x384 by default.

## 2. What the game needs

- RavenGun ships no games: you need your own copy of the game.
- 32-bit Linux libraries: `libglut.so.3`, `libXi.so.6`, `libGLU.so.1` (i386); RavenGun supplies these.
- Two things the cabinet provides in hardware: direct I/O ports (the game calls `iopl` and then uses `inb`/`outb`; it complains "/dev/p37c must exist or user must be root") and a gun kernel driver `/dev/mjg` that delivers light pulses. Neither exists on a normal Linux host.

## 3. The official start script, or why there is none

No start script is used; the cabinet runs the Linux program directly. RavenGun's route also starts it directly, with the game folder mounted in its sandbox.

## 4. The route we use

Native Linux route, gamescope (**INFERRED** from the route entry):

- `[Game] Type = ElfLdr2`, `Executable = med_pball`, `EmulationProfile = RawThrillsGUN`
- `[Input] Route = evdev` (placeholder: no real input route yet)
- The route entry is disabled.

What would be needed (**INFERRED**): a shim that makes `iopl` succeed and emulates the port instructions (they raise SIGSEGV for an unprivileged process), and a fake `/dev/mjg` that RavenGun feeds from the Move, mouse or controller.

## 5. Input

No input route exists yet. The guns are read through `/dev/mjg` as light pulses; the planned approach is to synthesise those from RavenGun's aim data. Buttons arrive over the port I/O. Nothing has been tried.

## 6. Timing

Not measured yet.

## 7. What we saw on screen

Nothing: never started.

## 8. Current state and open questions

- Never started; only statically examined (2026-10-14).
- Open: the port-I/O shim, the `/dev/mjg` emulation, and the input mapping. Same work item as [Police Trainer 2](Police-Trainer-2), which should be solved together.

## 9. What we tried and what did not work

Nothing was run. Natively the game fails at `iopl` (no root) and at the missing `/dev/p37c` and `/dev/mjg`; that was read from the program, not measured in a run.

## 10. What is Linux-specific, and what differs on Windows

This is a Linux-native game: there is no Wine involved. The problem is that it was built for a cabinet where the game runs privileged and talks to I/O ports and a gun driver; a normal Linux user session has neither. See [Running-on-Linux](Running-on-Linux).

This page covers the game and the loader: what you need to run this title and where it gets stuck.

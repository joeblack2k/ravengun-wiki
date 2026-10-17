# America's Army Arcade

**Status:** Starts (2026-10-16). Double-click runs the native Linux game on RavenGun's route and shows the attract and ranking screens (free play, 4:3 at 800x600). Start/coin keys and aiming are still open.

## 1. Platform and cabinet

Global VR "PC Based" light-gun cabinet (**INFERRED**). The game is a native Linux program: a 32-bit (i386) Unreal Engine 2 title, executable `armyops-bin` in the game's `System/` folder, using SDL 1.2. Two players.

## 2. What the game needs

- RavenGun ships no games: you need your own copy of the game.
- 32-bit Linux support on the host (the game is i386). SDL 1.2 comes from the game folder itself; `libstdc++.so.5` is supplied by RavenGun from its ElfLdr2 library set.
- A real mouse, for now (see Input).
- The game's own home directory (`System/env/home` in the dump) is used.

## 3. The official start script, or why there is none

No start script is used. The cabinet starts the Linux program directly; RavenGun does the same inside its sandbox, with the game folder mounted and the working directory set to `System/`.

## 4. The route we use

Native Linux route in a sandbox, under gamescope (the route is switched on since 2026-10-16):

- `[Game] Type = ElfLdr2`, `Executable = armyops-bin`
- `[Input] Route = evdev`

The profile defaults (from the profile template): input API RawInput, windowed, free play on, difficulty Medium.

## 5. Input

The game reads input through SDL, i.e. the X mouse and keyboard. Its own `System/DefUser.ini` defines (**MEASURED** from the file):

- **F1** = start player 1, **F2** = start player 2
- **C** = coin
- Left mouse button = fire

Two open problems (**MEASURED**/**INFERRED**):

1. The RavenGun daemon sends the keys `1` and `5` for start and coin, not F1 and C.
2. The virtual lightgun device does not move the X cursor (it is ignored by libinput on purpose), so aiming only works with a physical mouse.

## 6. Timing

Not measured yet: the time to attract and a five-minute run have not been recorded.

## 7. What we saw on screen

**MEASURED** (2026-10-16): the attract loop and the ranking screen with FREE PLAY, in a 4:3 picture (800x600) inside the 16:9 output.

## 8. Current state and open questions

- The game starts and shows its attract; it is not yet called working.
- Open: map RavenGun's start and coin to the game's F1 and C (or change the keys in `DefUser.ini`), and make the virtual lightgun move the cursor the game reads; aiming works with a physical mouse only.
- The difficulty option exists in the profile (Easy, Medium, Hard).

## 9. What we tried and what did not work

Static study first (2026-10-14: i386 ELF, Unreal Engine 2, library dependencies, input configuration file), then the native route above. No variants have been needed to reach the attract.

## 10. What is Linux-specific, and what differs on Windows

This is a Linux-native game, so there is no Windows or Wine layer involved. On the original cabinet it runs on a Linux PC with a light-gun interface; RavenGun supplies input through the X mouse/keyboard path because the game uses SDL 1.2. See [Running-on-Linux](Running-on-Linux).

This page covers the game and the loader: what you need to run this title and where it gets stuck.

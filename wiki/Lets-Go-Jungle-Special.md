# Let's Go Jungle Special

**Status:** Working (2026-10-15). Native Linux on the Lindbergh route: double-click in the app, `lgjsp_app` (the ride version) with `lindbergh.so`, `librg-stackalign.so`, passthrough fix 0003 and ride patch 0004. At boot press START for the ride reset, then coin and START. Played 5.5 minutes in mouse mode: game rounds, GAME OVER, next game.

## 1. Platform and cabinet

- SEGA Lindbergh Yellow; the game is a 32-bit Linux ELF (`lgjsp_app`), the **ride** (motion) version of Let's Go Jungle.
- Light gun game on the Lindbergh Type 3 style I/O board.
- RavenGun ships no games: you need your own copy of the game folder.

## 2. What the game needs

- The cabinet hardware a Lindbergh game expects, provided through `lindbergh.so` (lindbergh-loader, built locally by RavenGun's build script; not shipped).
- `librg-stackalign.so`, libCg 2.0 (shaders recompiled for Mesa), 32-bit libraries from RavenGun's `lib32`.
- Game ID in lindbergh-loader: `0x240beedc`. Launch resolution 1024x768 (4:3).
- Ride hardware: the cabinet's motion base is not present; RavenGun answers its after-game messages (patch 0004).

## 3. The official start script, or why there is none

The cabinet boots into the game. RavenGun starts the ELF itself in a sandbox through gamescope, with the preload libraries. See [Official-Start-Scripts](Official-Start-Scripts).

## 4. The route we use

```ini
[Game]
Type = Lindbergh
EmulationProfile = SegaJvsLetsGoJungle

[Input]
Route = jvs
Board = Lindbergh
```

- Route entry: `jvs = passthrough`, `stackalign = true`, `libcg = true`, zink.
- **Patch 0003 (MEASURED):** the game waits 1 second for a reply to its JVS packets; the baseboard layer passes the packets to the daemon in time.
- **Patch 0004:** answers the ride version's after-game messages (the route notes name it "after-game replies"); the next game then starts normally (**MEASURED**: GAME OVER, next game).
- `lindbergh.ini` as for [Lets-Go-Jungle](Lets-Go-Jungle): `REGION = EX`, `FREEPLAY = none`, `INPUT_MODE = 1`, `GPU_VENDOR = 2`.

## 5. Input

- **At boot press START first.** That is the ride reset. After it: coin key `5`, START key `1`.
- Shooting by mouse or PS Move; reload is `BUTTON_2` (gun beside the screen). **MEASURED** in mouse mode.

## 6. Timing

- Played: 5.5 minutes through several rounds, GAME OVER and the next game. **MEASURED.**
- Boot to attract and frame pacing: not measured.

## 7. What we saw on screen

The ride reset prompt, attract, game rounds, GAME OVER, then the next game starting.

## 8. Current state and open questions

- Open: real PS Move, player 2, sound.
- Open: the motion base itself is not emulated.

## 9. What we tried and what did not work

The patches are needed for the I/O replies (section 4); what the game does without them was not recorded. Not measured yet beyond that.

## 10. What is Linux-specific, and what differs on Windows

- No Windows version. On Linux the cabinet hardware is a preload library and the daemon's JVS board.
- The ride reset step has no equivalent on a flat cabinet; here it is a plain START press.

This page covers the game and the loader: what you need to run this title and where it gets stuck.

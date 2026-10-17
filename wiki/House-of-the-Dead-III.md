# The House of the Dead III

**Status:** Not starting yet (2026-10-17). SEGA Chihiro (Xbox-based) game; Cxbx-Reloaded under Proton does not get past its early threads (see section 7). No picture has been seen.

## 1. Platform and cabinet

SEGA Chihiro (an Xbox-based arcade platform; **INFERRED** from the goal list: "SEGA Chihiro (Xbox-emulation)").

## 2. What the game needs

- RavenGun ships no games: you need your own copy of the game.
- An Xbox emulation route for the SEGA Chihiro hardware. RavenGun has tried Cxbx-Reloaded under Proton (section 4).
- The profile family has a `Region` setting (the Cxbx-Reloaded region in an emulator configuration; **INFERRED**).

## 3. The official start script, or why there is none

Not known; the original machine boots the Xbox-based system directly.

## 4. The route we use

No finished route. The route under test is Cxbx-Reloaded run under Proton; it is started from RavenGun but does not reach a picture (details in section 8).

## 5. Input

Not known. No input route has been built before the emulation itself starts.

## 6. Timing

Not measured: no picture was reached.

## 7. What we saw on screen

Nothing: no picture. Under Proton 11 the Xbox main thread waits and two other threads fault; under GE-Proton10-34 the emulation does not start (details in section 8).

## 8. Current state and open questions

Measured with Cxbx-Reloaded (**MEASURED**, 2026-10-17; the findings are the same for both games):

- Under Proton 11 the Xbox main thread waits, and two other threads fault on an aligned SSE move (`MOVAPS`) because the stack is not aligned to 16 bytes. The faulting code lives in the mirrored physical memory region of the emulated Xbox (the 0xF7xxxxxx range), and it is the same in both games.
- Under GE-Proton10-34 the emulation does not start at all.
- The task of the Chihiro family is to measure only whether a passthrough loader (Cxbx-like, native x86) is feasible; nothing is playable.
- See also [Virtua Cop 3](Virtua-Cop-3), which has the same platform and the same findings.

## 9. What we tried and what did not work

- Cxbx-Reloaded under Proton 11: Xbox main thread waits, two threads fault on a misaligned `MOVAPS` in the mirrored physical memory region.
- Cxbx-Reloaded under GE-Proton10-34: the emulation does not start.
- Nothing else was tried.

## 10. What is Linux-specific, and what differs on Windows

The platform is neither a Windows PC nor a Linux PC: the game is an Xbox-class title. On Linux the emulator itself is a Windows program run under Proton, which adds its own stack-alignment and memory-mapping problems. See [Running-on-Linux](Running-on-Linux).

This page covers the game and the loader: what you need to run this title and where it gets stuck.

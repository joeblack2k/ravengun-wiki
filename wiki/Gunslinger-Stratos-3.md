# Gunslinger Stratos 3

**Status:** Skipped (2026-10-17) under the owner's rule for Japanese text without a 16:9 mode: the text is Japanese (measured in the game's own attract movie and default tutorial), and it is not a lightgun game. The profile is removed and the game folder is moved aside.

## 1. Platform and cabinet

Taito Type X4 cabinet (**INFERRED** from the goal list). The game is a 64-bit Windows program.

## 2. What the game needs

- RavenGun ships no games: you need your own copy of the game.
- Wine/Proton with 64-bit support.
- Native `xaudio2_7` and a FastIO pipe were needed to get as far as the measurements below.

## 3. The official start script, or why there is none

No start script is used; the cabinet boots Windows into Taito's launcher. RavenGun has no start route for this title.

## 4. The route we use

Skipped, so no route is kept. What was tried (**MEASURED**, 2026-10-17): the first game recognition matched [Cooper's 9](Coopers-9) because a size entry was missing in the profile; then native `xaudio2_7` and the FastIO pipe; after that the game ran at 60 fps with a black picture because the assets were not found.

## 5. Input

Unknown. No input layout, JVS board or Move mapping has been chosen.

## 6. Timing

Not measured.

## 7. What we saw on screen

Black picture at 60 fps without assets. The Japanese text was **MEASURED** in the game's own attract movie `gs3_pv1.wmv` and in the default tutorial; only 6 of the 21 tutorial movies have an English version.

## 8. Current state and open questions

- **Skipped (2026-10-17)** under the owner's rule: Japanese text and/or 4:3 without a 16:9 mode. Reason for this title: the text is Japanese (measured), and it is not a lightgun game.
- Nothing more is planned for this title.

## 9. What we tried and what did not work

See section 4: wrong recognition, missing audio library and pipe, then a black picture without assets. Nothing was fixed before the title was skipped.

## 10. What is Linux-specific, and what differs on Windows

Would be a Windows game under Wine; no Linux-specific findings. See [Running-on-Linux](Running-on-Linux).

This page covers the game and the loader: what you need to run this title and where it gets stuck.

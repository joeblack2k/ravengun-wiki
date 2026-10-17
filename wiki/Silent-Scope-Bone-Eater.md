# Silent Scope: Bone Eater

**Status:** Starts (2026-10-17). A double-click runs the 64-bit game (TeknoMacaw) with DXVK in gamescope, region Asia (English): warning screen, then the attract with the ranking and free play. The picture is portrait, centred in 16:9. Input has not been measured.

## 1. Platform and cabinet

Konami PC based hardware (TeknoMacaw, 64-bit). The game's main module is `arkndd.dll`; the cabinet has a portrait screen and a sniper-rifle style light gun. A scope shows on the same screen as an overlay.

## 2. What the game needs

- RavenGun ships no games: you need your own copy of the game.
- Wine with DXVK (with wined3d the picture stayed black).
- The three TrueType collections the game loads through GDI+ must be usable as single fonts (see section 4).
- Region: Asia, which gives English text.

## 3. The official start script, or why there is none

The cabinet boots Windows into the game. RavenGun starts the game itself, from a double-click in the RavenGun app.

## 4. The route we use

Windows route, direct, 64-bit:

- `[Game] Type = TeknoMacaw`, `EmulationProfile = KonamiAcio`, `Executable = arkndd.dll`
- `[Launch] Mode = direct`, `Dxvk = true`
- `[Launch] ViewRealDirs = data/font`, `ViewTtcAsTtf = data/font/df_heiseigothic_w5.ttc, data/font/df_heiseigothic_w7.ttc, data/font/df_sougei_w5.ttc`
- `[Display] Gamescope = true`
- `[Input] Route = tp-shm`, `Layout = KonamiAcio`
- Config: Input API RawInput, DisplayMode Windowed (under gamescope), Region Asia, Screen Layout Single Screen Scope.

**Why `ViewTtcAsTtf`:** Wine's GDI+ call that adds a font from memory does not accept a TrueType collection (`.ttc`), and the game stopped with "No font loaded or no font families data in font file". RavenGun makes a local copy of face 0 of each named collection as a single font in the game's view folder (the game folder itself is never written); `ViewRealDirs` makes the surrounding folder a real folder so the local copy can be placed there.

## 5. Input

Layout `KonamiAcio`. **Not measured in the game yet**; the sniper-rifle game probably needs a scope or zoom button next to the trigger (assumption).

## 6. Timing

Not measured: the time to the attract and a five-minute run have not been recorded.

## 7. What we saw on screen

**MEASURED** (2026-10-17): the English warning screen, then the attract with the ranking and FREE PLAY. The picture is portrait, centred in the 16:9 output.

## 8. Current state and open questions

- The game starts and shows its attract; it is not yet called working.
- Open: coin, START, the scope and aiming (input not measured), and a five-minute run.

## 9. What we tried and what did not work

- wined3d: the picture stayed black. Fixed by DXVK.
- Without `ViewTtcAsTtf`: the game stopped at start with the font error above. Fixed by the local single-font copies.

## 10. What is Linux-specific, and what differs on Windows

Wine-specific: Wine's GDI+ does not accept TrueType collections, so the fonts are converted in a local view; DXVK is needed for the picture. On the cabinet the game runs directly on Windows. See [Wine-Notes](Wine-Notes).

This page covers the game and the loader: what you need to run this title and where it gets stuck.

# Walking Dead

**Status:** Not working yet (2026-10-15). On RavenGun's native Linux route the game starts and prints "Welcome to Walking Dead v01.05", then stops: it cannot load 41 of its definition/data files because data the cabinet supplies at runtime is not in the tested dump.

## 1. Platform and cabinet

- Raw Thrills Linux PC-based lightgun cabinet; "The Walking Dead". The game file `game` (about 19 MB) is a 32-bit i386 Linux ELF (`ET_EXEC` at `0x08048000`, no section headers) taken as a memory dump of the running game. **MEASURED**
- The cabinet is a "mounted gun" cabinet: aim is read from the RIO board's channels 19..22 (the game logs "Defaulting to mounted gun"). **INFERRED**
- Template profile: TeknoParrot `WalkingDead` (revision 6), emulation profile `RawThrillsGUN`.

## 2. What the game needs

- Your own dump of the game folder; RavenGun ships no games.
- 32-bit libraries: `libGLU.so.1`, `libcsv.so`, OpenSSL 1.0.0 (`libssl.so.1.0.0`, `libcrypto.so.1.0.0`) and `libcaca.so.0`. SteamOS has no i386 `libcaca`; RavenGun builds a stub.
- A table that names the game's import slots, because the dump contains stale cabinet addresses: `dropin/eerste-plt-slots.tsv` (**MEASURED**: 806 of 806 stale slots named; 34 of 34 cross-checks agree).
- RavenGun provides the cabinet hardware the game expects; the gun board is emulated by the RIO bridge.

## 3. The official start script, or why there is none

On the cabinet the game is started by its own startup scripts with `-f<res> -e`. RavenGun uses the same arguments (`-f1920x1080 -e`).

## 4. The route we use

**MEASURED** 2026-10-15: native Linux route, no Wine. Disabled in the app's automatic selection.

- Sandbox with your game folder at `/pm`.
- `rg-elfloader` with `RG_ELF_SLOT_TABLE` (the slot table above) and `RG_ELF_MAIN=1`: the dump was made after the constructors had run, so `main` is called as a function.
- The libcaca stub, the RIO bridge, `librg-threadprio.so`, `librg-glslfix.so`, 1920x1080 through gamescope.

```ini
[Input]
Route = tp-shm
Layout = RawThrillsGUN
```

## 5. Input

`librg_rio_bridge.so` answers as the cabinet's gun board over USB, using `rio-invoer.ini`: the report layout (19 switch fields, 4 analog fields) is the same as in Jurassic Park and needs no encryption in this game. Hook addresses for `pmrt_usb_open` / read / write / close were found by static analysis. Switch meanings are taken from Jurassic Park and not yet verified on this game, because the game does not run far enough to use them.

## 6. Timing

Not measured yet. Nothing past the welcome line has run.

## 7. What we saw on screen

The text "Welcome to Walking Dead v01.05" in the log. No picture beyond that is documented. 41 of the game's definition files (RTDT/adj) fail to load, and the game then exits.

## 8. Current state and open questions

- Blocking: the data that the cabinet supplies at runtime is not present in the tested dump, so the game cannot read its own definition files.
- Aiming through RIO channels 19..22 is untested.
- Nothing has been played.

## 9. What we tried and what did not work

- The dumped image needed a table naming its import slots; with it (806/806) the game starts and prints its welcome line.
- Calling `main` directly (`RG_ELF_MAIN`) was needed because the dump is post-constructor.
- The i386 `libcaca` was missing; a stub fixed that.

## 10. What is Linux-specific, and what differs on Windows

The game is a Linux program; on Windows TeknoParrot's ElfLdr2 loader would run it under Wine. RavenGun runs it natively. See also [Aliens Armageddon](Aliens-Armageddon) and [Ghostbusters](Ghostbusters).

This page covers the game and the loader: what you need to run this title and where it gets stuck.

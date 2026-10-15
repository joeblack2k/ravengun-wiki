# RavenGun

RavenGun runs arcade lightgun games on Linux. It starts each game itself — native Linux where the cabinet ran Linux, Wine/Proton (with Vulkan where possible) where it ran Windows — and feeds it input from a PS Move, a mouse or a game controller. The goal: on a freshly installed SteamOS PC, a first-run wizard asks for the permissions it needs and for the folder with your game backups, and from then on you double-click a game and play, with per-game options in the app. No TeknoParrot tools or loaders are needed.

RavenGun ships no games. You need your own legally obtained copies.

This wiki collects what was learned per title, so others can build on it. **38 of 68 titles work** from a double-click (see [Compatibility](Compatibility)); the other pages say where each title stops.

## How to read a game page

Every game page has the same ten sections: platform and cabinet, what the game needs, the official start script, the route RavenGun uses, input, timing, what was seen on screen, current state, what did not work, and what is Linux-specific. Claims are labelled **MEASURED** (seen or measured on a test machine) or **INFERRED** (read from the game's files or derived); an assumption is called one.

## General pages

- [Compatibility](Compatibility): every title with its platform and state
- [Running on Linux](Running-on-Linux): installing RavenGun, the first-run wizard, your game folder
- [Loader architecture](Loader-Architecture): how RavenGun starts a game: routes, profiles, drop-ins, input bridges
- [Official start scripts](Official-Start-Scripts): what the cabinets' own start scripts do, and how RavenGun reads them
- [Wine notes](Wine-Notes): Wine/Proton fixes and options: movies, DXVK, audio, window handling

## Working (38)

- [After Dark](After-Dark) — UNIS PC Based
- [Bug Busters](Bug-Busters) — EM-Teck PC Based
- [Drakons: Realm Keepers](Drakons-Realm-Keepers) — Adrenaline Amusements PC-Based
- [Dream Raiders](Dream-Raiders) — SEGA RingWide
- [Elevator Action Invasion](Elevator-Action-Invasion) — UNIS PC Based
- [Gashaaaan!!!!](Gashaaaan) — Konami PC Based
- [Ghost Squad Evolution](Ghost-Squad-Evolution) — SEGA Lindbergh Red
- [HALO Fireteam Raven](Halo-Fireteam-Raven) — RAW Thrills Linux PC Based
- [The House of the Dead EX](House-of-the-Dead-EX) — SEGA Lindbergh Red
- [House of the Dead: Scarlet Dawn](House-of-the-Dead-Scarlet-Dawn) — SEGA ALLS
- [Jurassic Park Arcade](Jurassic-Park-Arcade) — RAW Thrills Linux PC Based
- [Let's Go Island 3D: Lost on the Island of Tropics](Lets-Go-Island-3D) — SEGA RingEdge
- [Let's Go Island: Lost on the Island of Tropics](Lets-Go-Island) — SEGA RingWide
- [Let's Go Jungle Special](Lets-Go-Jungle-Special) — SEGA Lindbergh Yellow
- [Let's Go Jungle: Lost on the Island of Spice](Lets-Go-Jungle) — SEGA Lindbergh Red
- [Let's Go Safari](Lets-Go-Safari) — SEGA RingWide
- [Lethal Enforcers 3](Lethal-Enforcers-3) — Konami PC Based
- [Mario Kart: Arcade GP DX](Mario-Kart-Arcade-GP-DX) — Namco ES3A
- [Mars Sortie](Mars-Sortie) — UDC PC Based
- [Music GunGun 2](Music-GunGun-2) — Taito Type X2
- [NERF Arcade](NERF-Arcade) — Raw Thrills PC Based
- [Night Hunter - After Dark, Chapter 2](Night-Hunter-After-Dark-Chapter-2) — UNIS PC Based
- [Operation G.H.O.S.T.](Operation-GHOST) — SEGA RingWide
- [Point Blank X](Point-Blank-X) — Namco ES4
- [Primeval Hunt](Primeval-Hunt) — SEGA Lindbergh Red
- [Pull The Trigger](Pull-The-Trigger) — COVIELSA PC-Based
- [Rabbids Hollywood Arcade](Rabbids-Hollywood) — ADRENALINE PC Based
- [Raccoon Rampage](Raccoon-Rampage) — UNIS PC Based
- [Rambo](Rambo) — SEGA Lindbergh Red EX
- [Rampage](Rampage) — ADRENALINE PC Based
- [SEGA Golden Gun](SEGA-Golden-Gun) — SEGA RingWide
- [Silent Hill: The Arcade](Silent-Hill-The-Arcade) — Konami PC Based
- [Target: Terror Gold](Target-Terror-Gold) — Raw Thrills Linux PC Based
- [Terminator Salvation](Terminator-Salvation) — RAW Thrills Linux PC Based
- [Tomb Raider Arcade](Tomb-Raider-Arcade) — ADRENALINE PC Based
- [Too Spicy](Too-Spicy) — SEGA Lindbergh Red
- [Transformers: Shadows Rising](Transformers-Shadows-Rising) — Windows PC
- [Wild West Shootout](Wild-West-Shootout) — Coastal PC-Based

## Not working yet (30)

- [Aliens Armageddon](Aliens-Armageddon) — RAW Thrills Linux PC Based
- [Aliens: Extermination](Aliens-Extermination) — Global VR PC Based
- [America's Army Arcade](Americas-Army-Arcade) — Global VR PC Based
- [Block King Ball Shooter](Block-King-Ball-Shooter) — Type-X PC Based
- [Cooper's 9](Coopers-9) — KONAMI PC Based
- [Crossfire: Maximum Paintball](Crossfire-Maximum-Paintball) — Linux PC Based
- [Elevator Action Death Parade](Elevator-Action-Death-Parade) — Taito Type X2
- [Far Cry Paradise Lost](Far-Cry-Paradise-Lost) — Global VR PC Based
- [Friction](Friction) — Unique PC Based
- [Gaia Attack 4](Gaia-Attack-4) — Taito Type X2
- [Ghostbusters](Ghostbusters) — ICE/RT Linux PC Based
- [Gunslinger Stratos 3](Gunslinger-Stratos-3) — Taito Type X4
- [Haunted Museum](Haunted-Museum) — Taito Type X2
- [Haunted Museum II](Haunted-Museum-II) — Taito Type X2
- [The House of the Dead 4](House-of-the-Dead-4) — SEGA Lindbergh Red
- [The House of the Dead 4 Special](House-of-the-Dead-4-Special) — SEGA Lindbergh Yellow
- [The House of the Dead III](House-of-the-Dead-III) — SEGA Chihiro
- [Infinity Blade FX](Infinity-Blade-FX) — ADRENALINE PC Based
- [Lost Land Adventure](Lost-Land-Adventure) — Namco ES3X
- [Luigi's Mansion Arcade](Luigis-Mansion) — SEGA Nu 1.1
- [Men in Black](Men-in-Black) — Windows PC
- [Mighty Moto](Mighty-Moto) — UNIS PC Based
- [Police Trainer 2](Police-Trainer-2) — Phantom Systems PC Based
- [Robin Hood](Robin-Hood) — ICE PC Based
- [Silent Scope: Bone Eater](Silent-Scope-Bone-Eater) — Konami PC-Based
- [Star Trek Voyager](Star-Trek-Voyager) — Team Play PC Based
- [Time Crisis 5](Time-Crisis-5) — Namco ES3X
- [Transformers: Human Alliance](Transformers-Human-Alliance) — SEGA RingEdge 2
- [Virtua Cop 3](Virtua-Cop-3) — SEGA Chihiro
- [Walking Dead](Walking-Dead) — RAW Thrills Linux PC Based

This page covers the game and the loader: what you need to run this title and where it gets stuck.

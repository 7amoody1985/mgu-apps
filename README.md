# 7amoody1985's MGU apps

A source for the [MGU Store](https://github.com/robertnisipeanu/mgu-store) on BMW iDrive 7 head units (MGU).
Unofficial: nothing here is made, endorsed or supported by BMW AG.

> [!WARNING]
> **Everything in this repository is experimental.** The apps are personal projects, tried on one car (a G05 X5
> with iDrive 7) or not yet tried in a car at all. They may not work on yours, may stop working after a head-unit
> update, and come with no warranty or support. Install them at your own risk, with the car parked, and keep
> your eyes on the road.

## Add it to the Store

In the Store: **Settings → Add source**, type `7amoody1985/mgu-apps` and pick **Releases**. The Store reads
`catalog.json` from this repository's release tagged `catalog`.

## Apps

| App | Version | What it is |
|---|---|---|
| RideTube (fork) | app 0.4.0, service 0.4.2 | A modified build of [JustAnotherPU's RideTube](https://github.com/JustAnotherPU/ridetube), a YouTube client. Fixes the Search menu (which holds the settings) closing right after it opens; the service streams the video in RAM instead of writing it to the head unit's flash, and keeps a debug report. Not endorsed by the original developer. Its own ids (`mdq_ridetube`, `mdq-ridetube-d`): it installs beside the original. Source and changes: [7amoody1985/ridetube](https://github.com/7amoody1985/ridetube). |
| CarLink (experimental) | 0.1.2 | The next turn from HudHud or Google Maps on your phone, in the middle of the instrument cluster and as a home-screen widget. **Not yet tried in a car.** |

### CarLink (experimental)

- **Status: first version, not yet tried in a car.** Tested on a PC in the kit's emulator only.
- It shows what the CarLink phone app sends: that app reads the navigation notification of HudHud or Google
  Maps and draws the turn card (arrow, distance, street, arrival time), and sends it over the car's Wi-Fi to
  port 47800. The phone app isn't published yet.
- **Demo** (on the app's screen) shows turns without the phone, to try the cluster and the widget.
- Needs **cluster-render**, the cluster renderer from the `robertnisipeanu/idrive-apps` source (Waze on cluster
  installs it too); the Store installs it first. It doesn't touch CarPlay or Android Auto.
- Settings: show on the cluster (on), on the HUD (off), and how long a quiet phone may be before the card goes.
- **Debug mode** (0.1.1): the phone app's Car log screen reads this app's log file, its live log and a status
  snapshot (the phone link, the route, cluster-render's layers and targets) over the same link. Since 0.1.2
  also the RideTube fork service's debug report (`status.json` and its recent plays from `sessions.jsonl`),
  when that service is installed; neither holds what was watched.

### RideTube (fork)

- **Status: the service's RAM streaming is not yet tried in a car.** Tested on a PC: its tests, and a live
  streaming check against YouTube.
- **Its own ids:** the app is `mdq_ridetube` (the tile says "RideTube (fork)"), its service `mdq-ridetube-d`.
  It installs beside JustAnotherPU's RideTube (`jap_ridetube`, `jap-ridetube-d`) and never over it; both can be
  installed, but only one plays at a time. Keep `JustAnotherPU/mgu-apps:releases`: Node.js 22 (`jap-node22`)
  comes from it.
- **From the fork's 0.3.9 / 0.4.1** (installed here as `jap_ridetube` / `jap-ridetube-d` before 2026-11-09): this
  source lists those ids no more. Uninstall them (Installed page: the app, then the service), then install
  **RideTube (fork)**. Sign in to YouTube again: the sign-in belonged to the old service.
- **The video in RAM:** the service mounts a 256 MB RAM disk and keeps only about two and a half minutes of the
  playing video in it, instead of writing the whole video to flash. Seeking back more than 45 s fetches it again
  (a short pause). Videos it can't stream that way (very long ones, about 90 minutes and up) go to flash as before.
- **Debug report:** `/run/mdq-ridetube-d/status.json` (RAM, memory, the stream, refreshed every 10 s while in use)
  and `/var/opt/mdq-ridetube-d/log/sessions.jsonl` (one line a play). Neither holds what you watched. Over the
  car's hotspot: `ssh root@172.16.222.97 cat /run/mdq-ridetube-d/status.json`. The fields:
  [the service's README](https://github.com/7amoody1985/ridetube/blob/main/native/mdq-ridetube-d/README.md).
- Licence: GPL-3.0-or-later, as the original (the licence texts are in the packages); the source of this build is
  [7amoody1985/ridetube](https://github.com/7amoody1985/ridetube), its packages made with its
  `tools/build_app.sh` and `tools/build_service.sh`.

## Adding an app

The step-by-step checklist (also for coding agents) is [AGENTS.md](AGENTS.md); in short:

1. Put the built package in `packages/` as `<id>@<x.y.z>.tgz` (not committed: it goes into the release only).
   The package's `package.json` names the same id and version, and it holds no BMW SDK (`node_modules/oap-sdk`).
2. Add the app to `apps.json`: `id`, `kind` (`app` or `tool`), `title`, `description`, `version`, and as needed
   `requires` (`{"<id>": "<min version>"}`, also from other sources), `mguHmi` (`["ID7"]`), `uninstallable`,
   `icon` (a PNG in `icons/`, at most 128 KiB) and `"build": "unit"` for a source package the head unit builds.
   The id takes this source's prefix `mdq_` (`mdq_myapp`), never one BMW or another source uses.
3. Publish: `powershell -File tools\publish.ps1` (Python 3 and the GitHub CLI, signed in). It writes `dist/`
   (`catalog.json`, the packages, the icons) and uploads it to the `catalog` release.
4. Check it as the car sees it: `python -I tools/verify.py` (ends with `all ok`).
5. On the car: **Settings → Check now** in the Store.

The catalog format: [Publishing for the MGU Store](https://github.com/robertnisipeanu/mgu-store/blob/main/docs/PUBLISHING.md).

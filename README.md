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
| RideTube (fork) | app 0.3.9, service 0.4.0 | A modified build of [JustAnotherPU's RideTube](https://github.com/JustAnotherPU/ridetube), a YouTube client. Fixes the Search menu (which holds the settings) closing right after it opens; the service streams the video in RAM instead of writing it to the head unit's flash, and keeps a debug report. Not endorsed by the original developer. Source and changes: [7amoody1985/ridetube](https://github.com/7amoody1985/ridetube). |
| CarLink (experimental) | 0.1.1 | The next turn from HudHud or Google Maps on your phone, in the middle of the instrument cluster and as a home-screen widget. **Not yet tried in a car.** |

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
  snapshot (the phone link, the route, cluster-render's layers and targets) over the same link.

### RideTube (fork)

- **Status: the service's RAM streaming (0.4.0) is not yet tried in a car.** Tested on a PC with its tests only.
- This source offers both the app (`jap_ridetube`) and its service (`jap-ridetube-d`), with RideTube's own ids.
  Keep `JustAnotherPU/mgu-apps:releases`: Node.js 22 (`jap-node22`) still comes from it.
- The Store updates an installed app or tool only from the source it came from. If RideTube came from
  JustAnotherPU's source: **uninstall the RideTube app and then the RideTube service** there, then install
  RideTube from this source (it installs this source's service first). Uninstalling the service deletes the
  YouTube sign-in: sign in again in the app.
- **The video in RAM:** the service mounts a 256 MB RAM disk and keeps only about two and a half minutes of the
  playing video in it, instead of writing the whole video to flash. Seeking back more than 45 s fetches it again
  (a short pause). Videos it can't stream that way (very long ones, about 90 minutes and up) go to flash as before.
- **Debug report:** `/run/jap-ridetube-d/status.json` (RAM, memory, the stream, refreshed every 10 s while in use)
  and `/var/opt/jap-ridetube-d/log/sessions.jsonl` (one line a play). Neither holds what you watched. Over the
  car's hotspot: `ssh root@172.16.222.97 cat /run/jap-ridetube-d/status.json`. The fields:
  [the service's README](https://github.com/7amoody1985/ridetube/blob/main/native/jap-ridetube-d/README.md).
- To go back to the original: uninstall the app and the service here, then install RideTube from
  `JustAnotherPU/ridetube`.
- Licence: GPL-3.0-or-later, as the original (the licence texts are in the packages); the source of this build is
  [7amoody1985/ridetube](https://github.com/7amoody1985/ridetube), its packages made with its
  `tools/patch_package.py` and `tools/patch_service.py`.

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

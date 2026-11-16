# 7amoody1985's MGU apps

A source for the [MGU Store](https://github.com/robertnisipeanu/mgu-store) on BMW iDrive 7 head units (MGU).
Unofficial: nothing here is made, endorsed or supported by BMW AG.

> [!WARNING]
> **Released, but still being tested.** The apps here are released for anyone to try, but they have been tried
> on one car (a G05 X5 with iDrive 7) or not yet in a car at all. They may not work on yours, may stop working after
> a head-unit update, and come with no warranty or support. Install them at your own risk, with the car parked,
> and keep your eyes on the road.

## Add it to the Store

In the Store: **Settings → Add source**, type `7amoody1985/mgu-apps` and pick **Releases**. The Store reads
`catalog.json` from this repository's release tagged `catalog`.

## Apps

| App | Version | What it is |
|---|---|---|
| Heritage Cluster (experimental) | 0.2.0 | **⚠ Still under development, not yet tested in a real car. Use at your own risk** (see below). Classic BMW instrument clusters on the car's 12.3-inch digital cluster, in place of the stock dials: the E-series analogue cluster (X5 E53, 5 Series E39) with its warning LEDs, LCDs and lamps, and the F-series digital display (X5 F15, X6 F16, 5 Series F10, 7 Series F01) in Comfort and Sport. For any iDrive 7 car with the 12.3-inch cluster; laid out on a G05 X5. Needs the cluster renderer (`cluster-render`) from the `robertnisipeanu/idrive-apps` source, which the Store installs with it. Screenshots below. **Not yet tried in a car.** |

### Heritage Cluster: read before installing

Heritage Cluster is still under development and **has not yet been tested in a real car**; a test in a car is coming soon. While it runs, it replaces the picture on your instrument cluster. Install and use it entirely at your own risk: try it parked first, and uninstall it if anything looks wrong (the stock cluster comes back when the app stops or is removed). BMW's own warning lights stay on top of it, but it is not a certified instrument display, so don't rely on it to drive.

It is provided "as is", without warranty of any kind. The author is not responsible for any damage, fault, fine, injury or other consequence of installing or using it. It is not made, endorsed or supported by BMW AG.

#### Screenshots

As the app draws them on the 12.3-inch cluster (rendered on a PC through the app's own engine, at 116 km/h). The Store on the car shows no screenshots, so they are here. Pick the cluster, the look and the units in the app's settings.

| | |
|---|---|
| **E-series (X5 E53, 5 Series E39), night** | **E-series, day** |
| ![E-series, night](screenshots/heritage/x5_e53_night.png) | ![E-series, day](screenshots/heritage/x5_e53_day.png) |
| **F-series (X5 F15, X6, 5 and 7 Series), Comfort by day** | **F-series, Comfort at night** |
| ![F-series, Comfort by day](screenshots/heritage/x5_f15_comfort.png) | ![F-series, Comfort at night](screenshots/heritage/x5_f15_night.png) |
| **F-series, Sport** (follows the drive mode) |  |
| ![F-series, Sport](screenshots/heritage/x5_f15_sport.png) |  |

**Which cars.** Any BMW with iDrive 7 and the 12.3-inch cluster (Live Cockpit Professional): every one gives apps the same 1920x720 cluster panel. The layout keeps clear of the G05's driver camera and glass corners, so it fits cars without them too. Units, rev counter (petrol or diesel) and tank size are settings; on M cars the F-series display follows M Drive's engine mode. Where there is no such panel, the app draws nothing and says why on its own screen.

### No longer here

The RideTube fork (`mdq_ridetube`, `mdq-ridetube-d`) and CarLink (`mdq_carlink`) were listed here until 2026-11-17.
They are personal experiments and are no longer offered in this source; installed copies keep working but get no
updates from it. The RideTube fork's source stays at [7amoody1985/ridetube](https://github.com/7amoody1985/ridetube).

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

# 7amoody1985's MGU apps

A source for the [MGU Store](https://github.com/robertnisipeanu/mgu-store) on BMW iDrive 7 head units (MGU).
Unofficial: nothing here is made, endorsed or supported by BMW AG.

## Add it to the Store

In the Store: **Settings → Add source**, type `7amoody1985/mgu-apps` and pick **Releases**. The Store reads
`catalog.json` from this repository's release tagged `catalog`.

## Apps

| App | Version | What it is |
|---|---|---|
| RideTube (fork) | 0.3.8 | A modified build of [JustAnotherPU's RideTube](https://github.com/JustAnotherPU/ridetube), a YouTube client. Fixes the Search menu (which holds the settings) closing right after it opens. Not endorsed by the original developer. Source and changes: [7amoody1985/ridetube](https://github.com/7amoody1985/ridetube). |

### RideTube (fork)

- Keep the sources `JustAnotherPU/ridetube:releases` and `JustAnotherPU/mgu-apps:releases`: the RideTube service
  (`jap-ridetube-d`) and Node.js 22 still come from them. Only the app comes from here.
- The app keeps RideTube's id, `jap_ridetube`. The Store updates an installed app only from the source it came
  from, so if RideTube is installed from JustAnotherPU's source, **uninstall the RideTube app** first (not its
  service), then install it from this source. The YouTube sign-in is kept: the service holds it.
- To go back to the original: uninstall it here, then install RideTube from `JustAnotherPU/ridetube`.
- Licence: GPL-3.0-or-later, as the original (the licence texts are in the package); the source of this build is
  [7amoody1985/ridetube](https://github.com/7amoody1985/ridetube), its package made with its
  `tools/patch_package.py`.

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

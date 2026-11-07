# Publishing to 7amoody1985/mgu-apps (for agents)

This repository is an MGU Store source (BMW iDrive 7 head units). The car reads `catalog.json` from the GitHub
release tagged `catalog`; that file lists **every** app of this source, so one source offers them all.
`apps.json` (committed) is the list it is made from. Packages are release assets only, never committed.

- Local checkout: `C:\Users\PC\Documents\Code\Personal\bmw-idrive-apps\mgu-apps`
- GitHub: https://github.com/7amoody1985/mgu-apps (the GitHub CLI is installed and signed in as 7amoody1985;
  `gh` may not be on PATH: `C:\Program Files\GitHub CLI\gh.exe`)
- The Store's own rules: https://github.com/robertnisipeanu/mgu-store/blob/main/docs/PUBLISHING.md

## Publish a new app, or a new version

1. **Check the package** (`<id>@<x.y.z>.tgz`, an OAP package with its files under `package/` or at the root):
   - its `package.json` `name` is the id and `version` the same x.y.z;
   - **no `node_modules/oap-sdk`** in it (BMW's SDK is not redistributable; the head unit generates it);
   - the id has this source's prefix **`mdq_`** (`mdq_myapp`), never an id BMW or another source uses;
   - `"mguInternet": true` in `package.json` if it needs the internet;
   - a native daemon or binary is not part of an app: it ships as a separate tool kit (`kind: "tool"`, a
     tgz with `component.json`), listed as its own entry and named in the app's `requires`.
2. **Copy it** to `packages\` (create the folder if missing; it is git-ignored).
3. **Add or update its entry in `apps.json`**; leave the other entries alone:

   ```json
   {
     "id": "mdq_myapp", "kind": "app", "title": "My App", "description": "One or two sentences for the Store.",
     "author": "7amoody1985", "version": "1.0.0",
     "requires": { "mgu-render": "0.6.11" },
     "uninstallable": true, "mguHmi": ["ID7"], "icon": "mdq_myapp.png"
   }
   ```

   `requires` only if it needs other components (`{"<id>": "<min version>"}`, from any source). `icon`: a PNG
   in `icons\` (140 x 140, at most 128 KiB), optional. A source package the head unit builds itself (a folder
   with `mgu-app.json`, packed) adds `"build": "unit"`. A new version: bump `version` here and in the file name.
4. **Publish**: `powershell -NoProfile -ExecutionPolicy Bypass -File tools\publish.ps1` (needs Python 3).
   It runs `tools/make_catalog.py` (writes `dist\`, checks names and versions) and uploads `dist\` to the
   `catalog` release, deleting assets no longer listed. All of `packages\` must be there for every entry,
   including the ones you did not change: if a package is missing, download it from the release first
   (`gh release download catalog --pattern "<id>@<version>.tgz" --dir packages`).
5. **Verify**: `python -I tools/verify.py` (downloads the published catalog anonymously, as the car does).
   It must end with `all ok`.
6. **Commit and push** `apps.json` (and `icons\`, `README.md`). Add the app to the README's Apps table.
   Commits use the repo's local identity (GitHub noreply address): do not change it.
7. Tell the user: in the Store, **Settings → Check now**, then install the app.

## Do not

- Commit packages, `dist\` or anything holding BMW's SDK.
- Change the `jap_ridetube` entry: it is the RideTube fork (https://github.com/7amoody1985/ridetube,
  checkout `..\ridetube`), whose package comes from that repo's `tools/patch_package.py`.
- Re-create or rename the `catalog` release, or publish it as a draft or prerelease: the Store reads only a
  published release named exactly `catalog`.

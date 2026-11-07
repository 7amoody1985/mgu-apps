#!/usr/bin/env python3
"""Builds this Store source's catalog from apps.json: dist/ gets catalog.json, every package and every icon,
ready to upload as the assets of the GitHub release tagged `catalog` (tools/publish.ps1 does both).

apps.json lists each component the source offers: an app or tool with its package file in packages/
(not committed: release assets only) and, optionally, an icon in icons/ (PNG, at most 128 KiB).
Requirements may name components of other sources (RideTube's service comes from JustAnotherPU/ridetube).

    python3 tools/make_catalog.py [--repo owner/name]

--repo: where the release lives (default: the `origin` remote's GitHub repository).
"""
import argparse, hashlib, json, os, re, shutil, subprocess, sys, tarfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ID_RE = re.compile(r'^[a-z0-9][a-z0-9_-]*$')
VER_RE = re.compile(r'^\d+\.\d+\.\d+$')


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def origin_repo():
    url = subprocess.run(['git', '-C', ROOT, 'remote', 'get-url', 'origin'], capture_output=True, text=True).stdout.strip()
    m = re.search(r'github\.com[:/]([^/]+/[^/]+?)(\.git)?$', url)
    if not m:
        sys.exit('make_catalog.py: no GitHub origin remote; pass --repo owner/name')
    return m.group(1)


def package_version(path):
    """(id, version) from the package's package.json (an app) or component.json (a tool)."""
    with tarfile.open(path, 'r:gz') as t:
        for n in ('package/package.json', 'package.json', 'component.json', './component.json'):
            try:
                j = json.load(t.extractfile(n))
                return j.get('name') or j.get('id'), j.get('version')
            except KeyError:
                continue
    return None, None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--repo')
    a = ap.parse_args()
    base = 'https://github.com/%s/releases/download/catalog/' % (a.repo or origin_repo())
    spec = json.load(open(os.path.join(ROOT, 'apps.json'), encoding='utf-8'))
    out = os.path.join(ROOT, 'dist')
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    comps, seen = [], set()
    for c in spec['components']:
        cid, ver = c['id'], c['version']
        if not ID_RE.match(cid) or cid in seen:
            sys.exit('make_catalog.py: bad or repeated id %r' % cid)
        if not VER_RE.match(ver):
            sys.exit('make_catalog.py: %s: version %r is not x.y.z' % (cid, ver))
        seen.add(cid)
        name = '%s@%s.tgz' % (cid, ver)
        src = os.path.join(ROOT, 'packages', name)
        if not os.path.isfile(src):
            sys.exit('make_catalog.py: packages/%s missing' % name)
        pid, pver = package_version(src)
        if (pid, pver) != (cid, ver) and not c.get('build') == 'unit':
            sys.exit('make_catalog.py: packages/%s says %s@%s' % (name, pid, pver))
        shutil.copy(src, os.path.join(out, name))
        e = {k: c[k] for k in ('id', 'kind', 'title', 'description', 'author', 'version') if k in c}
        e['artifact'] = {'name': name, 'size': os.path.getsize(src), 'sha256': sha256(src), 'url': base + name}
        for k in ('build', 'requires', 'optional', 'uninstallable', 'mguHmi', 'mguProvides'):
            if k in c:
                e[k] = c[k]
        if c.get('icon'):
            ic = os.path.join(ROOT, 'icons', c['icon'])
            if os.path.getsize(ic) > 128 * 1024:
                sys.exit('make_catalog.py: icons/%s is over 128 KiB' % c['icon'])
            shutil.copy(ic, os.path.join(out, c['icon']))
            e['icon'], e['iconSha256'] = c['icon'], sha256(ic)
        comps.append(e)
    with open(os.path.join(out, 'catalog.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump({'schema': 2, 'components': comps}, f, indent=2, ensure_ascii=False)
        f.write('\n')
    for n in sorted(os.listdir(out)):
        print('%10d  %s' % (os.path.getsize(os.path.join(out, n)), n))


if __name__ == '__main__':
    main()

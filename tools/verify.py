#!/usr/bin/env python3
"""Checks the published catalog as the car reads it: anonymous downloads from the `catalog` release, every
artifact and icon against its catalog size and sha256, the package naming its id and version, no BMW SDK in it,
and every component of apps.json listed at its version.

    python3 tools/verify.py [--repo owner/name]
"""
import argparse, hashlib, io, json, os, sys, tarfile, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_catalog import ROOT, origin_repo      # noqa: E402


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'mgu-apps-verify'}), timeout=60) as r:
        return r.read()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--repo')
    a = ap.parse_args()
    base = 'https://github.com/%s/releases/download/catalog/' % (a.repo or origin_repo())
    cat = json.loads(get(base + 'catalog.json'))
    want = {c['id']: c['version'] for c in json.load(open(os.path.join(ROOT, 'apps.json'), encoding='utf-8'))['components']}
    bad = 0
    for e in cat['components']:
        art = e['artifact']
        data = get(art['url'])
        ok = len(data) == art['size'] and hashlib.sha256(data).hexdigest() == art['sha256']
        with tarfile.open(fileobj=io.BytesIO(data), mode='r:gz') as t:
            names = t.getnames()
        sdk = any('node_modules/oap-sdk' in n for n in names)
        msg = []
        if not ok:
            msg.append('size/sha256 differ from the catalog')
        if sdk:
            msg.append('BMW oap-sdk inside: must not be published')
        if want.get(e['id']) != e['version']:
            msg.append('apps.json says %s' % want.get(e['id']))
        if e.get('icon'):
            ic = get(base + e['icon'])
            if e.get('iconSha256') and hashlib.sha256(ic).hexdigest() != e['iconSha256']:
                msg.append('icon sha256 differs')
        bad += bool(msg)
        print('%-4s %s@%s  %d bytes%s' % ('FAIL' if msg else 'ok', e['id'], e['version'], len(data), ': ' + '; '.join(msg) if msg else ''))
    for cid in sorted(set(want) - {e['id'] for e in cat['components']}):
        bad += 1
        print('FAIL %s: in apps.json, not in the published catalog (run tools/publish.ps1)' % cid)
    print('published catalog: ' + ('%d problem(s)' % bad if bad else 'all ok'))
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Fetch the CDLI bulk dumps (catalog + ATF) via the Git-LFS batch API.
No git required. Run from the repo root: python3 scripts/fetch_raw.py
Outputs to data/ (created if missing). ~241 MB total.
"""
import json, urllib.request, os

FILES = {
    "cdli_cat.csv": ("2e3232f75325b61c4d1e788d4d8c074c6230a947aed422110f9f35a6e353d09c", 154768722),
    "cdliatf_unblocked.atf": ("2896ec253767fa07fcaa5424af6fc25d6a047dc30b99c95f99d57ce75384d836", 86897831),
}
LFS_BATCH = "https://github.com/cdli-gh/data.git/info/lfs/objects/batch"

def download_url(oid, size):
    req = urllib.request.Request(
        LFS_BATCH,
        data=json.dumps({"operation": "download", "transfers": ["basic"],
                         "objects": [{"oid": oid, "size": size}]}).encode(),
        headers={"Content-Type": "application/vnd.git-lfs+json",
                 "Accept": "application/vnd.git-lfs+json"})
    d = json.loads(urllib.request.urlopen(req, timeout=30).read())
    return d["objects"][0]["actions"]["download"]["href"]

def main():
    os.makedirs("data", exist_ok=True)
    for fname, (oid, size) in FILES.items():
        dest = os.path.join("data", fname)
        if os.path.exists(dest) and os.path.getsize(dest) == size:
            print(fname, "already present, skipping")
            continue
        print("downloading", fname, flush=True)
        urllib.request.urlretrieve(download_url(oid, size), dest)
        print(fname, "done", os.path.getsize(dest), flush=True)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Weekly liveness check for the Claude Underground map.

Reads stations.json and verifies every station's public URL still resolves and
responds. Writes a Markdown report to stdout. Exits 1 if anything needs a human
look (so the workflow can open an issue) — it never edits the map itself.

Best-effort: some hosts block HEAD or bots, so flagged links are *candidates for
review*, not confirmed-dead. A human (you) decides.
"""
import json, os, sys, concurrent.futures, urllib.request, urllib.error, ssl

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
UA = {"User-Agent": "claude-underground-linkcheck/1.0 (+https://github.com/GabrieleZoppoli/claude-underground)"}
CTX = ssl.create_default_context()


def _get(url, method):
    req = urllib.request.Request(url, method=method, headers=UA)
    with urllib.request.urlopen(req, timeout=20, context=CTX) as r:
        return r.status


def check(url):
    """Return an int HTTP status, or a short error string."""
    try:
        return _get(url, "HEAD")
    except urllib.error.HTTPError as e:
        if e.code in (400, 403, 405, 406, 501):          # HEAD often refused — retry GET
            try:
                return _get(url, "GET")
            except urllib.error.HTTPError as e2:
                return e2.code
            except Exception as e2:
                return type(e2).__name__
        return e.code
    except Exception as e:
        return type(e).__name__


def main():
    data = json.load(open(os.path.join(ROOT, "stations.json")))
    stations = data if isinstance(data, dict) else {}
    items = [(sid, st.get("name", sid), st["url"]) for sid, st in stations.items()
             if isinstance(st, dict) and st.get("url")]

    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:
        futs = {ex.submit(check, url): (sid, name, url) for sid, name, url in items}
        for f in concurrent.futures.as_completed(futs):
            sid, name, url = futs[f]
            results[sid] = (name, url, f.result())

    def ok(status):
        # reachable: a normal success/redirect, OR an auth/rate gate (server is alive,
        # just refusing an anonymous bot). Genuine problems = 404, 5xx, DNS/timeout errors.
        return isinstance(status, int) and (200 <= status < 400 or status in (401, 403, 406, 429))

    flagged = {sid: v for sid, v in results.items() if not ok(v[2])}
    print(f"# Map liveness check — {len(items)} station URLs, {len(flagged)} need a look\n")
    if flagged:
        print("| Station | URL | Status / error |")
        print("|---|---|---|")
        for sid, (name, url, st) in sorted(flagged.items(), key=lambda kv: kv[1][0].lower()):
            print(f"| {name} | <{url}> | `{st}` |")
        print("\n_Some hosts block HEAD requests or bots, so a few of these may be false "
              "positives. Confirm, then update `CATALOGUE.md` / `generate_map.py` for any genuinely "
              "dead station, or close the issue._")
    else:
        print("All station URLs reachable. ✅")
    return 1 if flagged else 0


if __name__ == "__main__":
    sys.exit(main())

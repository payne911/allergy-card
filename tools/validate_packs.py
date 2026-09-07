#!/usr/bin/env python3
"""Validate every docs/lang/*.json.js pack: covers all allergen ids in al+wa,
has the full UI string count, parses as JSON."""
import io, json, os, sys

LANG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "lang")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_languages as G

ids, names, watches = G.parse_english()
want_ui = len(G.UI_STRINGS)
files = sorted(f for f in os.listdir(LANG_DIR) if f.endswith(".json.js"))
bad = []
for fn in files:
    code = fn[:-8]
    txt = io.open(os.path.join(LANG_DIR, fn), encoding="utf-8").read()
    marker = 'ALLERGY_LANG[%s]=' % json.dumps(code)
    i = txt.find(marker)
    try:
        data = json.loads(txt[i + len(marker):].rstrip().rstrip(";"))
    except Exception as e:
        bad.append((code, "unparseable: " + str(e)[:60]))
        continue
    ui, al, wa = data.get("ui") or [], data.get("al") or {}, data.get("wa") or {}
    miss_al = [x for x in ids if x not in al]
    miss_wa = [x for x in ids if x not in wa]
    if len(ui) != want_ui:
        bad.append((code, "ui=%d want %d" % (len(ui), want_ui)))
    if miss_al:
        bad.append((code, "al missing: " + ",".join(miss_al)))
    if miss_wa:
        bad.append((code, "wa missing: " + ",".join(miss_wa)))
print("packs=%d allergens=%d ui=%d bad=%d" % (len(files), len(ids), want_ui, len(bad)))
for c, m in bad[:40]:
    print("  %-8s %s" % (c, m))
sys.exit(1 if bad else 0)

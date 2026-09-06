#!/usr/bin/env python3
"""Append newly added UI strings (from gen_languages.UI_STRINGS) to every
existing language pack under docs/lang/. Packs whose ui array is already at
full length are skipped. Missing tails are machine-translated via the same
gtx batching gen_languages uses. English rebuilds from source.
"""
import io, json, os, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_languages as G

lang_dir = G.LANG_DIR
en_file = os.path.join(lang_dir, "en.json.js")

def read_pack(path, code):
    txt = io.open(path, encoding="utf-8").read()
    marker = 'ALLERGY_LANG[%s]=' % json.dumps(code)
    i = txt.find(marker)
    if i < 0:
        raise RuntimeError("marker not found in %s" % code)
    return json.loads(txt[i + len(marker):].rstrip().rstrip(";"))

def write_pack(path, code, data):
    with io.open(path, "w", encoding="utf-8") as f:
        f.write("window.ALLERGY_LANG=window.ALLERGY_LANG||{};ALLERGY_LANG[%s]="
                % json.dumps(code) + json.dumps(data, ensure_ascii=False) + ";")

files = sorted(f for f in os.listdir(lang_dir) if f.endswith(".json.js"))
patched, skipped, failed = 0, 0, []
for fn in files:
    code = fn[:-len(".json.js")]
    path = os.path.join(lang_dir, fn)
    try:
        data = read_pack(path, code)
        ui = data.get("ui") or []
        missing = len(G.UI_STRINGS) - len(ui)
        if missing <= 0:
            skipped += 1
            continue
        tail_src = G.UI_STRINGS[len(ui):]
        if code == "en":
            tail = tail_src
        else:
            tail = G.gtx_batch(code, tail_src)
        if len(tail) != len(tail_src):
            raise RuntimeError("tail length mismatch")
        data["ui"] = ui + tail
        write_pack(path, code, data)
        patched += 1
        print("ok %-8s (%d/%d)" % (code, patched, len(files)), flush=True)
        time.sleep(0.5)
    except Exception as e:
        failed.append((code, str(e)[:90]))
        print("FAIL %s: %s" % (code, str(e)[:90]), flush=True)
        time.sleep(1.0)
print("patched=%d skipped=%d failed=%d" % (patched, skipped, len(failed)))
if failed:
    for c, e in failed:
        print("  fail %s: %s" % (c, e))
    sys.exit(1)

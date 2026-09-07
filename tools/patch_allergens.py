#!/usr/bin/env python3
"""Append newly added allergens (parsed from index.html) to every existing
language pack under docs/lang/. Packs whose al/wa maps already cover every
allergen id are skipped. Missing entries are machine-translated via the same
gtx batching gen_languages uses. The English pack rebuilds only its al/wa
maps from source (ui strings untouched).
"""
import io, json, os, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_languages as G


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


def main():
    ids, names, watches = G.parse_english()
    if not ids or not names or not watches:
        raise SystemExit("could not parse English allergen data from index.html")
    lang_dir = G.LANG_DIR
    files = sorted(f for f in os.listdir(lang_dir) if f.endswith(".json.js"))
    patched, skipped, failed = 0, 0, []
    for fn in files:
        code = fn[:-len(".json.js")]
        path = os.path.join(lang_dir, fn)
        try:
            data = read_pack(path, code)
            al = data.get("al") or {}
            wa = data.get("wa") or {}
            missing = [i for i in ids if i not in al or i not in wa]
            if not missing:
                skipped += 1
                continue
            name_src = [names[i] for i in missing]
            watch_src = [watches[i] for i in missing]
            if code == "en":
                name_tr, watch_tr = name_src, watch_src
            else:
                out = G.gtx_batch(code, name_src + watch_src)
                name_tr, watch_tr = out[:len(name_src)], out[len(name_src):]
            for i, v in zip(missing, name_tr):
                al[i] = v
            for i, v in zip(missing, watch_tr):
                wa[i] = v
            data["al"], data["wa"] = al, wa
            write_pack(path, code, data)
            patched += 1
            print("ok %-8s (%d/%d) missing=%d" % (code, patched, len(files), len(missing)), flush=True)
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


if __name__ == "__main__":
    main()

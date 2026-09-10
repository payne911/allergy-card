#!/usr/bin/env python3
"""Shard of patch_allergens: translate the missing allergen ids for a subset
of packs. Usage: patch_allergens_shard.py <shard_idx> <shard_count>.

Env REPATCH_WA=1: re-translate the watch strings for the 25 new allergens in
every pack (used after the English watch texts were reworded).

Batching: names (25, short) go as one gtx batch; watches go in chunks of 5 —
small enough to stay fast even when the endpoint is grumpy, and
single-segment so no count-mismatch recursion. ~6 requests per pack.
"""
import io, json, os, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_languages as G
from patch_allergens import read_pack, write_pack

NEW_IDS = ["pork", "chicken", "turkey", "gelatin", "rice", "oats", "barley",
           "rye", "molluscs", "fava_beans", "apple", "banana", "orange",
           "peach", "strawberry", "pineapple", "tomato", "avocado", "coconut",
           "melon", "carrot", "mushroom", "poppy_seeds", "sunflower_seeds",
           "chocolate"]


def main():
    shard_idx, shard_count = int(sys.argv[1]), int(sys.argv[2])
    repatch_wa = os.environ.get("REPATCH_WA") == "1"
    ids, names, watches = G.parse_english()
    assert all(i in ids for i in NEW_IDS), "new ids missing from index.html"
    lang_dir = G.LANG_DIR
    files = sorted(f for f in os.listdir(lang_dir) if f.endswith(".json.js"))
    mine = [fn for k, fn in enumerate(files) if k % shard_count == shard_idx]
    patched, skipped, failed = 0, 0, []
    for fn in mine:
        code = fn[:-len(".json.js")]
        path = os.path.join(lang_dir, fn)
        try:
            data = read_pack(path, code)
            al = data.get("al") or {}
            wa = data.get("wa") or {}
            need_al = [i for i in ids if i not in al]
            need_wa = [i for i in ids if i not in wa]
            if repatch_wa:
                need_wa = list(NEW_IDS)
            if not need_al and not need_wa:
                skipped += 1
                continue
            if code == "en":
                name_tr = [names[i] for i in need_al]
                watch_tr = [watches[i] for i in need_wa]
            else:
                name_tr = G.gtx_batch(code, [names[i] for i in need_al])
                # watches in chunks of 5: small enough to stay fast even
                # when the endpoint is grumpy, single-segment so no
                # count-mismatch recursion.
                wq = [watches[i] for i in need_wa]
                watch_tr = []
                for j in range(0, len(wq), 5):
                    watch_tr.extend(G.gtx_batch(code, wq[j:j + 5]))
            for i, v in zip(need_al, name_tr):
                al[i] = v
            for i, v in zip(need_wa, watch_tr):
                wa[i] = v
            data["al"], data["wa"] = al, wa
            write_pack(path, code, data)
            patched += 1
            print("shard%d ok %-8s patched=%d" % (shard_idx, code, patched), flush=True)
            time.sleep(0.5)
        except Exception as e:
            failed.append((code, str(e)[:90]))
            print("shard%d FAIL %s: %s" % (shard_idx, code, str(e)[:90]), flush=True)
            time.sleep(1.0)
    print("shard%d done: patched=%d skipped=%d failed=%d" % (shard_idx, patched, skipped, len(failed)), flush=True)
    for c, e in failed:
        print("shard%d   fail %s: %s" % (shard_idx, c, e), flush=True)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()

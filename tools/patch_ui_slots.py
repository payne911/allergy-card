#!/usr/bin/env python3
"""Re-translate specific UI slots (7, 8, 9, 33) in every language pack, in
place, after the English source changed:
  7  onboarding step-3 body   (was QR copy)
  8  onboarding step-4 title  (was "Share by link or QR")
  9  onboarding step-4 body   (was QR copy)
  33 custom-emoji field label (was "Pick an emoji", now "Emoji (optional)")
One q-batch HTTP call per pack. Sequential, throttle-aware.
"""
import json, os, re, subprocess, sys, tempfile, time

ROOT = os.path.dirname(os.path.abspath(__file__))
LANG = os.path.join(ROOT, "..", "docs", "lang")

EN = {
    7:  "One tap presents a full-screen card the whole kitchen can read.",
    8:  "Share by link",
    9:  "Your whole profile is encoded in the card's link. Copy it and anyone can open the card on their own phone.",
    33: "Emoji (optional)",
}
MANUAL = {
    "zh": {7: "一键出示全屏卡片，整个后厨都能看懂。",
           8: "通过链接分享",
           9: "您的完整档案都编码在卡片链接中。复制链接，任何人都可以在手机上打开。",
           33: "表情符号 （可选）"},
    "ban": {7: "Akeh neken-neken, kartu layar penuh kaapingiang jagate pawon.",
            8: "Bagiang antuk paica",
            9: "Profil lengkep mudane kasimpan ring paica kartu. Salin paica manut rage, asapunika sami dados ngebuka ring telepon soang-soang.",
            33: "Emodi (opsional)"},
}

UA = ["Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"]
jar = tempfile.NamedTemporaryFile(delete=False).name

def fetch_one(code, text):
    q = subprocess.run(["python3", "-c",
        "import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1]))", text],
        capture_output=True, text=True).stdout.strip()
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl={code}&dt=t&q=" + q
    for attempt in range(5):
        ua = UA[attempt % len(UA)]
        r = subprocess.run(["curl", "-sL", "-b", jar, "-c", jar, "-A", ua, url],
                           capture_output=True, text=True)
        try:
            d = json.loads(r.stdout)
            tr = d[0][0][0]
            if isinstance(tr, str) and tr.strip():
                return tr
        except Exception:
            pass
        time.sleep(2.5 * (attempt + 1))
    return None

def fetch(code):
    out = []
    for t in [EN[7], EN[8], EN[9], EN[33]]:
        tr = fetch_one(code, t)
        if not tr:
            return None
        out.append(tr)
        time.sleep(0.9)
    return out

pack_re = re.compile(r'^(.*?ALLERGY_LANG\["([^"]+)"\]=)(\{.*\})(;\s*)$', re.S)

def patch(path, slots):
    src = open(path, encoding="utf8").read()
    m = pack_re.match(src)
    if not m:
        return "unparsable"
    pre, code, js, post = m.groups()
    d = json.loads(js)
    for idx, val in slots.items():
        d["ui"][idx] = val
    out = pre + json.dumps(d, ensure_ascii=False) + post
    open(path, "w", encoding="utf8").write(out)
    return code

files = sorted(os.listdir(LANG))
if len(sys.argv) > 1 and sys.argv[1] == "rev":
    files.reverse()
total = len(files)
failed = []
for i, f in enumerate(files):
    code = f.split(".")[0]
    p = os.path.join(LANG, f)
    if code == "en":
        patch(p, EN)
    elif code in MANUAL:
        patch(p, MANUAL[code])
    else:
        # already updated (same EN text)?  translate anyway only if stale
        cur = json.loads(pack_re.match(open(p, encoding="utf8").read()).group(3))
        if cur["ui"][7:10] == [EN[7], EN[8], EN[9]] and cur["ui"][33] == EN[33]:
            print(f"skip {code}  ({i+1}/{total})", flush=True)
            continue
        tr = fetch(code)
        if not tr:
            failed.append(code)
            print(f"FAIL {code}", flush=True)
            time.sleep(2)
            continue
        patch(p, {7: tr[0], 8: tr[1], 9: tr[2], 33: tr[3]})
    print(f"ok {code:<8} ({i+1}/{total})", flush=True)
    time.sleep(0.6)

print(f"\npatched={total - len(failed)} failed={len(failed)} {failed or ''}")
sys.exit(0 if not failed else 2)

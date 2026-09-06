#!/usr/bin/env python3
"""Build docs/languages.json + docs/lang/<code>.json.js for every language
machine translation can cover.

English is the source of truth (parsed from the current index.html: allergen
names + watch-out lines). Everything else is machine-translated once, here,
and baked into static files so the app itself stays fully offline.
Re-running is safe: languages already written are skipped.
"""
import io, json, os, re, socket, subprocess, sys, time, urllib.parse, urllib.request

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DOCS = os.path.join(ROOT, "docs")
LANG_DIR = os.path.join(DOCS, "lang")
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AllergyCard/1.0"}

# ---- English UI strings: EXACT text as embedded in index.html -------------
# Each generated pack stores the translations as an ARRAY in this order;
# index.html translates by looking strings up here positionally.
UI_STRINGS = [
 "Tap the allergens you're allergic to. Works offline.",
 "Show any waiter what you can't eat, in their language.",
 "Pick your allergens",
 "Tap everything you're allergic to \u2014 one tap selects, another deselects.",
 "Choose the local language",
 "French in Montr\u00e9al, Japanese in Tokyo, Thai in Bangkok \u2014 the card follows automatically.",
 "Show the red card",
 "One tap gives the waiter a full-screen card with a QR they can scan.",
 "Share by link or QR",
 "Your whole profile is encoded in the card's link. Show the QR and the waiter can carry the card to the kitchen on their own phone.",
 "GET STARTED",
 "Your choices are saved in this browser only. Nothing is sent anywhere.",
 "Waiter's language:",
 "Show QR",
 "Copy link",
 "SHOW THE WAITER CARD",
 "Select at least one allergen",
 "{n} allergens selected",
 "example dishes \u25be",
 "hide dishes \u25b4",
 "Usually in:",
 "Watch out:",
 "ALLERGY ALERT",
 "I am allergic to these foods. Please do not put them in my meal.",
 "Scan to open this card on your phone",
 "Share this allergy card",
 "This QR code and link carry the full profile: allergens and language.",
 "Choose your language",
 "Search languages\u2026",
 "Search allergens\u2026",
 "Add your own +",
 "Add a custom restriction",
 "Name it exactly as you'd say it",
 "Pick an emoji",
 "Save",
 "Add",
 "Edit",
 "Remove",
 "App",
 "{n} allergen selected",
 "Settings",
 "App language",
 "Show allergen emojis",
]

# ---- language list: ISO 639-1 + major 639-2/3 supplements -----------------
LANGS = {
# ISO 639-1
"aa":"Afar","ab":"Abkhazian","af":"Afrikaans","ak":"Akan","am":"Amharic","ar":"Arabic",
"as":"Assamese","ay":"Aymara","az":"Azerbaijani","ba":"Bashkir","be":"Belarusian","bg":"Bulgarian",
"bm":"Bambara","bn":"Bengali","bo":"Tibetan","br":"Breton","bs":"Bosnian","ca":"Catalan",
"ce":"Chechen","ch":"Chamorro","co":"Corsican","cr":"Cree","cs":"Czech","cv":"Chuvash",
"cy":"Welsh","da":"Danish","de":"German","dv":"Divehi","dz":"Dzongkha","ee":"Ewe",
"el":"Greek","en":"English","eo":"Esperanto","es":"Spanish","et":"Estonian","eu":"Basque",
"fa":"Persian","ff":"Fula","fi":"Finnish","fj":"Fijian","fo":"Faroese","fr":"French",
"fy":"Western Frisian","ga":"Irish","gd":"Scottish Gaelic","gl":"Galician","gn":"Guarani","gu":"Gujarati",
"gv":"Manx","ha":"Hausa","haw":"Hawaiian","he":"Hebrew","hi":"Hindi","hr":"Croatian",
"ht":"Haitian Creole","hu":"Hungarian","hy":"Armenian","id":"Indonesian","ig":"Igbo","is":"Icelandic",
"it":"Italian","iu":"Inuktitut","ja":"Japanese","jv":"Javanese","ka":"Georgian","kg":"Kongo",
"ki":"Kikuyu","kk":"Kazakh","kl":"Kalaallisut","km":"Khmer","kn":"Kannada","ko":"Korean",
"kr":"Kanuri","ks":"Kashmiri","ku":"Kurdish","kw":"Cornish","ky":"Kyrgyz","la":"Latin",
"lb":"Luxembourgish","lg":"Ganda","ln":"Lingala","lo":"Lao","lt":"Lithuanian","lu":"Luba-Katanga",
"lv":"Latvian","mg":"Malagasy","mh":"Marshallese","mi":"Maori","mk":"Macedonian","ml":"Malayalam",
"mn":"Mongolian","mr":"Marathi","ms":"Malay","mt":"Maltese","my":"Burmese","ne":"Nepali",
"nl":"Dutch","no":"Norwegian","ny":"Chichewa","oc":"Occitan","om":"Oromo","or":"Odia",
"pa":"Punjabi","pl":"Polish","ps":"Pashto","pt":"Portuguese","qu":"Quechua","rm":"Romansh",
"rn":"Kirundi","ro":"Romanian","ru":"Russian","rw":"Kinyarwanda","sa":"Sanskrit","sd":"Sindhi",
"sg":"Sango","si":"Sinhala","sk":"Slovak","sl":"Slovenian","sm":"Samoan","sn":"Shona",
"so":"Somali","sq":"Albanian","sr":"Serbian","st":"Sesotho","su":"Sundanese","sv":"Swedish",
"sw":"Swahili","ta":"Tamil","te":"Telugu","tg":"Tajik","th":"Thai","ti":"Tigrinya",
"tk":"Turkmen","tl":"Tagalog","tn":"Tswana","to":"Tongan","tr":"Turkish","ts":"Tsonga",
"tt":"Tatar","tw":"Twi","ug":"Uyghur","uk":"Ukrainian","ur":"Urdu","uz":"Uzbek",
"vi":"Vietnamese","wo":"Wolof","xh":"Xhosa","yi":"Yiddish","yo":"Yoruba","za":"Zhuang",
"zh":"Chinese (Simplified)","zu":"Zulu",
# supplements: widely spoken ISO 639-2/3 languages
"yue":"Cantonese","nan":"Min Nan","hak":"Hakka","wuu":"Wu Chinese","gan":"Gan Chinese",
"gsw":"Swiss German","bar":"Bavarian","nap":"Neapolitan","scn":"Sicilian","lij":"Ligurian",
"vec":"Venetian","fur":"Friulian","kab":"Kabyle","arq":"Algerian Arabic","arz":"Egyptian Arabic",
"aeb":"Tunisian Arabic","acm":"Mesopotamian Arabic","apc":"Levantine Arabic","ary":"Moroccan Arabic",
"ckb":"Central Kurdish","kmr":"Northern Kurdish","prs":"Dari","lrc":"Northern Luri","lez":"Lezgian",
"ceb":"Cebuano","war":"Waray","bcl":"Bikol","hil":"Hiligaynon","ilo":"Ilocano","pam":"Kapampangan",
"pag":"Pangasinan","bho":"Bhojpuri","mai":"Maithili","mag":"Magahi","doi":"Dogri","kok":"Konkani",
"sat":"Santali","awa":"Awadhi","bgc":"Haryanvi","hne":"Chhattisgarhi","mni":"Manipuri","gon":"Gondi",
"kha":"Khasi","lus":"Mizo","mwr":"Marwari","raj":"Rajasthani","tly":"Talysh","gag":"Gagauz",
"kaz2":None,"sah":"Yakut","tyv":"Tuvan","krc":"Karachay-Balkar","ady":"Adyghe","kbd":"Kabardian",
"kaa":"Karakalpak","inh":"Ingush","kum":"Kumyk","lbe":"Lak","dar":"Dargwa","udm":"Udmurt",
"chm":"Mari","mhr":"Meadow Mari","bpk":None,"ace":"Acehnese","ban":"Balinese","min":"Minangkabau",
"bjn":"Banjar","mad":"Madurese","tet":"Tetum","smi_x":None,"smn":"Inari Sami","hsb":"Upper Sorbian",
"dsb":"Lower Sorbian","krl":"Karelian","vep":"Veps","vro":"Voro","frr":"North Frisian","nds":"Low German",
"pfl":"Palatine German","frc":"Cajun French","pap":"Papiamento","jam":"Jamaican Patois","tpi":"Tok Pisin",
"quc":"K'iche'","mam":"Mam","cak":"Kaqchikel","nah":"Nahuatl","sqi_x":None,"shy":"Shawiya","shi":"Shilha",
"rif":"Tarifit","zgh":"Standard Moroccan Tamazight","tzm":"Central Atlas Tamazight","ibo_x":None,"ibb":"Ibibio",
"bin":"Edo","fat":"Fante","bci":"Baoule","mos":"Mossi","dyo":"Jola-Fonyi","bas":"Basaa",
"fuv":"Nigerian Fulfulde","kam":"Kamba","mer":"Meru","luo":"Luo","tum":"Tumbuka","swc":"Congo Swahili",
"nus":"Nuer","din":"Dinka","kmb":"Kimbundu","umb":"Umbundu","tig":"Tigre","gez":"Ge'ez","orm_x":None,
}
LANGS = {k:v for k,v in LANGS.items() if v}

def parse_english():
    s = io.open(os.path.join(DOCS, "index.html"), encoding="utf-8").read()
    # legacy inline data: names:{en:"..."} per allergen + watch:"..."
    ids = re.findall(r'\{id:"([a-z_]+)"', s)
    names = dict(re.findall(r'\{id:"([a-z_]+)"[^\n]*?names:\{en:"([^"]+)"', s))
    watch = dict(re.findall(r'\{id:"([a-z_]+)"[^\n]*?watch:"([^"]+)"', s))
    if not names:  # post-refactor build: use the flat bundled map
        m = re.search(r'const EN_AL = (\{.*?\});', s, re.S)
        if m: names = json.loads(m.group(1))
    if not watch:
        m = re.search(r'const EN_WATCH = (\{.*?\});', s, re.S)
        if m: watch = json.loads(m.group(1))
    return ids, names, watch

_JAR = os.path.join(os.environ.get("TMPDIR", "/tmp"), "allergy_gtx_cookies")

def _http_get(url):
    """One GET through the abuse-check redirects. Returns (status, body)."""
    r = subprocess.run(
        ["curl", "-sL", "-c", _JAR, "-b", _JAR, "--max-time", "40",
         "-w", "\n%{http_code}", url],
        capture_output=True, text=True)
    body, _, status = r.stdout.rpartition("\n")
    try:
        code = int(status.strip())
    except ValueError:
        code = 0
    return code, body

def _curl_batch(tl, queries):
    """Newline-joined multi-string queries, one segment per line. Chunked
    (~24 strings) because big payloads and fragment lines sometimes make the
    service merge lines; a count mismatch splits recursively down to single
    strings, which always resolve. 404 means the locale is unsupported;
    429/302 are transient throttling and get retries with growing pauses."""
    if len(queries) > 24:
        mid = len(queries) // 2
        return _curl_batch(tl, queries[:mid]) + _curl_batch(tl, queries[mid:])
    joined = "\n".join(queries)
    url = ("https://translate.googleapis.com/translate_a/single?client=gtx"
           "&sl=en&tl=" + urllib.parse.quote(tl) + "&dt=t&q="
           + urllib.parse.quote(joined))
    code, body, last = 0, "", None
    for attempt in range(6):
        code, body = _http_get(url)
        if code == 200 and body.lstrip().startswith("["):
            break
        if code == 404:
            raise UnsupportedError(tl)
        last = "http %d" % code
        time.sleep(2.5 * (attempt + 1))
    else:
        raise RuntimeError("%s: %s" % (tl, last))
    arr = json.loads(body)
    segs = [seg[0].strip() for seg in arr[0]]
    if len(segs) != len(queries):
        if len(queries) == 1:
            # a single multi-sentence string may come back as several
            # sentence segments: it's all one translation, stitch it
            return [" ".join(segs)]
        mid = len(queries) // 2
        return _curl_batch(tl, queries[:mid]) + _curl_batch(tl, queries[mid:])
    return segs

class UnsupportedError(Exception):
    pass

def gtx_batch(tl, queries):
    try:
        return _curl_batch(tl, queries)
    except UnsupportedError:
        raise RuntimeError("%s: unsupported (404)" % tl)

def native_name(code, fallback):
    """CLDR: how the language calls itself. Fails quietly to English name."""
    base = code.split("-")[0]
    locs = [code] if code == base else [code, base]
    for loc in locs:
        try:
            url = ("https://raw.githubusercontent.com/unicode-org/cldr-json/main/"
                   "cldr-json/cldr-localenames-full/main/%s/languages.json"
                   % urllib.parse.quote(loc))
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=6) as r:
                j = json.loads(r.read().decode("utf-8"))
            langs = j["main"][loc]["localeDisplayNames"]["languages"]
            for key in (code, base):
                if key in langs: return langs[key]
        except Exception:
            pass
    return fallback

def build_one(code, en_name, queries, all_ids):
    out = gtx_batch(code, queries)
    ui = out[:len(UI_STRINGS)]
    ai = len(UI_STRINGS)
    al = {aid: v for aid, v in zip(all_ids, out[ai:ai+len(all_ids)])}
    wa = {aid: v for aid, v in zip(all_ids, out[ai+len(all_ids):])}
    # heuristic for unsupported codes: everything identical to English
    same = sum(1 for q, t in zip(queries, out) if q == t)
    if same == len(queries):
        return None, "unsupported-same-as-english"
    native = native_name(code, en_name)
    return {"name": en_name, "native": native, "ui": ui, "al": al, "wa": wa}, None

def main():
    ids, names, watches = parse_english()
    name_queries = [names[i] for i in ids]
    watch_queries = [watches[i] for i in ids]
    queries = UI_STRINGS + name_queries + watch_queries
    os.makedirs(LANG_DIR, exist_ok=True)
    done, skipped, failed = [], [], []
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    chunk_i, chunk_n = 0, 1
    if "--chunk" in sys.argv:
        ci = sys.argv.index("--chunk"); chunk_i = int(sys.argv[ci + 1]); args = [a for a in args if a != sys.argv[ci + 1] and not a.startswith("--")]
    if "--of" in sys.argv:
        ci = sys.argv.index("--of"); chunk_n = int(sys.argv[ci + 1]); args = [a for a in args if a != sys.argv[ci + 1] and not a.startswith("--")]
    only = set(args)
    keys = sorted(LANGS.items(), key=lambda kv: kv[1])
    if chunk_n > 1:
        keys = [kv for i, kv in enumerate(keys) if i % chunk_n == chunk_i]
    for code, en_name in keys:
        if only and code not in only: continue
        out_file = os.path.join(LANG_DIR, code + ".json.js")
        if code == "en" or os.path.exists(out_file):
            continue
        try:
            data, err = build_one(code, en_name, queries, ids)
            if err:
                skipped.append((code, err)); continue
            with io.open(out_file, "w", encoding="utf-8") as f:
                f.write("window.ALLERGY_LANG=window.ALLERGY_LANG||{};ALLERGY_LANG[%s]="
                        % json.dumps(code) + json.dumps(data, ensure_ascii=False) + ";")
            done.append(code)
            print("ok %-6s (%d)" % (code, len(done)), flush=True)
            time.sleep(0.8)
        except Exception as e:
            failed.append((code, str(e)[:80]))
            print("FAIL %s: %s" % (code, str(e)[:80]), flush=True)
            time.sleep(1.0)
    # english is written from source, not machine output
    en = {"name":"English","native":"English",
          "ui":UI_STRINGS,"al":{i:names[i] for i in ids},"wa":{i:watches[i] for i in ids}}
    with io.open(os.path.join(LANG_DIR,"en.json.js"),"w",encoding="utf-8") as f:
        f.write('window.ALLERGY_LANG=window.ALLERGY_LANG||{};ALLERGY_LANG["en"]='
                + json.dumps(en, ensure_ascii=False) + ";")
    # index file for the search pickers: code, English name, native autonym
    listing = []
    for fn in sorted(os.listdir(LANG_DIR)):
        if not fn.endswith(".json.js"): continue
        code = fn[:-8]
        try:
            with io.open(os.path.join(LANG_DIR, fn), encoding="utf-8") as f:
                txt = f.read()
            j = json.loads(txt[txt.index("]=") + 2 : -1])
            listing.append({"c": code, "n": j["name"], "t": j["native"]})
        except Exception:
            continue
    listing.sort(key=lambda d: d["n"])
    with io.open(os.path.join(DOCS, "languages.json.js"), "w", encoding="utf-8") as f:
        f.write("window.ALLERGY_LANGUAGES=" + json.dumps(listing, ensure_ascii=False) + ";")
    print("languages.json entries:", len(listing))
    print("written:", len(done)+1, "skipped:", len(skipped), "failed:", len(failed))
    if skipped: print("skipped:", [c for c,_ in skipped])
    if failed: print("failed:", [c for c,_ in failed])

if __name__ == "__main__":
    socket.setdefaulttimeout(40)
    main()

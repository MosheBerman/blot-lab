"""Text experiments on Helen Hunter's German transcriptions (Claude version).

Per letter:
  E-skip   letter-level equidistant letter sequences (ELS) for a target lexicon, skips 2..120,
           both directions, against a 40x letter-shuffle null (same letters, same length)
  E-lines  acrostic (first letters of lines), telestich (last letters), first/last words of lines,
           every n-th word (n=2..9, all offsets), first letters of sentences / of every word
  E-anag   anagram pairs within the letter, words that are anagrams/reversals of target words
  E-caps   capital-letter string and cap/lower binary (Bacon 5-bit) decode
  E-caesar Caesar shifts 1..25 of the letters-only text, lexicon hits vs null
  E-nums   every number / date; book-cipher reading of number pairs as (line, word)
  E-names  code-name conventions (Hebrew/Yiddish words dressed as relatives), names not in the family set
  E-editorial  Helen's editorial markers and footnotes (deletions, blots, obscured, scribbled, Hebrew)
Cross-letter:
  E-gs     gezeirah-shava style links: rare word bigrams/trigrams shared by 2+ letters
Writes results/text_<N>.json and results/text_cross.json
"""
import re, json, os, sys, random, glob, itertools, collections

SRC = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/data/hh/transcription'
OUT = sys.argv[2] if len(sys.argv) > 2 else '/home/claude/data/textres'
os.makedirs(OUT, exist_ok=True)
random.seed(1940)

TARGETS = """lager polen opole lublin nisko kielce dachau buchenwald transport gestapo juden hunger
tod tot tote krank flucht hilfe gefahr getto ghetto zug osten deport verschickt arbeit wien krakau
theresienstadt elend angst rettet hilf weg fort schlecht schlimm sterben gestorben ermordet mord
geld visum affidavit schiff amerika palestina palaestina haifa kz konzentration gefangen haft
arrest polizei soldat militaer krieg front russland russen deutsche nazi hitler
josef jakob ewa eva mali maly klara chaja mina kalman joel salomon schlojme taube etel owadie
malka norbert adi bermann willner hirsch rosa regina sabina erna edit lily
mawes moves mowes rachmones zores tsores choleh malach haman amalek pharao chaim""".split()
TARGETS = sorted(set(t for t in TARGETS if len(t) >= 4))

# Holocaust-era Jewish epistolary code names (Hebrew/Yiddish word dressed up as a relative or visitor)
CODE_NAMES = {
    'mawes': 'death (mavet)', 'moves': 'death', 'mowes': 'death', 'malach': 'angel (of death)',
    'rachmones': 'pity/mercy', 'zores': 'troubles', 'tsores': 'troubles', 'choleh': 'sick',
    'raw': 'hunger? (ra\'av)', 'rawe': 'hunger', 'reaw': 'hunger', 'kaddisch': 'mourning prayer',
    'haman': 'persecutor', 'amalek': 'persecutor', 'pharao': 'oppressor', 'mizrajim': 'bondage',
    'gehinom': 'hell', 'schmad': 'persecution', 'golus': 'exile', 'chaim': 'life (could be a real name)',
    'kewer': 'grave', 'chewra': 'burial society', 'schiwe': 'mourning', 'tachrichim': 'shrouds',
    'onkel hunger': 'hunger', 'tante not': 'need', 'herr tod': 'death', 'onkel tod': 'death',
}
FAMILY = set("""josef jossel josel jakob ewa eva chawa chava chawe mali maly malka klara chaja chaje mina kalman
joel salomon schlojme schlojmen taube etel ettel owadie norbert nobi adi bermann berman willner hirsch
rosa rosi regina sabina erna edit lily hönig minne peretz rachel lea ruchel ruchale ruchalen rose chawcze
wiely netsche pepi stern werner etka feld fink abrahams gerhardi max hersch abraham berta josefine""".split())

def fold(s):
    return (s.lower().replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss'))

def parse(path):
    raw = open(path, encoding='utf-8').read()
    raw = raw.split('\n', 1)[1] if raw.startswith('<!--') else raw
    head = open(path).readline()
    t = raw.replace('\\[', '[').replace('\\]', ']').replace('\\!', '!').replace('\\-', '-').replace('\\*', '*')
    lines = [l.rstrip() for l in t.split('\n')]
    foot, body, editorial = [], [], []
    infoot = False
    last_ref = max([i for i, l in enumerate(lines) if '#footnote' in l], default=None)
    for i, l in enumerate(lines):
        s = l.strip()
        if not s: continue
        # footnote block = lines from the first '1 ...' after the last footnote reference in the body
        if last_ref is not None and i > last_ref and re.match(r'^1 \S', s):
            infoot = True
        if infoot:
            foot.append(s); continue
        if s.startswith('Letter ') or s.startswith('Transcribed by') or re.match(r'^\[\d+\.pdf\]$', s) or re.match(r'^\[\d+(-co2)?\.pdf\]$', s):
            continue
        if s.startswith('[') and s.endswith(':]') or re.match(r'^\[[^\]]*(Note|Letter|letter|note|Sender|Recipient|Additional|Text)[^\]]*\]:?$', s):
            editorial.append(s); continue
        body.append(s)
    clean = []
    for s in body:
        s2 = re.sub(r'\[(\d+)\]\(#footnote\d+\)|(?<=\S)(\d+)\(#footnote\d+\)', '', s)
        s2 = re.sub(r'\(#footnote\d+\)', '', s2)
        clean.append(s2)
    return dict(head=head.strip(), body=clean, editorial=editorial, footnotes=foot, raw=t)

def words_of(lines):
    out = []
    for l in lines:
        l2 = re.sub(r'\[(deletion|unclear|Unclear|\?|text loss|Text loss|ink blot|Hebrew/Yiddish)\]', ' ', l)
        l2 = re.sub(r'\[([a-zäöüß\-!]*)\]', r'\1', l2)  # restore expansions like l[iebe] -> liebe
        out.append(re.findall(r"[A-Za-zÄÖÜäöüß]+", l2))
    return out

def letters(ws):
    return ''.join(fold(w) for line in ws for w in line)

def els_count(seq, target, maxskip=120, _cache={}):
    """All ELS hits of target (and its reversal) at skips 2..maxskip; uses residue-class strings."""
    n = len(seq); hits = []
    key = (id(seq), seq[:20], n)
    cls = _cache.get(key)
    if cls is None:
        cls = {d: [seq[r::d] for r in range(d)] for d in range(2, maxskip + 1)}
        _cache.clear(); _cache[key] = cls
    for t, rev in ((target, False), (target[::-1], True)):
        for d in range(2, maxskip + 1):
            if d * (len(t) - 1) >= n: break
            for r, sub in enumerate(cls[d]):
                j = sub.find(t)
                while j != -1:
                    hits.append((r + j * d, d, rev)); j = sub.find(t, j + 1)
    return hits

def lexhits(s, minlen=4):
    s = fold(s)
    return sorted({t for t in TARGETS if len(t) >= minlen and t in s})

def bacon(bits):
    al = 'abcdefghiklmnopqrstuwxyz'  # 24-letter Baconian
    out = ''
    for i in range(0, len(bits) - 4, 5):
        v = int(bits[i:i + 5], 2)
        out += al[v] if v < 24 else '?'
    return out

def analyse(N, path):
    P = parse(path); ws = words_of(P['body'])
    seq = letters(ws)
    flatw = [w for l in ws for w in l]
    R = dict(letter=N, source=P['head'], n_lines=len(P['body']), n_words=len(flatw), n_letters=len(seq))
    # ---- E-editorial
    marks = collections.Counter(re.findall(r'\[(deletion|unclear|Unclear|\?|text loss|Text loss|ink blot|Hebrew/Yiddish)\]', P['raw']))
    R['editorial_markers'] = dict(marks)
    R['footnotes'] = P['footnotes']
    kw = re.compile(r'delet|blot|scribbl|obscur|crossed|cross through|black ink|faint|pencil|stamp|censor|fold|text loss|Hebrew|Yiddish|corner|edge|unclear|correct', re.I)
    R['footnotes_physical'] = [f for f in P['footnotes'] if kw.search(f)]
    R['editorial_notes'] = P['editorial']
    # ---- E-skip (ELS) with null
    targ = [t for t in TARGETS if len(t) >= 4]
    obs = {t: els_count(seq, t) for t in targ}
    null = collections.defaultdict(list)
    for k in range(40):
        sh = list(seq); random.shuffle(sh); sh = ''.join(sh)
        for t in targ:
            null[t].append(len(els_count(sh, t)))
        els_count.__defaults__[1].clear()
    import statistics as st
    els = []
    tot_obs = sum(len(v) for v in obs.values()); tot_null = [sum(null[t][k] for t in targ) for k in range(40)]
    for t in targ:
        o = len(obs[t]); mu = st.mean(null[t]); sd = st.pstdev(null[t]) or 0.5
        if o:
            els.append(dict(target=t, observed=o, null_mean=round(mu, 2), null_sd=round(sd, 2), z=round((o - mu) / sd, 2),
                            examples=[dict(start=i, skip=d, reversed=r) for i, d, r in obs[t][:3]]))
    R['els'] = sorted(els, key=lambda e: -e['z'])
    R['els_total'] = dict(observed=tot_obs, null_mean=round(st.mean(tot_null), 1), null_sd=round(st.pstdev(tot_null), 1))
    # ---- E-lines
    linesw = [l for l in ws if l]
    acro = ''.join(fold(l[0][0]) for l in linesw)
    tele = ''.join(fold(l[-1][-1]) for l in linesw)
    firstw = ' '.join(l[0] for l in linesw); lastw = ' '.join(l[-1] for l in linesw)
    initials = ''.join(fold(w[0]) for w in flatw)
    finals = ''.join(fold(w[-1]) for w in flatw)
    text = ' '.join(' '.join(l) for l in ws)
    sents = re.split(r'[.!?]\s+|,\s*(?=[A-ZÄÖÜ])', ' '.join(P['body']))
    sinit = ''.join(fold(s.strip()[0]) for s in sents if s.strip() and s.strip()[0].isalpha())
    def nth_hits(fw):
        out = {}
        for n in range(2, 10):
            for off in range(n):
                sub = fw[off::n]
                h = [x for x in lexhits(''.join(sub)) if not any(x in fold(w) for w in sub)]  # must span a word boundary
                if h: out[f'{n}/{off}'] = h
        return out
    nth = nth_hits(flatw)
    nn = []
    for k in range(20):
        sw = flatw[:]; random.shuffle(sw); nn.append(sum(len(v) for v in nth_hits(sw).values()))
    R['nth_word_hits_total'] = sum(len(v) for v in nth.values()); R['nth_word_hits_null_mean'] = round(sum(nn) / len(nn), 1)
    R['acrostic'] = acro; R['telestich'] = tele
    R['first_words'] = firstw; R['last_words'] = lastw
    R['word_initials'] = initials; R['sentence_initials'] = sinit
    R['line_hits'] = dict(acrostic=lexhits(acro), telestich=lexhits(tele), acrostic_rev=lexhits(acro[::-1]),
                          word_initials=lexhits(initials), word_finals=lexhits(finals), sentence_initials=lexhits(sinit),
                          first_words=[h for h in lexhits(firstw.replace(' ', '')) if not any(h in fold(w) for w in firstw.split())],
                          last_words=[h for h in lexhits(lastw.replace(' ', '')) if not any(h in fold(w) for w in lastw.split())])
    # null for initials: shuffle words
    nh = []
    for k in range(40):
        sw = flatw[:]; random.shuffle(sw)
        nh.append(len(lexhits(''.join(fold(w[0]) for w in sw))))
    R['word_initials_null_mean'] = round(sum(nh) / len(nh), 2)
    R['nth_word_hits'] = nth
    # ---- E-anag
    uniq = sorted({fold(w) for w in flatw if len(w) >= 4})
    groups = collections.defaultdict(set)
    for w in uniq: groups[''.join(sorted(w))].add(w)
    R['anagram_pairs_in_letter'] = [sorted(g) for g in groups.values() if len(g) > 1]
    tsig = collections.defaultdict(list)
    for t in TARGETS: tsig[''.join(sorted(t))].append(t)
    R['anagrams_of_targets'] = [[w, tsig[''.join(sorted(w))]] for w in uniq if ''.join(sorted(w)) in tsig and w not in TARGETS]
    R['reversals_of_targets'] = [w for w in uniq if w[::-1] in TARGETS]
    R['targets_plain'] = sorted({fold(w) for w in flatw if fold(w) in TARGETS})
    # ---- E-caps
    capsmid = []
    for l in linesw:
        for j, w in enumerate(l):
            if j > 0 and w[0].isupper(): capsmid.append(w)
    capstr = ''.join(fold(w[0]) for w in capsmid)
    bits = ''.join('1' if w[0].isupper() else '0' for w in flatw)
    R['caps_string'] = capstr; R['caps_hits'] = lexhits(capstr)
    R['bacon_from_caps'] = bacon(bits)
    R['bacon_hits'] = lexhits(R['bacon_from_caps'])
    # ---- E-caesar
    cz = {}
    base = 'abcdefghijklmnopqrstuvwxyz'
    for k in range(1, 26):
        tr = str.maketrans(base, base[k:] + base[:k])
        h = lexhits(seq.translate(tr), 5)
        if h: cz[k] = h
    R['caesar_hits'] = cz
    R['plain_lexicon_hits_len5plus'] = lexhits(seq, 5)
    # ---- E-nums
    nums = re.findall(r'\d+(?:[/.–-]\d+)*', ' '.join(P['body'] + P['editorial']))
    R['numbers'] = nums
    flat_ints = [int(x) for x in re.findall(r'\d+', ' '.join(nums))]
    book = []
    for a, b in zip(flat_ints[::2], flat_ints[1::2]):
        if 1 <= a <= len(linesw) and 1 <= b <= len(linesw[a - 1]): book.append(linesw[a - 1][b - 1])
    R['book_cipher_reading'] = book
    gem = {}
    for v in flat_ints:
        if v in (18, 26, 36, 72, 613, 541, 86, 248, 365, 70): gem[v] = True
    R['gematria_notable_numbers'] = sorted(gem)
    # ---- E-names
    low = fold(text)
    R['code_name_hits'] = {k: v for k, v in CODE_NAMES.items() if re.search(r'\b' + re.escape(k) + r'\b', low)}
    caps = sorted({w for l in linesw for j, w in enumerate(l) if w[0].isupper()})
    R['capitalised_words'] = caps
    R['names_not_in_family_set'] = sorted({w for w in caps if fold(w) not in {fold(x) for x in FAMILY}} )
    R['hebrew_yiddish_insertions'] = marks.get('Hebrew/Yiddish', 0)
    R['body'] = P['body']
    return R, flatw

all_words = {}
for path in sorted(glob.glob(os.path.join(SRC, '*.md')), key=lambda p: (len(p), p)):
    N = os.path.basename(path)[:-3]
    if not N.isdigit(): continue
    R, fw = analyse(N, path)
    all_words[N] = [fold(w) for w in fw]
    json.dump(R, open(os.path.join(OUT, f'text_{N}.json'), 'w'), ensure_ascii=False, indent=1)
    top = R['els'][0] if R['els'] else None
    print(N, R['n_words'], 'els', R['els_total'], 'top', (top['target'], top['observed'], top['z']) if top else None,
          'lines', {k: v for k, v in R['line_hits'].items() if v}, 'nth', len(R['nth_word_hits']), 'anag', R['anagram_pairs_in_letter'][:3],
          'codes', R['code_name_hits'], 'caesar', R['caesar_hits'])

# ---- cross-letter gezeirah shava: rare shared n-grams
FORMULA = set('sonst kein neues grüße küße euch vielmals liebe lieber lieben dankend erhalten brief schreiben'.split())
def ngrams(ws, n): return {' '.join(ws[i:i + n]) for i in range(len(ws) - n + 1)}
df = collections.Counter(); where = collections.defaultdict(set)
for N, ws in all_words.items():
    for n in (2, 3):
        for g in ngrams(ws, n):
            if all(t in FORMULA or len(t) <= 3 for t in g.split()): continue
            df[g] += 1; where[g].add(N)
shared = [(g, sorted(where[g], key=int)) for g in df if 2 <= df[g] <= 3 and sum(len(t) for t in g.split()) >= 12]
wdf = collections.Counter(w for ws in all_words.values() for w in set(ws))
rare_words = sorted([(w, sorted([N for N, ws in all_words.items() if w in ws], key=int)) for w in wdf if wdf[w] == 2 and len(w) >= 7])
json.dump(dict(shared_ngrams=sorted(shared), rare_words_in_exactly_two_letters=rare_words), open(os.path.join(OUT, 'text_cross.json'), 'w'), ensure_ascii=False, indent=1)
print('cross shared ngrams', len(shared), 'rare 2-letter words', len(rare_words))

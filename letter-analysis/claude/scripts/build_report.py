"""Build the 'Letter analysis — Claude Version' page (index.html) and report.md from the data/ folder.
Run from letter-analysis/Claude:  python3 scripts/build_report.py
"""
import json, re, glob, html, os

D = 'data'
notes = {}
for f in glob.glob(f'{D}/notes/*.md'):
    notes[os.path.basename(f)[:-3]] = open(f, encoding='utf-8').read().strip().split('\n')
verd = json.load(open(f'{D}/verdicts.json'))
imgs = json.load(open(f'{D}/images.json'))
links = json.load(open(f'{D}/links.json'))
fns = json.load(open(f'{D}/footnotes.json'))
cross = json.load(open(f'{D}/text/text_cross.json'))
text = {}
for f in glob.glob(f'{D}/text/text_*.json'):
    if 'cross' in f: continue
    R = json.load(open(f)); text[R['letter']] = R
sweep = {}
for f in glob.glob(f'{D}/sweep/*.json'):
    s = json.load(open(f)); sweep.setdefault(s['page'].split('-')[0], []).append(s)
LETTERS = [str(n) for n in range(1, 55)]
REDACTED = {'20', '28'}
e = html.escape

STOP = set('und die der das ich ist nicht mit von zu sich auch den dem ein eine euch dich mir mich wir ihr sie er es so wie was wan wenn dass daß habe hat haben sein soll sollen sollt kann kan schon noch nur sehr bitte'.split())
gs = {}
for g, Ls in cross['shared_ngrams']:
    ws = g.split()
    if len([w for w in ws if w not in STOP and len(w) > 3]) < 2: continue
    if any(w in ('author', 'follows', 'letter', 'overleaf', 'visible', 'second', 'same', 'continues') for w in ws): continue
    for l in Ls: gs.setdefault(l, []).append((g, [x for x in Ls if x != l]))

def drive_links(n, md=False):
    out = []
    lab = {'scan': 'Scan PDF', 'transcription_docx': 'Helen transcription (.docx, with footnotes)', 'translation_docx': 'Helen translation (.docx, with footnotes)',
           'transcription_doc': 'Helen transcription (Google Doc)', 'translation_doc': 'Helen translation (Google Doc)'}
    for k in ('scan', 'transcription_docx', 'translation_docx', 'transcription_doc', 'translation_doc'):
        if k in links.get(n, {}):
            t, u = links[n][k]
            if md: out.append(f'[{lab[k]}: {t}]({u}) *(Drive link · private)*')
            else: out.append(f'<a class="drive" href="{e(u)}" target="_blank" rel="noopener">{e(lab[k])}: {e(t)}</a> <span class="dl">Drive link · private</span>')
    return out

def tech_rows(n):
    """Technique iv–viii rows from the text experiments."""
    R = text.get(n)
    if not R:
        no = 'Not run: Helen has no transcription for this item (Yiddish, Hebrew, English or a form). Visual checks only — see findings.'
        return [('iv Word skips', no), ('v Anagrams', no), ('vi Jewish code patterns', 'Visual: Hebrew/Yiddish formulas checked on the image (see findings).'),
                ('vii Ciphers', no), ('viii WWI plain-sight', 'See findings.')]
    t = R['els_total']; z = (t['observed'] - t['null_mean']) / (t['null_sd'] or 1)
    top = [x for x in R['els'] if x['z'] >= 3][:3]
    iv = (f"Skip sequences (every 2nd–120th letter, both directions, {len([1 for _ in range(1)])and 'target list of 125 place, family and danger words'}): "
          f"{t['observed']} hits vs {t['null_mean']} ± {t['null_sd']} in 40 shuffles of the same letters (z = {z:.2f}). "
          + (f"Single-word excesses: {', '.join(x['target'] + ' (' + str(x['observed']) + ' vs ' + str(x['null_mean']) + ')' for x in top)} — expected by chance across 125 words. " if top else '')
          + f"Every n-th word (n = 2–9, all offsets, hits spanning a word boundary): {R.get('nth_word_hits_total', 0)} vs {R.get('nth_word_hits_null_mean', 0)} in shuffled word order.")
    v = 'Anagram pairs inside the letter: ' + (', '.join('/'.join(p) for p in R['anagram_pairs_in_letter']) if R['anagram_pairs_in_letter'] else 'none') + \
        '. Words that rearrange or reverse into a target word: ' + (', '.join(a for a, _ in R['anagrams_of_targets']) + ' ' if R['anagrams_of_targets'] else '') + (', '.join(R['reversals_of_targets']) if R['reversals_of_targets'] else 'none') + '.'
    links_ = gs.get(n, [])
    links_.sort(key=lambda x: -len(x[0]))
    vi = (f"Hebrew/Yiddish insertions marked by Helen: {R['hebrew_yiddish_insertions']}. Code-name lexicon (Mawes, Rachmones, Zores, Haman, Onkel Hunger …): "
          + (', '.join(R['code_name_hits']) if R['code_name_hits'] else 'no hits')
          + '. Gezeirah-shava links (rare phrases shared with only 1–2 other letters): '
          + ('; '.join(f'“{g}” → L{", L".join(o)}' for g, o in links_[:4]) if links_ else 'none') + '.')
    lh = {k: v_ for k, v_ in R['line_hits'].items() if v_}
    vii = ('Acrostic/telestich of lines, first/last words, word and sentence initials: '
           + ('; '.join(f'{k}: {", ".join(v_)}' for k, v_ in lh.items()) if lh else 'nothing')
           + f" (shuffled-word baseline for initials: {R['word_initials_null_mean']}). Capitals string / Bacon 5-bit: "
           + (', '.join(R['caps_hits'] + R['bacon_hits']) or 'nothing')
           + '. Caesar shifts 1–25: ' + (', '.join(f'shift {k}: {", ".join(v_)}' for k, v_ in R['caesar_hits'].items()) if R['caesar_hits'] else 'nothing')
           + '. Number pairs read as (line, word): ' + (' '.join(R['book_cipher_reading']) if R['book_cipher_reading'] else '—') + ' (no sense).')
    return [('iv Word skips', iv), ('v Anagrams', v), ('vi Jewish code patterns', vi), ('vii Ciphers', vii)]

def sweep_log(n):
    S = sorted(sweep.get(n, []), key=lambda s: s['page'])
    if not S: return 'Image sweep: not shown for this item.'
    parts = []
    for s in S:
        c = {}
        for f in s['flags']: c[f['kind']] = c.get(f['kind'], 0) + 1
        parts.append(f"{s['page']}: x-height {s['xheight']:.0f} px, {s['n_words']} word blobs, {s.get('n_cells', 0)} text cells; flags — lighter {c.get('lighter_word', 0)}, other-ink {c.get('different_ink', 0)}, marks {c.get('mark_below_word', 0) + c.get('mark_isolated', 0)}, pinhole specks {s.get('n_bright_total', 0)}")
    return '; '.join(parts) + '.'

def viewer(vid, items):
    if not items: return ''
    first = items[0]
    strip = ''.join(f'<button class="th{" on" if i == 0 else ""}" data-src="{e(src)}" data-cap="{e(cap)}" aria-label="{e(cap)}"><img loading="lazy" src="{e(src)}" alt=""></button>' for i, (k, src, cap) in enumerate(items))
    return (f'<figure class="viewer" id="{vid}"><a class="mainlink" href="{e(first[1])}" target="_blank"><img class="main" loading="lazy" src="{e(first[1])}" alt="{e(first[2])}"></a>'
            f'<figcaption><i>{e(first[2])}</i></figcaption><div class="strip">{strip}</div></figure>')

def fmt_note_line(l):
    l = e(l)
    l = re.sub(r'^(i visible|ii lighter[^:]*|iii marks|Content[^:]*|Plain-sight[^:]*|Euphemism[^:]*|Decoder[^:]*|Deletion test[^:]*|Blot test[^:]*|Block test[^:]*|Hole test[^:]*|Show-through test[^:]*|Dab test|Ink-separation experiment[^:]*|Lead[^:]*|Image check|Translation nuance[^:]*|Text techniques|Coding relevance|Era note|Context[^:]*|Closing lines[^:]*|All text techniques|Red specks[^:]*|ii, iii|ii lighter / different ink)(:)', r'<b>\1</b>\2', l)
    l = re.sub(r'\b(L\d{1,2})\b', lambda m: f'<a href="#{m.group(1)}">{m.group(1)}</a>', l)
    return l

def foot_cites(n):
    out = []
    fx = fns.get(n, {})
    for kind in ('transcription', 'translation'):
        rel = [f for f in fx.get(kind, []) if re.search(r'delet|blot|scribbl|obscur|black ink|cross|stamp|censor|unclear|Hebrew|Yiddish|fold|corner|faint|pencil|correct|deliberate|omit|number', f[1], re.I)]
        for num, t in rel[:6]:
            out.append((f'Helen Hunter, {kind.capitalize()} {n}, fn {num}', t))
    return out

# ------------------------------------------------------------------ page sections
KEY = [
 ('L53', 'Destination replaced by a person: “nach Palästina” struck, “zur Malwin” written above', 'Medium', 'The writer struck two words after “der Jossel möchte so gern …” and wrote “zur Malwin” over them. Fragments of the struck words fit “nach Palästina”; Mali (Malka) was in Palestine. Naming a relative instead of a place is the oldest plain-sight convention.'),
 ('L19', '“Ich übersiedle” = listed for deportation', 'High', 'Written four days before the 15 Feb 1941 Vienna–Opole transport: stop sending, write via Aunt Chawe, don’t worry if I write less. L36 confirms the word.'),
 ('L36', 'Decoder letter: “Josef ist in Polen, Opole bei Lublin”', 'High', 'States Josef’s place openly and explains the earlier “übersiedeln”.'),
 ('L12', 'Location by relative: “in der Nähe deines Bruders Schlojme”', 'High', 'Repeated in L26; with L34, L51, L52 the route to Josef runs through Salomon (Schlojme) Willner in Strzyżów.'),
 ('L48', 'Mail route: Josef → Chaja (Vienna) → New York', 'High', '“I must first write to Chajcze and she forwards it” — explains gaps in Josef’s letters.'),
 ('L51', '“a paar M[ark] zum Leben” — the request is money, via Schlojme', 'Medium–High', 'Resolves Helen’s fn2 toward financial help; money could not go from Vienna to the General Government.'),
 ('L41', '“Ruthi ist nicht zu Hause … der Onkel kann keine Antwort geben”', 'Medium–High', 'Classic way of reporting an arrest or deportation without naming it.'),
 ('L45', '“…und da weiss ich alles leider”', 'Medium', 'Bad news about Mina’s brother-in-law acknowledged but deliberately left unstated.'),
 ('L46', 'Lea Fröhlich: fees (“Spesen”) sent elsewhere, “kann mit dem Transport nicht mehr daran kommen”', 'Medium–High', 'An organised emigration transport, April 1940 — concrete lead.'),
 ('L37', '“Pass abgelaufen, auch Unbede[nklichkeit…]”', 'Medium', 'Best fit for Helen’s untranslated “Unbeden”: the tax-clearance certificate required to emigrate.'),
 ('L44', '“…die sollen schon alle ausgelöst werden”', 'High', 'Owadie, from Palestine, prays the family be ransomed/freed — the word a censor in Vienna would not have passed.'),
 ('L52', '“Ich zahle allein den Zins” = I pay the rent alone', 'High', 'Austrian “Zins” is rent, not interest (translation nuance).'),
]
LEADS = [
 ('Vienna→Opole transport of 15 Feb 1941 (Josef Bermann; Chaja and Maly Willner listed or not)', 'L19, L36, L42', 'DÖW Vienna transport lists; Yad Vashem transport database; Opole Lubelskie ghetto records (Archiwum Państwowe w Lublinie)'),
 ('US consular files: Josef, Chaja, Malka affidavits (“14 Bogen”, “affidavit too weak”, sworn statement of relationship)', 'L8, L10, L34, L37', 'NARA RG 59 visa case files; US consulates Vienna and Jerusalem'),
 ('HIAS: $50 notice (Oct 1940), Lisbon food parcel (Jun 1941), ticket enquiries', 'L18, L40, L45', 'HIAS-HICEM archives (YIVO RG 245); JDC Archives (Lisbon office)'),
 ('Parcels to Josef via “G. Gerhardi, per Adr. Norddeutscher Lloyd, Bremen”', 'L40', 'Norddeutscher Lloyd records, Staatsarchiv Bremen'),
 ('Money transfers: 30 RM Dresdner Bank (Christmas 1940); 40 RM via Hamburg-Amerika Linie Berlin (1941)', 'L43, L45', 'Historisches Archiv der Dresdner Bank (Commerzbank); HAPAG archive (Hamburg)'),
 ('Chaja Willner tax clearance / emigration file', 'L37', 'Finanzamt / Vermögensverkehrsstelle files, Austrian State Archives (AdR); IKG Vienna emigration questionnaires'),
 ('Malka Bermann: Beth Zeiroth, Youth Aliyah grant, Kfar Haroé (Klipper, P.O.B. 22)', 'L10, L32, L34', 'Central Zionist Archives (Youth Aliyah, S75)'),
 ('Lea Fröhlich (?) — emigration transport, spring 1940', 'L46', 'IKG Vienna emigration department records'),
 ('Censor examiner numbers (1517, 1398a, 1820–2622, 1834, 282/23b …)', 'many', 'Auslandsbriefprüfstelle Wien (OKW) — numbers tie letters into mailing batches'),
 ('Rosa/Rosi Hirsch: Vienna → Yugoslavia (left 10 March) → Chicago nurse (1943)', 'L35, L40, L54, L30', 'Passenger and naturalisation records, US'),
]
NEG = [
 'Skip sequences: across all 45 transcribed letters, 2,997 hits vs 2,947.5 expected from shuffled letters (aggregate z = 0.88); no single letter beyond |z| = 2. No hidden word stands out.',
 'Acrostics, telestichs, first/last words, word and sentence initials, capitals, Bacon 5-bit, Caesar 1–25, number-pair book cipher: nothing above the shuffled baseline. Two Caesar hits (L26 “angst”, L30 “krank”) occur at the rate seen in shuffled text.',
 'Code-name lexicon (Hebrew/Yiddish words dressed as relatives — Mawes, Rachmones, Zores, Onkel Hunger, Haman …): zero hits in all transcriptions.',
 'Lighter words: no letter has an isolated faint word; every lighter region is a fold, glare, show-through, a pencil/copying-pencil tone change or a second sitting.',
 'Dots and pinholes under letters: none in a pattern; flagged dots are i-dots, question-mark dots, foxing, stamp ink.',
 'Kiss-count zeros vs the letter’s date: 1 match in 7 dated letters (L7: 19 zeros, 19 Jan) — chance level.',
 'Anagrams: only ordinary German pairs (hier/ihre, euer/eure, meine/einem, deine/diene); L44 “Gerson/sorgen” is coincidence.',
]

TECH = [
 ('i', 'Visible text', 'Re-read every page image against Helen Hunter’s transcription and footnotes; corner numbers, stamps, margins, insertions, corrections.'),
 ('ii', 'Lighter words', 'Ink-darkness map per page (pixel darkness vs local paper, LAB) and a cell test: each 3×1.2 x-height text cell compared with its 4×2 neighbourhood (robust z < −3 with normal ink amount). Ink-hue map for second inks.'),
 ('iii', 'Subtle marks', 'Isolated ink specks outside word blobs classed by position (below a word, isolated) plus pinhole-like bright specks; zoomed crop sheets reviewed by eye. Dense ink masses (scribble-outs, blots) colour-matched against the darkest nearby writing.'),
 ('iv', 'Word skips', 'Equidistant letter sequences, skips 2–120, both directions, 125 target words (places, family names, danger words, Yiddish code words) vs 40 letter shuffles; every n-th word n = 2–9.'),
 ('v', 'Anagrams', 'Same letters, different order: pairs inside each letter; words that rearrange or reverse into a target word.'),
 ('vi', 'Jewish code patterns', 'Gezeirah shava (rare word pairs/triples shared by only 2–3 letters), notarikon/abbreviations (ב"ה, G.s.d., Ka"h), gematria-notable numbers, Hebrew/Yiddish code names for relatives.'),
 ('vii', 'Ciphers', 'Acrostic, telestich, first/last words of lines, word and sentence initials, capitals string and Bacon 5-bit, Caesar 1–25, numbers as (line, word) book cipher.'),
 ('viii', 'WWI Austrian conventions', 'Plain-sight techniques known from k.u.k. field-post censorship and reused 1939–42: a place named through a relative (“near brother X”), illness as excuse for silence, “visiting” for movement, euphemisms (“not at home”), substitution of a destination by a name, messages under stamps. Checked by reading.'),
]

PRIVATE = ('Moshe — the blot-lab repo history shows GitHub Pages deploys, so if Pages is on, anyone with the URL can read this page, '
           'including this note and the Drive link labels (the Drive files themselves still need your sign-in). The two items the index marks [redacted] (scans 20 and 28) are left out on purpose. '
           'If I were spending one more day: (1) have someone hold L53 under a raking lamp and a magnifier — the two struck words are the best candidate here; '
           '(2) order the DÖW transport list for 15 Feb 1941; (3) check whether the HIAS/JDC Lisbon files hold the 1940–41 cases for Chaja Willner and Josef Bermann. '
           'This session cannot push to GitHub, so the report was delivered to you as a zip of letter-analysis/Claude (and committed locally on branch claude/letter-analysis).')

# ------------------------------------------------------------------ HTML
css = r'''
*{box-sizing:border-box}
:root{--bg:#111;--card:#1b1b1b;--line:#333;--fg:#e8e8e8;--muted:#9a9a9a;--accent:#4da3ff;--gold:#c9a227;--warn:#e07a5f}
html{scroll-padding-top:64px}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.55 -apple-system,system-ui,"Segoe UI",sans-serif}
a{color:var(--accent)}
.wrap{display:grid;grid-template-columns:250px minmax(0,1fr);gap:24px;max-width:1240px;margin:0 auto;padding:16px}
header.top{grid-column:1/-1}
h1{font-size:1.25rem;margin:0 0 2px}
.badge{display:inline-block;font-size:.72rem;letter-spacing:.04em;text-transform:uppercase;border:1px solid var(--gold);color:var(--gold);border-radius:4px;padding:1px 6px;margin-left:6px;vertical-align:middle}
p.sub{color:var(--muted);font-size:.85rem;margin:0 0 10px}
.sitenav{font-size:.82rem;margin:0 0 12px;color:var(--muted)}
.sitenav a{text-decoration:none;margin-right:14px}
aside.side{position:sticky;top:12px;align-self:start;max-height:calc(100vh - 24px);overflow:auto;border:1px solid var(--line);border-radius:10px;background:var(--card);padding:10px 8px;font-size:.82rem}
aside.side a{display:block;text-decoration:none;color:#cfd8e3;padding:3px 8px;border-radius:6px}
aside.side a:hover{background:#262626}
aside.side a.cur{background:#1c3d66;color:#fff}
aside.side .grp{color:var(--muted);text-transform:uppercase;font-size:.7rem;letter-spacing:.05em;margin:10px 8px 4px}
aside.side .v{color:var(--gold);font-size:.7rem}
.mobilenav{display:none}
main{min-width:0}
details.sec,details.letter{background:var(--card);border:1px solid var(--line);border-radius:10px;margin:0 0 12px}
details>summary{cursor:pointer;list-style:none;padding:12px 14px;display:flex;gap:10px;align-items:baseline}
details>summary::-webkit-details-marker{display:none}
details>summary::before{content:"\25B6";font-size:.75rem;color:var(--muted);transition:transform .15s;flex:none}
details[open]>summary::before{transform:rotate(90deg)}
summary h2,summary h3{margin:0;font-size:1rem}
summary h3{font-size:.92rem}
summary .meta{color:var(--muted);font-size:.8rem;margin-left:auto;text-align:right}
summary .anchor{color:var(--muted);text-decoration:none;font-size:.8rem}
.body{padding:0 14px 14px}
details.sub{border-top:1px solid var(--line);border-radius:0;background:transparent;margin:0}
.split{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);gap:16px;align-items:start}
.split.noimg{grid-template-columns:1fr}
.viewer{margin:0}
.viewer .main{width:100%;max-height:520px;object-fit:contain;background:#000;border-radius:8px;display:block}
.viewer figcaption{font-size:.78rem;color:var(--muted);margin:6px 0}
.strip{display:flex;gap:6px;overflow-x:auto;padding-bottom:4px}
.strip .th{flex:none;width:64px;height:64px;padding:0;border:2px solid transparent;border-radius:6px;background:#000;cursor:pointer}
.strip .th img{width:100%;height:100%;object-fit:cover;border-radius:4px;display:block}
.strip .th.on{border-color:var(--accent)}
p{margin:.45em 0}
.log li,.find p{font-size:.88rem}
cite,.cite{font-style:italic;color:#c8c8c8;font-size:.84rem}
.cites{border-left:2px solid var(--line);padding-left:10px;margin-top:8px}
.drive{font-size:.84rem}
.dl{font-size:.7rem;color:var(--warn);border:1px solid var(--warn);border-radius:3px;padding:0 4px;margin-left:4px}
table{border-collapse:collapse;width:100%;font-size:.82rem;table-layout:fixed;overflow-wrap:anywhere}
.find,.log,.cites,p,li{overflow-wrap:anywhere}
th,td{border-bottom:1px solid var(--line);padding:6px 6px;text-align:left;vertical-align:top}
th{color:var(--muted);font-weight:600}
.tech td:first-child{width:28%;color:#cfd8e3}
.verdict{border-left:3px solid var(--gold);padding-left:10px}
.conf{display:inline-block;border-radius:4px;padding:0 6px;font-size:.75rem;font-weight:600;background:#2a2a2a;border:1px solid var(--line)}
.private{border:1px dashed var(--warn);background:#221a17;border-radius:10px;padding:10px 14px;margin:0 0 12px;font-size:.86rem}
.private b{color:var(--warn)}
.grid54{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:6px}
.grid54 a{display:block;border:1px solid var(--line);border-radius:6px;padding:6px 8px;text-decoration:none;color:var(--fg);font-size:.78rem;background:#151515}
.grid54 a b{color:var(--accent)}
@media (max-width:900px){
 .wrap{grid-template-columns:1fr;padding:0 16px 16px}
 aside.side{display:none}
 .mobilenav{display:block;position:sticky;top:0;z-index:20;background:var(--bg);padding:8px 0;border-bottom:1px solid var(--line);margin:0 -16px 10px;padding-left:16px;padding-right:16px}
 .mobilenav select{width:100%;font-size:16px;padding:8px;border-radius:8px;background:#1b1b1b;color:var(--fg);border:1px solid var(--line)}
 .split{grid-template-columns:1fr}
 summary .meta{display:none}
 header.top{padding-top:12px}
}
'''

js = r'''
(function(){
  function openFor(id){
    var el=document.getElementById(id); if(!el) return;
    var n=el; while(n){ if(n.tagName==='DETAILS') n.open=true; n=n.parentElement; }
    setTimeout(function(){ el.scrollIntoView({block:'start'}); },30);
  }
  if(location.hash) openFor(decodeURIComponent(location.hash.slice(1)));
  window.addEventListener('hashchange',function(){ openFor(decodeURIComponent(location.hash.slice(1))); });
  document.querySelectorAll('summary a.anchor').forEach(function(a){
    a.addEventListener('click',function(ev){ ev.stopPropagation(); });
  });
  document.querySelectorAll('.viewer').forEach(function(v){
    var main=v.querySelector('.main'), link=v.querySelector('.mainlink'), cap=v.querySelector('figcaption i');
    v.querySelectorAll('.th').forEach(function(b){
      b.addEventListener('click',function(){
        main.src=b.dataset.src; main.alt=b.dataset.cap; link.href=b.dataset.src; cap.textContent=b.dataset.cap;
        v.querySelectorAll('.th').forEach(function(x){x.classList.remove('on')}); b.classList.add('on');
      });
    });
  });
  var sel=document.getElementById('jump');
  if(sel) sel.addEventListener('change',function(){ if(sel.value){ location.hash=sel.value; } });
  var links=[].slice.call(document.querySelectorAll('aside.side a[href^="#"]'));
  var targets=links.map(function(a){return document.getElementById(a.getAttribute('href').slice(1));});
  function spy(){
    var y=window.scrollY+90, cur=null;
    targets.forEach(function(t,i){ if(t && t.offsetParent!==null && t.getBoundingClientRect().top+window.scrollY<=y) cur=i; });
    links.forEach(function(a,i){ a.classList.toggle('cur',i===cur); });
  }
  window.addEventListener('scroll',spy,{passive:true}); spy();
  document.getElementById('expandall').addEventListener('click',function(){ document.querySelectorAll('details.letter').forEach(function(d){d.open=true;}); });
  document.getElementById('collapseall').addEventListener('click',function(){ document.querySelectorAll('details.letter').forEach(function(d){d.open=false;}); });
})();
'''

def letter_title(n):
    l = notes[n][0]
    return re.sub(r'^L\d+\s*\|\s*', '', l)

def html_letter(n):
    v = verd[n]; title = letter_title(n)
    items = imgs.get(n, [])
    crops = [x for x in items if x[0] == 'crop']
    base = [x for x in items if x[0] != 'crop']
    body_lines = notes[n][1:]
    exp_manual = [l for l in body_lines if re.match(r'^(Deletion test|Blot test|Block test|Hole test|Show-through test|Dab test|Ink-separation experiment|Closing lines|Image check)', l)]
    find_lines = [l for l in body_lines if l not in exp_manual]
    tr = tech_rows(n)
    dl = drive_links(n)
    cites = foot_cites(n)
    # experiment
    exp = ['<ul class="log">',
           f'<li><b>Sources read:</b> scan pages; Helen Hunter’s transcription and translation with footnotes (where they exist); LastLetters index sheet.</li>',
           f'<li><b>i–iii image sweep (automated):</b> {e(sweep_log(n))}</li>',
           '<li><b>ii ink maps:</b> darkness heat map and hue map for every page (film strip).</li>',
           '<li><b>iii marks review:</b> every flagged speck viewed in a zoomed crop sheet.</li>',
           f'<li><b>iv–vii text tests (automated):</b> {"run on Helen’s German transcription" if n in text else "not possible — no transcription"}.</li>',
           '<li><b>viii conventions:</b> read for relative-for-place, illness excuse, visiting, euphemism, substitution, examiner numbers.</li>']
    for l in exp_manual:
        exp.append(f'<li>{fmt_note_line(l)}</li>')
    exp.append('</ul>')
    exp_html = ''.join(exp)
    fview = viewer(f'v{n}e', base) if n not in REDACTED else ''
    cview = viewer(f'v{n}f', crops)
    techrows = ''.join(f'<tr><td>{e(a)}</td><td>{e(b)}</td></tr>' for a, b in tr)
    find_html = ''.join(f'<p>{fmt_note_line(l)}</p>' for l in find_lines)
    cite_html = ''
    if cites:
        cite_html = '<div class="cites">' + ''.join(f'<p><cite>{e(a)}:</cite> <span class="cite">“{e(t)}”</span></p>' for a, t in cites) + '</div>'
    drive_html = '<div class="cites">' + '<br>'.join(dl) + '</div>' if dl else ''
    return f'''
<details class="letter" id="L{n}">
<summary><h2>Letter {n}</h2><span class="sumt">{e(title[:90])}</span><a class="anchor" href="#L{n}" title="Link to this letter">#</a><span class="meta">{e(v[0])}</span></summary>
<div class="body">
 <details class="sub" id="L{n}-experiment" open><summary><h3>Experiment</h3><a class="anchor" href="#L{n}-experiment">#</a></summary>
  <div class="body"><div class="split{'' if fview else ' noimg'}">{fview}<div>{exp_html}{drive_html}</div></div></div></details>
 <details class="sub" id="L{n}-findings" open><summary><h3>Findings</h3><a class="anchor" href="#L{n}-findings">#</a></summary>
  <div class="body"><div class="split{'' if cview else ' noimg'}">{cview}<div class="find">{find_html}{cite_html}</div></div>
  <table class="tech" style="margin-top:10px"><tr><th>Technique</th><th>Result for this letter</th></tr>{techrows}</table></div></details>
 <details class="sub" id="L{n}-confidence" open><summary><h3>Confidence</h3><a class="anchor" href="#L{n}-confidence">#</a></summary>
  <div class="body verdict"><p><b>{e(v[0])}</b> <span class="conf">{e(v[1])}</span></p><p>{e(v[2])}</p></div></details>
</div></details>'''

side = ['<div class="grp">Report</div>', '<a href="#summary">Summary</a>', '<a href="#leads">Primary-source leads</a>', '<a href="#negatives">Negative results</a>',
        '<a href="#cross">Cross-letter tests</a>', '<a href="#method">Method</a>', '<a href="#all">All letters</a>', '<div class="grp">Letters</div>']
opts = ['<option value="">Jump to…</option>', '<option value="summary">Summary</option>', '<option value="leads">Primary-source leads</option>',
        '<option value="negatives">Negative results</option>', '<option value="cross">Cross-letter tests</option>', '<option value="method">Method</option>']
for n in LETTERS:
    side.append(f'<a href="#L{n}">L{n} <span class="v">{e(verd[n][1])}</span></a>')
    opts.append(f'<option value="L{n}">Letter {n} — {e(verd[n][0][:48])}</option>')

key_rows = ''.join(f'<tr><td><a href="#{k}">{k}</a></td><td>{e(t)}</td><td><span class="conf">{e(c)}</span></td><td>{e(d)}</td></tr>' for k, t, c, d in KEY)
lead_rows = ''.join(f'<tr><td>{e(a)}</td><td>{re.sub(r"(L\d+)", lambda m: f"<a href=#{m.group(1)}>{m.group(1)}</a>", e(b))}</td><td><i>{e(c)}</i></td></tr>' for a, b, c in LEADS)
neg = ''.join(f'<li>{e(x)}</li>' for x in NEG)
tech = ''.join(f'<tr><td>{a}. {e(b)}</td><td>{e(c)}</td></tr>' for a, b, c in TECH)
grid = ''.join(f'<a href="#L{n}"><b>L{n}</b> · {e(verd[n][0][:60])}</a>' for n in LETTERS)

cross_html = '''
<p><b>Gezeirah shava (shared rare phrases).</b> Word pairs/triples occurring in only 2–3 letters were listed (509 raw; formula greetings removed). The meaningful links are semantic, not lexical:
<i>“in der Nähe von dein Bruder Schlojme”</i> (<a href="#L12">L12</a>, <a href="#L26">L26</a>) — place by relative;
<i>“übersiedeln”</i> (<a href="#L19">L19</a>, <a href="#L36">L36</a>) — deportation listing;
<i>“besuchen”</i> for Josef’s movements (<a href="#L11">L11</a>, <a href="#L18">L18</a>, <a href="#L43">L43</a>, <a href="#L52">L52</a>);
<i>“zur Mali fahren”</i> for Palestine (<a href="#L25">L25</a>, <a href="#L33">L33</a>, <a href="#L39">L39</a>, <a href="#L46">L46</a>, <a href="#L53">L53</a>);
<i>“Erholung”</i> (<a href="#L35">L35</a> ambiguous; <a href="#L42">L42</a> literal). A lexical link that is false: “nicht aufgeben” (<a href="#L10">L10</a> give up; <a href="#L12">L12</a> post a letter).</p>
<p><b>Examiner numbers.</b> Identical numbers bind letters into mailing batches: 1820–2622 on <a href="#L25">L25</a> and <a href="#L27">L27</a>; 1398a on <a href="#L14">L14</a> and <a href="#L39">L39</a>; 1517 on <a href="#L17">L17</a> and <a href="#L23">L23</a>; 1834 on <a href="#L48">L48</a> (and probably <a href="#L52">L52</a>). These are censorship handling numbers, not messages.</p>
<p><b>Mail route reconstructed from the letters themselves:</b> Josef → Chaja in Vienna (<a href="#L48">L48</a>) → New York; money and clothes to Josef → Salomon/Schlojme in Strzyżów (<a href="#L34">L34</a>, <a href="#L51">L51</a>, <a href="#L52">L52</a>); parcels → G. Gerhardi c/o Norddeutscher Lloyd, Bremen (<a href="#L40">L40</a>); tickets and food → HIAS Lisbon (<a href="#L18">L18</a>, <a href="#L23">L23</a>, <a href="#L45">L45</a>).</p>
<p><b>Shared sheet.</b> <a href="#L53">L53</a> and <a href="#L54">L54</a> are two sides of one sheet; the L53 deletion shows through on L54 and was used as an independent second look.</p>
'''

page = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Letter Analysis (Claude)</title><meta name="robots" content="noindex,nofollow">
<style>{css}</style></head>
<body>
<div class="wrap">
<header class="top">
 <h1>Letter analysis <span class="badge">Claude Version</span></h1>
 <p class="sub">Every letter, page by page, against eight techniques: visible text, lighter words, subtle marks, word skips, anagrams, Jewish code patterns, ciphers and WWI-era plain-sight conventions. Built 16 Oct 2026 from the scans, Helen Hunter’s transcriptions, translations and footnotes.</p>
 <nav class="sitenav"><a href="../../index.html">Lab home</a><a href="../../lab.html">Lab</a><a href="../../experiments.html">Experiments</a><a href="../../scrubber.html">Scrubber</a><a href="../../ink-layer-report.html">Ink-layer report</a><a href="../../forensics-report.html">Forensics report</a><a href="index.html">Letter analysis (Claude)</a><a href="report.md">Markdown version</a></nav>
</header>
<aside class="side">{''.join(side)}</aside>
<main>
<div class="mobilenav"><select id="jump" aria-label="Jump to section">{''.join(opts)}</select></div>
<div class="private"><b>Private annotation.</b> {e(PRIVATE)}</div>

<details class="sec" id="summary" open><summary><h2>Summary</h2><a class="anchor" href="#summary">#</a></summary><div class="body">
<p>54 scans (110 page images) were examined; 45 have Helen Hunter transcriptions and were run through every text test. No mechanical cipher was found: skip sequences, acrostics, capitals, Caesar and anagram tests all sit at chance. No faint or dotted hidden writing was found. What the letters do contain is <b>plain-sight writing</b>: places named through relatives, deportation called “moving”, detention called “not at home”, a destination replaced by a name. Those are below, ranked.</p>
<table><tr><th>Letter</th><th>Finding</th><th>Confidence</th><th>Why</th></tr>{key_rows}</table>
<p style="margin-top:10px"><button id="expandall">Expand all letters</button> <button id="collapseall">Collapse all letters</button></p>
</div></details>

<details class="sec" id="leads" open><summary><h2>Primary-source leads</h2><a class="anchor" href="#leads">#</a></summary><div class="body">
<p>Facts in the letters that should exist in an archive. Archive names are suggestions to check, not confirmed holdings.</p>
<table><tr><th>Fact</th><th>Letters</th><th>Where to look</th></tr>{lead_rows}</table></div></details>

<details class="sec" id="negatives"><summary><h2>Negative results</h2><a class="anchor" href="#negatives">#</a></summary><div class="body"><ul>{neg}</ul></div></details>

<details class="sec" id="cross"><summary><h2>Cross-letter tests</h2><a class="anchor" href="#cross">#</a></summary><div class="body">{cross_html}</div></details>

<details class="sec" id="method"><summary><h2>Method</h2><a class="anchor" href="#method">#</a></summary><div class="body">
<table class="tech"><tr><th>Technique</th><th>What was run</th></tr>{tech}</table>
<p class="cite">Scripts in <code>letter-analysis/Claude/scripts/</code>: <code>page_sweep.py</code>, <code>ink_maps.py</code>, <code>deletion_ink.py</code>, <code>block_views.py</code>, <code>text_experiments.py</code>, <code>build_report.py</code>. Raw results in <code>data/</code>. Only the scans, Helen’s documents and the LastLetters index were used; no earlier lab conclusions were consulted for the findings.</p>
</div></details>

<details class="sec" id="all" open><summary><h2>All letters</h2><a class="anchor" href="#all">#</a></summary><div class="body"><div class="grid54">{grid}</div></div></details>

{''.join(html_letter(n) for n in LETTERS)}
</main></div>
<script>{js}</script>
</body></html>'''
open('index.html', 'w', encoding='utf-8').write(page)

# ------------------------------------------------------------------ Markdown
md = ['# Letter analysis — Claude Version', '',
      '*Built 16 Oct 2026 from the scans, Helen Hunter’s transcriptions, translations and footnotes. HTML version: [index.html](index.html).*', '',
      '> **Private annotation.** ' + PRIVATE, '', '## Summary', '',
      '54 scans (110 page images) examined; 45 transcribed letters run through every text test. No mechanical cipher and no faint or dotted hidden writing found. The letters do use plain-sight writing; ranked findings:', '',
      '| Letter | Finding | Confidence | Why |', '|---|---|---|---|']
md += [f'| [{k}](#{k.lower()}) | {t} | {c} | {d} |' for k, t, c, d in KEY]
md += ['', '## Primary-source leads', '', '| Fact | Letters | Where to look |', '|---|---|---|']
md += [f'| {a} | {b} | *{c}* |' for a, b, c in LEADS]
md += ['', '## Negative results', ''] + [f'- {x}' for x in NEG]
md += ['', '## Cross-letter tests', '', re.sub(r'<[^>]+>', '', cross_html).strip(), '', '## Method', '', '| Technique | What was run |', '|---|---|']
md += [f'| {a}. {b} | {c} |' for a, b, c in TECH]
for n in LETTERS:
    v = verd[n]
    md += ['', f'## L{n}', '', f'**{letter_title(n)}**', '', '### Experiment', '',
           '- Sources read: scan pages; Helen Hunter’s transcription and translation with footnotes (where they exist); LastLetters index sheet.',
           f'- Image sweep: {sweep_log(n)}',
           f'- Text tests: {"run on Helen’s German transcription" if n in text else "not possible — no transcription"}.']
    for l in notes[n][1:]:
        if re.match(r'^(Deletion test|Blot test|Block test|Hole test|Show-through test|Dab test|Ink-separation experiment|Closing lines|Image check)', l): md.append(f'- {l}')
    md += drive_links(n, md=True) and ['', 'Originals: ' + ' · '.join(drive_links(n, md=True))] or []
    ims = [x for x in imgs.get(n, [])]
    if ims and n not in REDACTED:
        md += ['', ' '.join(f'[![{c}]({s})]({s})' for k, s, c in ims[:1]), '', 'Images: ' + ' · '.join(f'[{c[:40]}]({s})' for k, s, c in ims)]
    md += ['', '### Findings', '']
    for l in notes[n][1:]:
        if not re.match(r'^(Deletion test|Blot test|Block test|Hole test|Show-through test|Dab test|Ink-separation experiment|Closing lines|Image check)', l): md.append(f'- {l}')
    for a, t in foot_cites(n): md.append(f'- *{a}:* “{t}”')
    md += ['', '| Technique | Result |', '|---|---|'] + [f'| {a} | {b} |' for a, b in tech_rows(n)]
    md += ['', '### Confidence', '', f'**{v[0]}** — {v[1]}. {v[2]}']
open('report.md', 'w', encoding='utf-8').write('\n'.join(md) + '\n')
print('ok', len(page), len('\n'.join(md)))

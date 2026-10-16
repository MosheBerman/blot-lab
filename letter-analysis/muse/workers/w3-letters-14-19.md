# Coded-language forensic report — Letters 14, 15, 16, 17, 18, 19
Worker: w3 | Date: 2026-10-16 | Corpus: ~/workspace/goals/the-coded-letters/hidden_files/

Scope: letters 14–19 only. Sources used: transcription-N.txt (14, 17, 18, 19),
translation-N.docx body + footnotes (14, 17, 18, 19), scans N.pdf rendered at 170 dpi
(all pages viewed), 300 dpi spot crops, CSV index (LastLettersCSV.csv). Letters 15 and 16
have no transcript/translation: image skim + manual Yiddish reading + tesseract attempt
(tesseract has no yid/heb language data installed; `-l deu` run produced garbage —
documented below). No existing analysis files were opened.

Identity note used below: there are THREE distinct Maly/Mali individuals in these letters —
(a) Mali/Maly, daughter of the New York recipients Jakob Willner & wife (letters 17, 18, 19:
"die liebe Mali", "Euere liebe Mali", ill in 18/19); (b) "Maly B." = Maly Bermann, Ewa's
daughter in New York (letter 18: "von die l. Ewa und Maly B. den Brief"); (c) "meine
Maly"/"Maltschi" = Maly Willner, Chaja's own daughter in Vienna (letters 17, 18, 19;
signs letter 19 as "Chaja und Maly Willner"). Do not conflate.

---

## Letter 14 — 28 Aug 1940, Klara → Ewa Bermann, 1 page (scan 14.pdf, 1 p.)

### i) VISIBLE TEXT
- Method: read transcript against scan; read translation + HH footnotes.
- Observations:
  - "habe schon zu Untersuchung man bekommt leider jetzt von der Isr. K. keine
    Schiffskarten überhaupt gar nichts." ("I have already [been summoned] for the
    examination; unfortunately one gets no ship tickets at all from the IKG now.")
    HH footnote 2: grammar is garbled but the meaning is that her number had come up
    for the appointment; the "examination" is an emigration-procedure step.
  - "zu Etlen habe geschreiben und keine Antwort sie hat amir nie geantwortet."
    ("I wrote to Etlen and got no answer; she never answered me.") "Etlen" sits at the
    crumpled right edge; HH footnote 4 notes a possibly obscured letter after the 'n'.
    Crop confirms "Etlen" with the edge crumple immediately after — most plausibly
    "Etel" (Ettel = Taube Ettel Biller, née Bermann, the writer's sister), but the 'n'
    is clearly written, so [uncertain].
  - "zu Schlome habe geschrieben [deletion] er gibt mir immer auf 2 Karten Antwort"
    ("I wrote to Schlome [deletion]; he always answers one of every two cards.")
  - "der Josef ferdient es geht im ganz gut" ("Josef is earning; he is doing quite
    well.") — the "X is earning" work-claim formula.
  - Penciled "1398a" in the upper left corner, lighter script than the body.
- Finding: emigration-logistics facts (IKG ship-ticket stoppage, Aug 1940; the
  "Untersuchung" summons) are primary-source-rich (IKG emigration files). No
  euphemisms for deportation (too early); no jargon code detected. The 1-in-2 reply
  ratio from Schlome and the unanswered Etlen are plain correspondence facts.
- Confidence: medium (for "no code"); low on the "Etlen"="Etel" identification.

### ii) LIGHTER WORDS
- Method: compared ink density across the page.
- Observations: "1398a" (p.1, upper left) and the date line "Wien den 28/8 40" are in
  noticeably lighter, pencil-like script vs. the dark-ink body. The "40" is followed
  by a dark ink blob (looks like a heavy period).
- Finding: "1398a" is almost certainly a later archival filing number, not the
  author's hand. The lighter date line may be the same pencil or a different pen;
  not readable as emphasis. Nothing found suggesting deliberate lightening of
  message words.
- Confidence: medium.

### iii) SUBTLE MARKINGS
- Method: full-page visual scan at 170 dpi + crop of top region.
- Observations: dark ink blots on/near: "habe" (line 4, "habe schon"), "leider"
  (line 5), left margin before "habe geschrieben" (line 8), and the start of "grüßen"
  ("auch meine Maly lässt Alle schön grüßen"); a blot on the "L" of "Liebe
  Schwester!"; a small superscript mark above "der" in the PS ("der Josef ferdient").
- Finding: blots look like pen blobs from a scratchy nib, not placed marks. The
  superscript mark above "der" is [uncertain] — could be a stray stroke. Nothing
  systematic.
- Confidence: low.

### iv) WORD SKIPS / LAYOUT
- Method: traced reading order against the transcript.
- Observations: the page is written in TWO COLUMNS (left column first, then right
  column); the transcript reconstructs the reading order across columns. One
  [deletion] is marked by the transcriber at "zu Schlome habe geschrieben".
- Finding: two-column layout is a paper-economy habit, not a code layout. The
  deletion's content is unrecoverable from the scan (blotted). Nothing further.
- Confidence: medium.

### v) ANAGRAM-LIKE / TRANSPOSED WORDS
- Method: scripted check — all word pairs (len>=4) that are exact letter-permutations.
- Observations: only hit: "geschreiben" vs "geschrieben" ("zu Etlen habe geschreiben"
  vs "zu Schlome habe geschrieben") — true anagrams (transposed 'e'/'i'), but the
  first is simply Klara's misspelling of the correct "geschrieben". No name/place
  transpositions.
- Finding: natural spelling error, not code. Nothing found.
- Confidence: high.

### vi) JEWISH RELIGIOUS CODE PATTERNS
- Method: checked for Hebrew phrases, holiday refs, liturgical quotes; read HH footnotes.
- Observations: none present in this letter.
- Finding: nothing found. Confidence: high.

### vii) CRYPTOGRAPHY / KNOWN TECHNIQUES
- Method: listed sentence-initials ([p]Dw]z]Psd — brackets are transcript markup,
  no pattern) and word-initials (no pattern); checked numbers/dates; looked for
  book-cipher references and deliberate misspellings.
- Observations: number "1398a" = filing number (see ii). Date reads clearly "28/8"
  on the scan — resolves the CSV's "June or Aug 28, 1940" note toward 28 August
  (the transcriber's [?] is overcautious; the "8" is unambiguous in the crop).
  No "as I wrote on page X" references. Misspellings ("geschreiben", "ferdienst",
  "amir") are consistent dialectal writing, not patterned.
- Finding: nothing found. Confidence: medium-high.

### viii) HISTORICAL COMPARISON
- "Untersuchung" + IKG ship tickets + "Josef is earning" are straightforward
  emigration-era plain text, Aug 1940 — before deportations, so the "emigrated"=
  deported euphemism family does not apply. The unanswered letters and 1:2 reply
  ratio are ordinary wartime-mail facts, not null-cipher signals.

**Per-letter verdict:** No coded message detected. A plain emigration-logistics
letter; its facts (IKG ship-ticket stoppage, Untersuchung summons, Josef employed)
are primary-source leads. Minor anomalies: pencil filing number "1398a", the
"Etlen"[?] name at the crumpled edge, one blotted deletion.

---

## Letter 17 — 18 July 1940, Chaja Willner → Jakob Willner (cc Ewa), 2 pages (postcard)

### i) VISIBLE TEXT
- Method: transcript + translation + HH footnotes, checked against both scan pages.
- Observations:
  - "der Salomon hat mir die Adresse geschickt von Dir l. Bruder, er hat ein Brief
    von Dir erhalten" ("Salomon sent me your address, dear brother; he received a
    letter from you.") — addresses relayed through a third party; describes another
    person's message.
  - "die l. Ewa hat afor die Ostern geschrieben das zu Ostern nimt sie die Kinder
    zu sich" ("dear Ewa wrote before Easter that at Easter she will take the
    children to her.") — a specific dated plan (Easter = 24 Mar 1940), reported
    secondhand, stated as still unfulfilled ("und wir warten noch auf den Brief").
    This is the letter's most content-bearing sentence and the locus of the
    heavy-ink words (see iii).
  - "ich hab den Josef fon dem Brief nicht gesagt" ("I didn't tell Josef about that
    letter.") — deliberate withholding of information from Josef; motive unstated
    (spare him worry? or operational?).
  - "der Josef ferdient, er ist in [?] noch dort" ("Josef is earning; he is still in
    the same place.") — "in [?] noch dort": the location word is illegible in the
    transcript; on the scan it is overwritten by the postmark area [uncertain].
  - "ich weiß nicht wan ich daran kom nach U.S.A." ("I don't know when it will be
    my turn to come to the USA.")
  - "der Schwager kan leider alein nicht schreiben weil er Finger weh hat"
    ("unfortunately my brother-in-law can't write himself because his fingers hurt.")
  - Three lines blacked out in heavy black ink immediately after "soll die Ewa und
    Kinder mir schreiben" (HH footnote 2: "Several words blotted out with black ink
    over three lines").
- Finding: the Easter plan + the withheld letter + the blacked-out passage form the
  densest anomaly cluster in this batch. Read at face value it is still coherent
  (a failed family-reunion plan, sparing Josef bad news, a second thought blacked
  out). No decodable second message; but this is the strongest candidate for
  plain-sight significance.
- Confidence: medium that there is "more here than a routine card"; low that it is
  a formal code.

### ii) LIGHTER WORDS
- Method: compared ink density; examined address side.
- Observations: penciled "1268 [?]–1345" along the lower edge (faint; first digit
  faint — "1268" per transcript, confirmed as faint pencil in crop); stamped "1517"
  in a box below "Absender:" (light blue-grey office stamp). No lighter *message*
  words.
- Finding: both are filing/office numbers, not authorial. Nothing found.
- Confidence: medium.

### iii) SUBTLE MARKINGS
- Method: 170 dpi full-page + zoom crop of lines 8–11 (message side).
- Observations: a cluster of words in markedly HEAVIER ink than the surrounding
  text, all inside the Easter sentence: "afor" (very heavy), "nimt" (heavy), "zu"
  (in "die Kinder zu", heavy), "das" (in "das zu Ostern", heavier). Also "zum" (in
  "weder zum Josef", heavier). Elsewhere on the card the ink is normal. Separately:
  a blot on the "D" of "Dir" ("Brief von Dir erhalten"); a dark blot over
  "Schwägerin" in the salutation; small ink speckles below "Brief nicht gesagt".
- Finding: the heavy-ink cluster is visually real (confirmed in crop) and confined
  to one sentence — consistent with either deliberate emphasis/marking or a
  freshly-dipped pen pressed harder on verbs. The marked words read
  "afor… nimt… zu… (sich)… zum…" — no clear hidden message. Report as observed,
  unresolved. The blots look like nib blobs.
- Confidence: medium that the heavy ink is real; low that it encodes anything.

### iv) WORD SKIPS / LAYOUT
- Method: traced visual line order.
- Observations: "ein Brief" is squeezed in TINY above the line between "forige
  Woche" and "weder" ("endlich war forige Woche [ein Brief] weder zum Josef
  zugeschrieben noch von Euch ein Wort" — "finally last week a letter came, with
  nothing for Josef and not a word from any of you"). Text continues along the
  left-hand edge and top edge, rotated 90° ("auch ganze Fam[ilie]. Mali Küßt
  [unclear] auch alle Eure Chaja"). The three blacked-out lines sit between "soll
  die Ewa und Kinder mir schreiben" and "sonst [grüße] küße Euch vielmal" — the
  writer (or possibly the censor; the ink matches the writing pen) obliterated ~3
  lines with heavy black bars (confirmed in crop: two broad bars).
- Finding: the insertion and edge-writing are space economy on a postcard. The
  blackout is the significant event: content unrecoverable; position (right after
  asking Ewa and the children to write) is noted. Cannot determine author vs.
  censor from the image alone.
- Confidence: medium.

### v) ANAGRAM-LIKE / TRANSPOSED WORDS
- Method: scripted permutation check; manual name-variant review.
- Observations: no anagram pairs. Name variants: "Mali" here vs "Maly" in letters
  18/19 (i/y alternation); "afor" is dialectal "vor" with prosthetic 'a' ("a vor"
  = before), not a transposition.
- Finding: dialectal spelling only. Nothing found. Confidence: high.

### vi) JEWISH RELIGIOUS CODE PATTERNS
- Method: checked HH footnotes; scanned for Hebrew/holiday/liturgical items.
- Observations: "Ostern" (Easter) used as the date anchor of Ewa's plan — a
  Christian holiday used by a Jewish writer as a calendar reference (common in
  Austrian usage; the family also uses "Jom Kipor" in letter 18). No Hebrew
  phrases, no liturgical quotes in this letter.
- Finding: the Easter reference is calendrical, not liturgical. Possible
  double-meaning ("take the children to herself" = bring them to America?) is
  speculation — the sentence reads as a real, failed plan. Nothing found as code.
- Confidence: medium.

### vii) CRYPTOGRAPHY / KNOWN TECHNIQUES
- Method: listed sentence-initials ([pE]d]SAd[M[S[] — transcript-markup noise, no
  pattern), word-initials (no pattern); checked last-letters visually — no pattern;
  examined numbers: "1517" (office stamp), "1268–1345" (pencil filing number);
  postmark "WIEN 20 | 19.7.40.-12 | d" is consistent with the 18/7/40 letter date —
  no anomaly. Looked for diagonal reads and capitalization patterns: none.
- Finding: nothing found. Confidence: medium-high.

### viii) HISTORICAL COMPARISON
- Withholding a letter's existence from Josef, blacking out three lines, and
  relaying addresses via Salomon are all consistent with ordinary caution under
  censorship rather than with a formal cipher (no known WWII civilian-letter
  cipher uses heavy pen pressure as its carrier). The "write that…/tell them…"
  family is present only as ordinary message-relay ("Salomon sent me your
  address"). The Wehrmacht "Checked" stamp (HH footnote 5) confirms the card went
  through military censorship — motive for caution, not evidence of code.

**Per-letter verdict:** No decodable code, but the densest anomaly cluster of the
batch: heavy-ink words inside the Easter-plan sentence, a deliberately withheld
letter, and three blacked-out lines. Best read as a worried family card with
self-censorship, not a cipher.

---

## Letter 18 — 7 Oct 1940, Chaja Willner → Jakob Willner, 2 pages (postcard)

### i) VISIBLE TEXT
- Method: transcript + translation + HH footnotes vs. both scan pages.
- Observations:
  - "die Hias hat mir gesagt von die 50 Dollar was Ihr geschickt hat ich hoffe das
    sie werden mir den Rest Betrag zu geben zu Schiffskarten" ("HIAS told me about
    the 50 dollars you sent; I hope they will give me the remaining sum for ship
    tickets.") — money amount + HIAS + ship tickets, all in one sentence.
  - "nur leider vorleifig kann man nicht fahren auch der Am. K. gibt kein Visum"
    ("unfortunately one can't travel for the time being, and the American consul
    isn't issuing any visas either.") — dated 7 Oct 1940: a factual claim about
    US visa issuance, primary-source-checkable.
  - "fileicht wird der Schwager zu Jom Kipor uns besuchen" ("maybe my
    brother-in-law will visit us for Yom Kippur.") — Yom Kippur 1940 fell on
    12 Oct, 5 days after the letter date: natural timing.
  - "Gebe der l. Gott die Maly soll a Rfua schlajme bkerew haben" ("May God grant
    Maly a refuah shleimah bekarov [a speedy complete recovery].")
  - PS along the left edge: "Frau Stern habe vorige Woche getrofen sie hat Post
    fon H. Stern und Kinder [?] schreiben ihr sehr gute Briefe" ("I met Mrs. Stern
    last week; she gets mail from Mr. Stern and the children write her very good
    letters.") — a description of *other people's* correspondence, included
    without clear purpose: the classic "descriptions of other messages" flag, but
    reads as plain emigrant gossip.
- Finding: the HIAS/$50/ship-ticket/visa sentences are the richest
  primary-source facts in the batch (HIAS case files, consular visa practice, Oct
  1940). No jargon code detected; the Frau Stern PS is gossip-shaped, not
  signal-shaped.
- Confidence: medium-high.

### ii) LIGHTER WORDS
- Method: ink-density comparison; examined address side.
- Observations: faint pencil "184–1682" [uncertain: first digit could be 1 or 2]
  at the bottom-right of the address side (confirmed in crop — faint pencil filing
  number). Blue office stamps "282" and "23b [?]" right of the sender address.
  No lighter message words.
- Finding: filing/office numbers. Nothing found. Confidence: medium.

### iii) SUBTLE MARKINGS
- Method: 170 dpi + zoom crop of the "Rfua" lines.
- Observations: a heavy black INK BLOT runs through the middle of "Rfua"
  ("die Maly soll a Rfua schlajme" — the "fu" is obscured, the blot drips below
  the line toward "bkerew"); a smaller blot after "schlaj" in "schlajme"; blots on
  "vielmals" ("Euch vielmals"), on the "t" of "sollt" ("Alle sollt gesund sein"),
  on the final "e" of "Alle" ("und haben Alle"), and a smudge over "Neu" ("ein
  glücklich Neu Jahr"); a rust-brown spot at the left margin over the "die Maly
  soll" line (looks like foxing/rust, not ink).
- Finding: the "Rfua" blot is the most visually striking — it partially obliterates
  the letter's only Hebrew word. It has the character of a pen blob (occurring
  mid-word at a pen lift), not a placed mark; no pattern across the blots.
  Report as observed; not evidence of marking.
- Confidence: medium that blots are accidental; low for any signaling.

### iv) WORD SKIPS / LAYOUT
- Method: traced both pages.
- Observations: the letter's conclusion and the PS run vertically along the
  left-hand edge in two tight columns: inner column "liebe Kinder meine Maly
  wünscht alle alles beste", outer column the Frau Stern PS. Date "Wien den 7/10"
  with "40" underlined.
- Finding: edge-writing is postcard space economy. Nothing found. Confidence: high.

### v) ANAGRAM-LIKE / TRANSPOSED WORDS
- Method: scripted permutation check.
- Observations: one hit: "Frau" vs "Rfua" ("Frau Stern" / "a Rfua schlajme") —
  exact letter-permutations, but across two languages (German "woman" vs. Hebrew
  רפואה transliterated "refuah"): coincidence, and the "Rfua" token is half
  covered by the blot (see iii). No other pairs; "Maly" spelling consistent in
  this letter.
- Finding: coincidence. Nothing found. Confidence: high.

### vi) JEWISH RELIGIOUS CODE PATTERNS
- Method: checked HH footnotes; identified Hebrew items.
- Observations: "a Rfua schlajme bkerew" appears TWICE (message side and
  continuation) — standard "refuah shleimah bekarov" formula for the sick Mali,
  not a signal; "zu Jom Kipor" is calendrical (correct season); "Neu Jahr"
  wishes on 7 Oct 1940 fall in the holiday season (after Rosh Hashanah, before
  Sukkot ended) — natural.
- Finding: formulas are used naturally and repeatedly, exactly as a worried
  relative writes. Nothing found as code. Confidence: high.

### vii) CRYPTOGRAPHY / KNOWN TECHNIQUES
- Method: sentence-initials ([pEd],[ — markup noise, no pattern), word-initials
  (no pattern); numbers "282"/"23b" are office stamps; postmark "WIEN 20 … 10-17"
  partially legible (HH footnote 3); no diagonal/capitalization patterns;
  underlining only on the date's "40".
- Finding: nothing found. Confidence: medium-high.

### viii) HISTORICAL COMPARISON
- HIAS + dollar amounts + ship tickets + "the consul gives no visas" is the
  textbook plain-sight emigration-logistics vocabulary of 1940 civilian mail —
  facts a censor would pass, and facts historians can verify against HIAS and
  consular records. The "50 Dollar … den Rest Betrag … zu Schiffskarten" chain is
  money tied to a border crossing in the plain sense (paying for tickets), not a
  coded amount.

**Per-letter verdict:** No coded message. The richest factual letter in the batch
for primary sources (HIAS, $50, ship tickets, visa stoppage, Oct 1940). The
"Rfua" blot and "Frau"/"Rfua" anagram are curiosities without evidentiary weight.

---

## Letter 19 — 11 Feb 1941, Chaja Willner → Jakob Willner (+ "Goldiger Erich!"), 2 pages (postcard)

### i) VISIBLE TEXT
- Method: transcript + translation + HH footnotes vs. both scan pages.
- Observations:
  - "ich habe der Ewa geschrieben sie soll den Josef Geld schicken ch glaub sie
    brauch nicht schicken, mir braucht Ihr auch nichts mehr schicken den ich
    übersidel" ("I wrote to Ewa to send Josef money, but I don't think she needs
    to; you needn't send me anything more either, since I'm moving.")
  - "wen Ihr schreibt auf Tante Chawes Adresse sie wird mir fileicht die Briefe
    übergeben" ("if you write to Aunt Chawe's address she will perhaps pass the
    letters on to me.") — a forwarding arrangement; "Tante Chawe" is the writer
    herself referred to in the third person (the children's "Aunt Chawe"; she
    signs "Chaja"). The sender address on the card is still Taborstrasse 67/14.
  - "bis jetzt habe jede Woche geschrieben aber jetzt braucht Ihr nicht besorgt
    sein was ch will nicht so oft schreiben." ("until now I wrote every week, but
    don't worry if I don't write so often now.")
  - "was hat die l. Ewa müssen im Spital gehn?" ("why did dear Ewa have to go to
    hospital?") — Ewa hospitalized (New York), early 1941.
  - "sonst geht es mir sehr gut" ("otherwise I'm very well") — the reassurance
    formula; in this letter its "geht"/"sehr" are the heavy-ink words (see iii).
  - "meine Maltschi schickt Dir 10000000000000 Pusis" ("my Maltschi sends you
    10,000,000,000,000 kisses") — the zero count was verified mechanically in the
    crop: "1" followed by exactly 13 zeros (10 trillion), matching the transcript.
- Finding: the moving + forwarding-address + write-less-often cluster is the
  classic pattern that *can* mask a deportation, but here it is explicitly tied
  to "ich übersidle" (I'm moving house), Feb 1941 — seven months before the
  Vienna deportations began (Oct 1941). Read plainly: a house move with mail
  forwarding. The operationally notable fact is the "Tante Chawe" forwarding
  cut-out. No euphemisms ("emigrated"/"resettled"/"journey") appear.
- Confidence: medium-high for "no code".

### ii) LIGHTER WORDS
- Method: ink-density comparison; address side examined.
- Observations: penciled "962–29" at the lower left of the address side (clear,
  matches transcript). A large RED/ORANGE CRAYON stroke (part of an X) crosses
  the continuation text on the address side — confirmed in crop; it is not the
  author's pen. The purple Wehrmacht eagle censor stamp ("…der Wehrmacht",
  "1866") sits mid-card.
- Finding: "962–29" is a filing number. The red crayon mark and eagle stamp are
  censor/archive handling marks, not authorial. No lighter message words.
- Confidence: medium-high.

### iii) SUBTLE MARKINGS
- Method: 170 dpi + crops.
- Observations: "geht" and "sehr" in "sonst geht es mir sehr gut" are written in
  markedly heavier ink than surrounding words (confirmed on message-side view).
  Blots on "Dir" ("schickt Dir"), on "Ihr" ("Wünschen Ihr"), on "Grüssen"; the
  word "ergere" ("ich ergere mich sehr") is overstruck/corrected mid-word.
- Finding: same sporadic heavy-ink phenomenon as letter 17, here on the
  reassurance sentence. As in 17: visually real, meaning unresolved — pen pressure
  or emphasis; the two words yield no message ("geht… sehr"). The "ergere"
  overstrike is an ordinary self-correction.
- Confidence: medium that heavy ink is real; low for encoding.

### iv) WORD SKIPS / LAYOUT
- Method: traced both pages.
- Observations: two letters in one card: the main letter to Jakob + wife, then
  "Goldiger Erich!" (to the recipients' son Erich) continuing onto the address
  side. No squeezed insertions like letter 17's "ein Brief".
- Finding: nothing anomalous. Confidence: high.

### v) ANAGRAM-LIKE / TRANSPOSED WORDS
- Method: scripted permutation check; manual review.
- Observations: no anagram pairs. Name variants: "Chaja" (signature, letter 17)
  vs "Tante Chawe" (this letter) — the same person spelled with j/w alternation,
  a dialectal feature (also "Maly"/"Maltschi" pet-name). "Mali" (17) vs "Maly"
  (18, 19) i/y alternation.
- Finding: dialectal, not code. Nothing found. Confidence: high.

### vi) JEWISH RELIGIOUS CODE PATTERNS
- Method: checked HH footnotes; scanned for Hebrew/holiday items.
- Observations: "Gebe der Ewiger" ("may the Eternal grant"), "G. s. d." (Gott sei
  Dank) twice — standard formulas. No holidays, no liturgical quotes.
- Finding: nothing found. Confidence: high.

### vii) CRYPTOGRAPHY / KNOWN TECHNIQUES
- Method: sentence-initials ([pEi]sIsA, — markup noise, no pattern),
  word-initials (no pattern); numbers; date/postmark check; zeros count.
- Observations: DATE ANOMALY — the letter is dated "Wien den 11/2 1941" (the "11"
  is unambiguous in the crop; "1941" underlined) but the Vienna postmark on the
  stamp reads "2.2.41-16" (crop-confirmed, no leading "1"). A letter cannot be
  postmarked 9 days before it was written. Most plausible: the writer misdated
  (meant 1/2 or 2/2 — a "11/2" slip for "1/2" fits the 2.2.41 postmark exactly).
  "10000000000000" verified as 1 + 13 zeros — playful hyperbole, not a code
  number. Filing number "962–29".
- Finding: the date anomaly is almost certainly a writer's slip, not a date
  cipher (a cipher would not put the "wrong" date where the censor checks it
  first). Nothing cryptographic found.
- Confidence: medium-high.

### viii) HISTORICAL COMPARISON
- "I'm moving, write via Tante Chawe, don't worry if I write less" is the surface
  shape of the later deportation-era reassurance letter, but in Feb 1941 Vienna
  it is premature for that reading, and the letter gives the mundane reason
  itself (Übersiedlung). No "emigrated"/"resettled"/"on a journey" euphemisms.
  The censor's eagle stamp + red crayon mark show the card was inspected — and
  passed.

**Per-letter verdict:** No coded message. Notable operational fact: the move and
the "Tante Chawe" forwarding arrangement (Feb 1941). Notable anomaly: the
2.2.41 postmark vs. 11/2/41 letter date — best explained as a dating slip.

---

## Letter 15 — 3 Oct 1943, Israel Kohn (155 Edgewood St, Hartford CT) → Ewa Bermann (94 Sheriff St, NYC), Yiddish postcard, 2 pages

### Sources and method
- No transcript, no translation (CSV: "Areas needing attention: Non-German").
  Rendered 15.pdf at 170 dpi (both sides) and the message side at 300 dpi;
  read the Yiddish handwriting visually in three cropped sections. Tesseract has
  no yid/heb language data installed; a `-l deu` attempt on the message side
  returned garbage (documented), so no machine reading was possible. All Yiddish
  readings below are manual and marked [uncertain] where the hand is ambiguous.
  A fluent Yiddish reader is needed for a real transcription.
- Address side: sender "Israel Kohn, 155 Edgewood St, Hartford Conn."; recipient
  "M. Ewa Bermann, 94 Sheriff Street, New York, N.Y."; postmark "HARTFORD OCT 4
  6:30 PM 1943 CONN."; 1¢ Jefferson postal card with "WAR SAVINGS BONDS AND
  STAMPS" slogan. Card date "10/3" vs. 4 Oct postmark: consistent.

### i) VISIBLE TEXT (partial reading)
- Observations (RTL, [uncertain] throughout):
  - Top: "10/3" (Latin) and "ב״ה יום ג׳ הארטפארד" ("B"H, Tuesday[?], Hartford").
    Note: 3 Oct 1943 was a SUNDAY, so "יום ג׳" (Tuesday) mismatches the "10/3"
    date — either a weekday slip by the writer or my misreading of the weekday
    letter. Flagged, low confidence.
  - Salutation: "ליבע … חוה תחי׳" ("dear … Chava, may she live") — the recipient
    is addressed as "Chava" (Ewa's Hebrew name), confirming the family link.
  - "אייער ליבע בריף … האב איך ערהאלטן" ("your dear letter … I received").
  - Mid: "שרייבט מיר בשורות טובות" ("write me good news") — standard closing
    formula, clearly legible.
  - Signature block: three lines beginning "אייער" ("your"), including
    "אייער טרייער" ("your faithful") and a name that reads [uncertain] "יענקל"
    (Yankl) — which does NOT match the address-side sender "Israel Kohn".
    Unresolved: a second family member may have written/signed, or the reading
    is wrong ("ישראל" misread). Needs a Yiddish reader.
- Finding: an ordinary family postcard (acknowledges a letter, asks for news,
  standard formulas). The signature/name mismatch is the one open question.
- Confidence: low (partial reading only).

### ii) LIGHTER WORDS — none observed; single ink throughout. Confidence: medium.
### iii) SUBTLE MARKINGS — pencil doodle: 2–3 short diagonal strokes at the
bottom-right corner (pen-test scribbles, not placed marks). Vertical dotted
smudges down the center are postmark-machine ink transfer, not writing.
Finding: nothing. Confidence: medium.
### iv) WORD SKIPS / LAYOUT — full card used, ~16 lines, no insertions,
no edge-writing, no crossings-out observed. Finding: nothing. Confidence: medium.
### v) ANAGRAM-LIKE / TRANSPOSED WORDS — not testable without a transcription;
no inconsistent spellings spotted in the words I could read. Finding: nothing;
method limited. Confidence: none (gap stated).
### vi) JEWISH RELIGIOUS CODE PATTERNS — "ב״ה" (be'ezrat hashem) opening,
"תחי׳" (tichye) after Chava's name, "בשורות טובות" closing: all standard
epistolary formulas, used naturally. No holiday refs, no liturgical quotes, no
gematria-adjacent numbers. Finding: nothing as code. Confidence: medium.
### vii) CRYPTOGRAPHY — line-initial acrostic not extractable without reliable
transcription (gap stated). Numbers: "10/3" (date), "155" (street address) —
address/date, not cipher. No book-cipher references. Finding: nothing found
within the limits of a partial reading. Confidence: low (method-limited).
### viii) HISTORICAL COMPARISON — Yiddish in Oct 1943 US domestic mail is
unremarkable (no German-only rule applied outside occupied Europe); there is no
censorship motive for this Hartford→NYC card. The "write me good news" formula
is the normal diaspora-letter close, not a signal.

**Per-letter verdict:** No code detectable in a partial reading; an ordinary
Yiddish family postcard. Two flags for follow-up: (1) the "יום ג׳" vs. Sunday
10/3/1943 mismatch [uncertain reading]; (2) the signature name reading
"יענקל" vs. sender "Israel Kohn" — needs a Yiddish reader to resolve.

---

## Letter 16 — 11 June 1942 [CSV says 1942-07-11], Kalman Willner (314 1/2 State St, Los Angeles) → Mrs. Eva Berman (94 Sheriff St, NYC), Yiddish postcard, 2 pages

### Sources and method
- No transcript, no translation (CSV: "Non-German"). Rendered 16.pdf at 170 dpi
  (both sides); a 300 dpi render was partially blocked by a full /tmp (only
  page 1 completed). Visual reading of the message side (~24 dense lines +
  vertical right-edge continuation) at 170 dpi. Tesseract `-l deu` attempt =
  garbage (no yid/heb data installed). Readings below are word-spotting only,
  all [uncertain].

### i) VISIBLE TEXT (partial)
- Address side: sender written vertically at left: "K. Willner 314 1/2 S. State
  Str. Los Angeles California" [uncertain: "S. State"]; recipient "Mrs. Eva
  Berman, 94 Sheriff Street, New-York City, N.Y."; postmark "LOS ANGELES JUN 11
  11 AM 1942 CALIF." — the postmark reads JUN (June), contradicting the CSV
  date 1942-07-11. The CSV date is likely wrong; the card is June 1942.
  1¢ Jefferson postal card.
- Message side: dense cursive Yiddish, right-to-left; spot-read words include
  "איר/אייער" (your), "ליבע" (dear), "בריף" (letter), "ערהאלטן" (received),
  "געזונט" (health), "שרייבט" (write), "גרוס" (greetings) — the standard
  family-letter vocabulary. No ב״ה opening visible. A vertical (rotated)
  continuation runs down the right edge. Two small bluish stains mid-left are
  paper stains, not ink.
- Finding: ordinary family postcard vocabulary as far as can be read; no
  content-level anomaly visible.
- Confidence: low (word-spotting only).

### ii)–iv) LIGHTER WORDS / MARKINGS / LAYOUT — single dark ink throughout; no
placed marks; no insertions or crossings-out visible at this resolution; the
right-edge vertical text is a space-economy continuation. Finding: nothing.
Confidence: low-medium (resolution-limited).
### v) ANAGRAM-LIKE — not testable without transcription (gap stated).
### vi) RELIGIOUS CODE — no Hebrew formulas spotted; no holiday refs visible.
Finding: nothing (resolution-limited). Confidence: low.
### vii) CRYPTOGRAPHY — acrostic/initials not extractable (gap stated). Numbers:
"314 1/2" (address), "JUN 11 1942" (postmark). Finding: nothing.
Confidence: low (method-limited).
### viii) HISTORICAL COMPARISON — as with letter 15: Yiddish in 1942 US domestic
mail needs no censorship motive; nothing about the card suggests concealment.

**Per-letter verdict:** No code detectable at the available resolution. The card
needs a proper Yiddish transcription (300 dpi re-render when /tmp allows).
Correction for the index: the postmark is JUN 11 1942, not July — the CSV date
1942-07-11 appears to be an error.

---

## Cross-letter observations (14–19)

1. **The "X is earning" formula** recurs: "der Josef ferdient es geht im ganz gut"
   (14, Klara, Aug 1940), "der Josef ferdient, er ist in [?] noch dort" (17, Chaja,
   Jul 1940). Plain employment reassurance; consistent across two authors.
2. **Ship tickets as the through-line**: "keine Schiffskarten … von der Isr. K."
   (14, Aug 1940) → "die 50 Dollar … den Rest Betrag zu geben zu Schiffskarten …
   der Am. K. gibt kein Visum" (18, Oct 1940) — a coherent HIAS/IKG/visa timeline,
   all primary-source-checkable (HIAS case files, IKG emigration records, US
   consular practice).
3. **Heavy-ink words** appear in exactly two letters, both by Chaja Willner:
   letter 17 ("afor", "nimt", "zu", "das", "zum" — clustered in the Easter
   sentence) and letter 19 ("geht", "sehr" — in "sonst geht es mir sehr gut").
   Visually confirmed in crops. No hidden message emerges from the marked words
   in either letter; pen-pressure variation or emphasis are equally plausible.
   Worth one comparative look by whoever studies Chaja's hand across the corpus,
   but not evidence of a marking code on its own.
4. **Filing numbers** (pencil/office, not authorial): "1398a" (14), "1517" stamp
   + "1268–1345" pencil (17), "282"/"23b" stamps + "184–1682"[?] pencil (18),
   "962–29" pencil (19). Archival processing marks; not codes.
5. **Name-spelling instability** (dialectal, not code): Mali/Maly (i/y),
   Chaja/Chawe (j/w), geschreiben/geschrieben, ferdient/verdient. The scripted
   permutation check found only the geschreiben/geschrieben pair (a natural
   misspelling) and the coincidental cross-language Frau/Rfua pair.
6. **Mechanical null results**: sentence-initials and word-initials listed for
   all four German letters — no acrostic words or names; no n-th-letter, diagonal,
   capitalization, or underlining patterns (underlining occurs only on dates:
   "40" in 18, "1941" in 19).
7. **Date anomalies**: 19 (postmark 2.2.41 vs letter date 11/2/41 — writer's slip
   most likely); 16 (postmark JUN 11 1942 vs CSV 1942-07-11 — CSV likely wrong);
   14 (scan resolves CSV's "June or Aug" to 28/8); 15 ("יום ג׳" vs Sunday
   10/3/1943 — uncertain reading).
8. **Censorship context, all German cards**: Wehrmacht "Checked" stamps on 17
   and 19 (HH footnotes), eagle stamp on 19, red crayon mark on 19 — the cards
   were inspected and passed. Motive for caution existed; no concealed-message
   technique was found in any of the six letters.

## Crop requests (for the imaging worker)

1. Letter 19, PDF p.1, anchor "Dir 10000000000000 Pusis" → crop the zero-string
   to archive the verified 13-zero count (finding: playful hyperbole, not code).
2. Letter 19, PDF p.1, anchor postmark "2.2.41-16" on the green 6 stamp →
   crop the postmark date (finding: 9-day predate anomaly vs "11/2 1941").
3. Letter 19, PDF p.2, anchor "Wien den 11/2 1941" → crop the date line
   (finding: confirms the "11" is genuine, anchoring the anomaly).
4. Letter 17, PDF p.2, anchor "hat afor die Ostern" (lines 8–11) → crop the
   heavy-ink cluster (finding: heaviest marking anomaly in the batch).
5. Letter 17, PDF p.1, anchor the two black bars below "mir schreiben" → crop
   the redaction (finding: ~3 lines blacked out, content unrecoverable).
6. Letter 17, PDF p.1, anchor lower edge "1268–1345" → crop the pencil filing
   number (finding: archival mark, faint first digit).
7. Letter 18, PDF p.2, anchor "a Rfua schlajme" → crop the ink blot through
   "Rfua" (finding: blot partially obliterates the letter's only Hebrew word).
8. Letter 14, PDF p.1, anchor upper-left "1398a" → crop the pencil number
   (finding: archival filing number, lighter than body ink).
9. Letter 14, PDF p.1, anchor "zu Etlen" at the crumpled right edge → crop the
   name (finding: "Etlen"[?] — likely "Etel"/Ettel, edge obscures).
10. Letter 18, PDF p.1, anchor bottom-right faint "184–1682" → crop the pencil
    number (finding: faint archival filing number, first digit uncertain).
11. Letter 15, PDF p.2, anchor signature block ("אייער טרייער … [יענקל?]") →
    crop for a Yiddish reader (finding: name does not match sender "Israel Kohn").
12. Letter 16, PDF p.1, anchor postmark "JUN 11 1942" → crop (finding: corrects
    the CSV's 1942-07-11 dating).

# Forensic reading report — worker w4: letters 20, 21, 22, 23, 24, 25

Worker: w4 (subagent, fresh eyes; no existing analysis files read)
Date of examination: 2026-10-16
Corpus paths used: `~/workspace/goals/the-coded-letters/hidden_files/trans/transcription-{23,24,25}.txt`, `~/workspace/goals/the-coded-letters/hidden_files/letters/translation-{23,24,25}.docx` (body via python-docx, footnotes via word/footnotes.xml), scans `~/workspace/goals/the-coded-letters/hidden_files/drive/allpdfs/{20,21,22,23,24,25}.pdf` rendered with `pdftoppm -r 170` (plus 300 dpi crops for the Yiddish cards), and `LastLettersCSV.csv` for metadata only.

Method per letter: (a) read German transcript + English translation + all HH footnotes; (b) view every scan page; (c) compare image against transcript for dropped layout/markings/lightness; (d) mechanical checks run by script: sentence-initials, sentence-final letters, per-sentence word-initial strings, line-initials on the message side, strict anagram/inconsistent-spelling scan; (e) visual scan for lighter words, markings, layout anomalies at full page and at crop zoom. Letters 20/21/22 have no transcript and no translation: letter 20 (legible English hand) transcribed by me, marked as my reading; letters 21/22 (Yiddish, Hebrew script) skimmed visually only — no reliable transcription possible (see gaps).

Privacy note: letter 20's author/recipient are redacted in the CSV ("Private letter to Tante Malka"). The card itself bears handwritten names/addresses; I reproduce only what is needed for the forensic record and do no further identification work.

---

## Letter 20 — undated in CSV; card dated 4/23/52 and postmarked Lakewood NJ Apr 23 1952; 2 PDF pages

CSV: author [redacted], recipient [redacted], note "Private letter to Tante Malka". No transcript/translation exists.
Scan: US 2-cent postal card. Page 1 = address side; page 2 = message side.

Address side (my reading): sender "T. Mandelkorn / 346 Dewey Ave. / Lakewood, N.J."; recipient "Miss Malka Berman / 94 Sheriff St. / New York 2, N.Y." Postmark: LAKEWOOD, N.J., APR 23, 2:30 PM, 1952. Printed "THIS SIDE OF CARD IS FOR ADDRESS".

Message side (my transcription; handwriting is clear English cursive, readings high-confidence except where marked):

"4/23/52
Dear Malka,
How are you and the family?
The directions for coming here are:
1 Take Lincoln Transit Co. bus at Port Authority Terminal 8th Ave. + 40th N.Y.C. going to Lakewood.
At Lakewood ask directions to 4th St. On 4th St. ask for East 4th St. which is the eastern section of the st.
Walk along East 4th St. till you reach Dewey Ave.
The walking distance is about 9 blocks. If you write the time you are coming I will meet you at the station"

The message ends at the bottom edge of the card ("station" slightly clipped by the edge but legible). There is NO signature on the message side; the sender is identified only via the address side. The date "4/23/52" at top is in a thinner, lighter hand than the message body.

### i) Visible text
- Method: read my transcription against the image, checked every noun/number for double meaning.
- Observations: The text is mundane bus directions, internally consistent and factually accurate: the Port Authority Bus Terminal is at 8th Ave/40th St; Lincoln Transit Co. was a real NJ bus operator; the sender's own address is 346 Dewey Ave, Lakewood, matching the destination "Dewey Ave". "4th St." is repeated three times ("to 4th St. On 4th St. ask for East 4th St."), and "about 9 blocks" is given. No money, no euphemisms, no descriptions of other messages, no non sequiturs.
- Finding: The repetition of "4th St." is ordinary wayfinding redundancy (distinguishing 4th St. from East 4th St.), not a code pattern. Nothing reads as jargon code. This is a 1952 US domestic card; there is no censorship motive.
- Confidence: high.

### ii) Lighter words
- Method: compared stroke weight across the message side at full page and in crops.
- Observations: The date "4/23/52" (top) is written in a visibly thinner/lighter hand than the body text (thick black ink). Within the body, "the eastern section of the st." is written slightly smaller but in the same ink. One light smudge sits right of "the" in line 2 ("How are you and the [smudge]").
- Finding: The lighter date hand suggests the date was added with a different pen, possibly by the recipient when filing, or by the writer before picking up the thicker pen. No content word is selectively lightened. Nothing found.
- Confidence: medium (the two-hand observation is solid; its meaning is undetermined).

### iii) Subtle markings
- Method: inspected margins, line starts/ends, interlinear space at 170 dpi and in crops of the left margin, top, and bottom.
- Observations: (1) A large curved pen stroke brackets the words "for East 4th St. which is" on the left (like a parenthesis drawn around the phrase). (2) Three to four vertical pen strokes run down the left margin alongside the last four lines ("The walking distance is / about 9 blocks. If you / write the time you are / coming I will meet you at the station"), crossing the text. Same black ink as the body. (3) Small ink dots after abbreviations ("40th.", "N.Y.C.", "St.") are the writer's normal periods.
- Finding: The curve and the vertical margin strokes are deliberate pen marks emphasizing the final instructions, but their authorship is unknown (writer's emphasis vs. a later reader's). They carry no decodable content. Noted, not a cipher.
- Confidence: medium on the observation; none on authorship.

### iv) Word skips / layout
- Method: checked line breaks, margins, and the card edges.
- Observations: Text fills the message side top to bottom; the last word "station" is clipped by the bottom edge. No squeezed insertions, no cross-outs, no margin cramming beyond the edge clip, no skipped words.
- Finding: nothing found. Confidence: high.

### v) Anagram-like / transposed words
- Method: listed all content words; checked for letter-permutations and inconsistent spellings.
- Observations: none. Spelling is standard.
- Finding: nothing found. Confidence: high.

### vi) Jewish religious code patterns
- Method: scanned for Hebrew phrases, blessings, holiday references.
- Observations: none present.
- Finding: nothing found. Confidence: high.

### vii) Cryptography / known techniques
- Method: listed line-initials of the 18 message lines: D-H-T-T-C-T-N-A-t-f-t-W-t-T-a-w-c-s. Checked sentence-initials and final letters; checked for null-word patterns, book-cipher references, deliberate misspellings.
- Observations: initials form no word or name in either direction; no n-th letter regularity; no references to other letters/pages; no misspellings at all.
- Finding: nothing found. Confidence: high.

### viii) Historical comparison
- Method: compared against the wartime euphemism/jargon-code conventions.
- Observations: 1952 US domestic postcard, no censor marks, English (not German/Yiddish). No "emigrated/resettled" language, no forced cheerful formulas.
- Finding: no censorship motive exists for this item; it is almost certainly in the corpus only as family context ("Tante Malka"). Nothing found. Confidence: high.

Per-letter verdict: No hidden or coded message. A plain 1952 directions postcard from T. Mandelkorn (Lakewood NJ) to "Miss Malka Berman" (94 Sheriff St, NYC). Only anomalies are non-textual margin strokes of unknown authorship and a lighter-weight date hand. Genealogical side-note (not code): the "Miss Malka Berman" / "M. E. Berman" (letter 22) recipient forms at the same 94 Sheriff St address used for "Mrs Berman"/"Ewa Bermann" suggest Malka may be Ewa's Jewish name; flagged as an identity lead with the privacy caveat, no further work done.

---

## Letter 21 — 1943-10-07, Kalman Willner, 330 1/2 So. State St, Los Angeles, CA, to Ewa Bermann, 94 Sheriff St, NYC; Yiddish postcard; 2 PDF pages

CSV: author Kalman Willner, Yiddish postcard, no transcript/translation.
Scan page 1 (address side): sender written vertically at left, my reading "Kal. Willner / 330 1/2 So. State St / Los Angeles"; recipient "Mrs Berman / 94 Sheriff St / New York / N.Y." Postmark: LOS ANGELES, OCT 7, 1 PM, 1943. US postal card with "BUY WAR SAVINGS BONDS AND STAMPS" machine cancel.
Scan page 2 (message side): ~20 lines of handwritten Yiddish in Hebrew-script cursive, written in pencil, faint, filling the card edge to edge, right-to-left.

### i) Visible text
- Method: visual skim at 170 dpi and 300 dpi crops of the top portion.
- Observations: The script is small, faint pencil, idiosyncratic cursive. I could not reliably transcribe it. Isolated uncertain guesses: the top-right line may open with ב"ה ("b"H", with God's help) [uncertain]; a middle line may contain קארטל ("kartl", card) [uncertain]. No transcript exists and tesseract has no Yiddish/Hebrew traineddata installed, so no OCR attempt was possible.
- Finding: content unknown; honest gap. The card is US domestic (LA to NYC), 1943; Yiddish is used openly on a postcard, which is consistent with no censor to evade (Nazi postal rules banning Yiddish applied to mail under German control, not US domestic mail). Nothing found; nothing decodable by me.
- Confidence: none on content; high on the contextual point.

### ii) Lighter words
- Method: compared stroke weight across the message side.
- Observations: The entire message is in uniformly light pencil; no word or line is selectively lighter or darker. The address side is in darker pencil/ink.
- Finding: the lightness is the writing medium (pencil), not selective emphasis. Nothing found. Confidence: medium.

### iii) Subtle markings
- Method: inspected margins, interlinear space, card edges at 300 dpi.
- Observations: no underlines, dots, circles, or margin marks attributable to the writer beyond normal script. No censor stamps on either side (only the US postmark and war-savings cancel slogan).
- Finding: nothing found. Confidence: medium (faint pencil limits certainty).

### iv) Word skips / layout
- Method: checked line structure and edges.
- Observations: regular horizontal lines, right-to-left, filling the card; no insertions, cross-outs, margin cramming, or orientation changes.
- Finding: nothing found. Confidence: medium.

### v) Anagram-like / transposed words
- Method: not applicable without transcription.
- Finding: cannot assess; no transcript exists. Confidence: none.

### vi) Jewish religious code patterns
- Method: visual scan for Hebrew-script religious formulae.
- Observations: possible ב"ה opening [uncertain]; no identifiable liturgical quotes or holiday references could be confirmed.
- Finding: nothing confirmed. Confidence: none.

### vii) Cryptography / known techniques
- Method: none applicable without a readable text.
- Finding: cannot assess. Confidence: none.

### viii) Historical comparison
- Method: compared the mailing context against the censorship-motivation model.
- Observations: US domestic postcard, October 1943, Yiddish used openly, no censor marks.
- Finding: no plausible censorship motive; Yiddish here is the family vernacular, not a cover. Nothing found. Confidence: high on context.

Per-letter verdict: No code indicators; content inaccessible to me (Yiddish cursive in faint pencil, no transcript, no Yiddish OCR available). Recommend a Yiddish reader transcribe it before any content-level claims. The only primary-source facts extractable are the sender address (Kalman Willner, 330 1/2 So. State St, Los Angeles) and the October 7, 1943 postmark.

---

## Letter 22 — 1944-08-09, Israel Kohn, 1307 Main St, Hartford, Conn., to Ewa Bermann, 94 Sheriff St, NYC; Yiddish postcard; 2 PDF pages

CSV: author Israel Kohn, Yiddish postcard, no transcript/translation.
Scan page 1 (address side): sender (top left) "Israel Kohn / 1307 Main St / Hartford Conn."; recipient "M. E. Berman / 94 Sheriff St. / New York / N.Y." Postmark: HARTFORD CONN, AUG 9, 10:30 PM, 1944. Vertical blue-ink notation at right edge reading "n 1521" (my reading; the "n" may abbreviate "number").
Scan page 2 (message side): ~14 lines of Yiddish in Hebrew-script cursive, black ink, right-to-left. A large accidental-looking ink blot covers part of the left side (lines ~9-11). The top line begins with "9/8" in Latin digits followed by Yiddish text (the written date, matching the Aug 9 postmark).

### i) Visible text
- Method: visual skim at 170 dpi and 300 dpi crops (top, middle, bottom).
- Observations: No transcript exists; tesseract has no Yiddish traineddata. Partial uncertain readings only: the bottom line appears to end with a signature-like word resembling "ישראל" (Yisroel/Israel) [uncertain]; one mid-card line may read "בשורות טובות" ("b'suros tovos", good tidings — a standard Yiddish closing formula) [uncertain]. The large ink blot obscures several words on the left.
- Finding: content largely inaccessible; the two uncertain readings, if correct, are conventional formulae, not code. The penciled "n 1521" on the address side matches the style of penciled numbers on letters 23 ("2511-1399a") and 25 ("1820–2622") — likely a family filing number or a processing number; origin undetermined. Primary-source facts: sender Israel Kohn, 1307 Main St, Hartford, Conn.; recipient styled "M. E. Berman".
- Confidence: low on the word guesses; high that they are conventional if correct; medium on the "n 1521" reading.

### ii) Lighter words
- Method: compared stroke weight across the message side.
- Observations: uniform black ink throughout; the superimposed vertical strokes (see iii) are in a greyer medium but are not script. No content word is selectively lighter.
- Finding: nothing found. Confidence: medium.

### iii) Subtle markings
- Method: inspected at 300 dpi crops; counted superimposed strokes.
- Observations: (1) Two clusters of straight vertical strokes in a grey pencil/crayon-like medium are superimposed OVER the Yiddish text: a top-right cluster of ~7 strokes spanning lines 2-3, and a mid-card cluster of ~7 strokes spanning ~3 lines. They are not part of the script and cross over the writing. (2) The large ink blot on the left is irregular, with satellite spatter — consistent with an accidental pen spill, and it obscures text rather than marking it. (3) No underlines, circles, or dots attributable to the writer.
- Finding: The two ~7-stroke clusters are the most anomalous non-textual feature in this letter batch. They look like tally/counting marks added later (by whom and why is unknown — possibly a reader counting lines, a filing mark, or idle pen strokes). They carry no decodable content themselves. Flagged as an unexplained marking, not a cipher.
- Confidence: high on the observation; none on authorship or purpose.

### iv) Word skips / layout
- Method: checked line structure and edges.
- Observations: regular right-to-left lines; the blot area aside, no insertions, cross-outs, or margin cramming.
- Finding: nothing found. Confidence: medium.

### v) Anagram-like / transposed words
- Method: not applicable without transcription.
- Finding: cannot assess. Confidence: none.

### vi) Jewish religious code patterns
- Method: visual scan for religious formulae.
- Observations: possible "בשורות טובות" closing [uncertain]; date line "9/8" in Latin digits. No identifiable liturgical quotes.
- Finding: nothing confirmed; the possible closing is conventional. Confidence: low.

### vii) Cryptography / known techniques
- Method: none applicable without a readable text. The two 7-stroke clusters were considered as possible tallies: two groups of ~7 with no accompanying key or context; no textual anchor.
- Finding: cannot assess textually; the stroke clusters are noted under (iii) and are not decodable. Confidence: none.

### viii) Historical comparison
- Method: compared mailing context against the censorship model.
- Observations: US domestic postcard, August 1944, Yiddish used openly, no censor marks.
- Finding: no plausible censorship motive. Nothing found. Confidence: high on context.

Per-letter verdict: No code indicators in the accessible features. Content inaccessible (no transcript; partial uncertain skim only). Two unexplained clusters of ~7 vertical tally-like strokes superimposed on the text are the one anomaly worth a closer look by the coordinating team (crop requested). Recommend Yiddish transcription before content-level analysis.

---

## Letter 23 — 1940-08-13, Chaja Willner, Wien II, Taborstrasse 67/14, to Ewa Bermann, 94 Sheriff St, NYC; German postcard; 2 PDF pages

Transcript + translation + 4 HH footnotes read in full. Scan page 1 (PDF p.1) = address side with the letter's continuation on the left half and vertical conclusion "auch Mali lässt Alle schön grüßen" along the left edge; scan page 2 (PDF p.2) = message side beginning "Wien den 13/8 40 / Liebe Schwester!".

### i) Visible text
- Method: close reading of transcript against translation and image; flagged every concrete fact, amount, route, and message-about-message.
- Observations:
  - "Deine l. Karte von 1/7 und Brief von 8/7 habe den 9/8 erhalten" (I received your dear card of 1 July and letter of 8 July on 9 August) — a five-week transit time, consistent with wartime airmail.
  - "wegen die l. Mali ihre Papiere hat glaub ich, daß schon, 3 Monat daß der Josef hat zum A. Konsul geschrieben, er soll sie überschiken" (regarding dear Mali's papers, I think it is 3 months now since Josef wrote to the American consul [saying] he should send them over) — HH footnote flags the phrasing as ambiguous (possibly: "it is three months since Josef wrote to the American consul. He is supposed to be sending them over"). Either way: a dated contact with the US consulate (~May 1940) about Mali's papers — a fact likely to produce primary sources (consulate correspondence/visa file).
  - "bitte schreibe ob Du ferdienst" (please write whether you are earning) — a work/income question; no amounts named.
  - "der Josef hat mir gegeben ein Brief ich soll ihm Dir schicken" (Josef gave me a letter, I am to send it to you) and "habe grad Deine Schwägerin getrofen und sie wolte apaar Worten zu Ruchale schreiben, habe ihr gegeben" (I just met your sister-in-law and she wanted to write a few words to Ruchale; I gave her [the letter]) — a documented chain of custody: Josef's letter physically carried inside Chaja's mailing, with the sister-in-law adding words for Ruchale. Descriptions of other messages, but mundane relay logistics.
  - "fon mir wie Ihr schon weist hätte schon zu Untersuchung nur müsste ich die Schiffskarten haben wan es wirklich möglich ist bitte sehr über Lisabonn mir zu schiken" (as you know I should already have been to the examination, only I would need to have the ship tickets; if it is really possible please send them to me via Lisbon) — "Untersuchung" is the visa medical examination; "Schiffskarten" (ship tickets) via Lisbon names the known emigration route (Portugal). No prices, no dates, no ship names.
  - "habe Euch ein Rekomandierten Brief geschrieben habt Ihr den erhalten" (I wrote you a registered letter; did you receive it) — reference to another message; mail-reliability checking, standard in this correspondence.
  - "meine Mali sekiert mich sehr oft wan werden wir schon nach U.S.A. fahren" (my Mali pesters me very often [about] when we will finally go to the USA) — note: this is Chaja's Mali, in Vienna with her, distinct from Josef and Ewa's daughter Mali (see letter 25 analysis).
  - "fon Schwager ist sehr oft Post. es geht ihm gut." (from [my] brother-in-law comes mail very often. He is doing well.) — an unidentified brother-in-law in regular contact; identity not established in this letter.
  - "bittesollen die Kinder auch zu schreiben zu Dein Brief" (please, the children should also write in your letter) — message-relay instruction, mundane.
  - Penciled along the lower edge: "2511-1399a [?]" (my image reading concurs, faint). Purple boxed stamps "1517" (by the sender's address) and a boxed stamp over the street line reading "1932" [uncertain — HH footnote suggests "1532" [?]]. Round censor stamp with swastika, partially legible "…mando der … Geprüft" (HH footnote: "Checked [?] | Wehrmacht High Command"), plus "MIT LUFTPOST / PAR AVION" sticker and Deutsches Reich 6pf stamp.
- Finding: The letter is dense with emigration-logistics facts that could produce primary sources (US consulate file re Mali's papers ~May 1940; Chaja's pending medical examination; Lisbon-route ship tickets; the registered letter). No money amounts, no coded euphemisms ("emigrated", "resettled", "on a journey" do not appear), no odd repetitions beyond normal epistolary formulae, no non sequiturs. The "Untersuchung"/"Schiffskarten"/"Lisabonn" vocabulary is the plain language of 1940 Vienna emigration efforts, matching the known plain-sight conventions as ordinary usage rather than jargon code. The penciled "2511-1399a" is of unknown origin (postal processing vs. family filing).
- Confidence: high on the reading; medium that no euphemism is present (a domain expert should confirm "Untersuchung" had no secondary sense, but the visa-medical reading is strongly supported by context).

### ii) Lighter words
- Method: compared stroke weight across both sides at full page.
- Observations: uniform brownish ink throughout; the date's "40" is underlined (see iii). No word or line is selectively lighter or fainter. The penciled number is lighter because it is pencil.
- Finding: nothing found. Confidence: high.

### iii) Subtle markings
- Method: inspected at full page; checked tops of lines, interlinear space, margins.
- Observations: (1) The "40" in "Wien den 13/8 40" is underlined. (2) The digit "3" in "3 Monat" is written larger and darker than surrounding text. (3) A dark smudge/stamp remnant sits at the top-right corner of the message side. (4) Small stroke over "Schwägerin" is the ä umlaut. (5) Postal/censor stamps and the penciled number as listed in (i).
- Finding: The underlined "40" and the heavy "3" are emphasis of the date and the waiting time — consistent with the letter's anxious theme (three months without Mali's papers), not a code. The top-right smudge is likely a stamp/ink transfer. Nothing found beyond ordinary emphasis. Confidence: medium-high.

### iv) Word skips / layout
- Method: traced the text flow across both sides.
- Observations: message side is filled top to bottom; the letter continues onto the address side's left half (normal postcard practice) and concludes with a vertical line "auch Mali lässt Alle schön grüßen" along the left edge (also normal). No squeezed insertions, cross-outs, skipped or rewritten words.
- Finding: nothing found. Confidence: high.

### v) Anagram-like / transposed words
- Method: scripted strict letter-permutation scan over the transcript; manual check of name spellings.
- Observations: no true anagram pairs. Inconsistent spellings: "Lisabonn" (for Lissabon), "ferdienst" (verdienst), "Rekomandierten" (Rekommandierten), "getrofen" (getroffen), "Schwägerin" with dialectal forms — all consistent with Chaja's phonetic/dialectal spelling, also seen across the corpus. "Mali"/"Mina"/"Jakob"/"Ruchale" are spelled consistently.
- Finding: dialectal orthography, not transposition code. Nothing found. Confidence: high.

### vi) Jewish religious code patterns
- Method: scanned for Hebrew phrases, blessings, holidays, liturgical quotes; checked HH footnotes (none identify quotes here).
- Observations: none present.
- Finding: nothing found. Confidence: high.

### vii) Cryptography / known techniques
- Method: listed message-side line-initials (26 lines): W-L-D-v-u-u-h-d-g-b-v-w-u-s-g-s-g-W-h-w-w-z-i-e-ü-h; sentence-initials WDDMSAFFEECS; sentence-final letters RTTUSANTTRIA; per-sentence word-initial strings (checked for embedded words). Checked for null-word patterns, book-cipher references ("as I wrote…"), deliberate misspellings, diagonal reads.
- Observations: no initials sequence spells a word or name in either direction; last letters likewise random; the only cross-letter reference is the registered letter already noted in (i). Misspellings are dialectal, not systematic.
- Finding: nothing found. Confidence: high.

### viii) Historical comparison
- Method: compared against the civilian-euphemism and jargon-code conventions; noted the censor context.
- Observations: The card demonstrably passed military censorship (Wehrmacht "Geprüft" stamp, airmail). Dated August 1940, pre-deportation; the family is actively pursuing legal emigration (consul, medical exam, Lisbon tickets). The vocabulary matches documented plain-sight emigration correspondence; none of the known deportation euphemisms appear, correctly for the date.
- Finding: no coded layer indicated; the letter's "code-like" density is fully explained by emigration logistics under censorship. Nothing found. Confidence: high.

Per-letter verdict: No hidden message. A plain, censorship-passed August 1940 emigration-logistics postcard whose value is as a primary-source pointer (US consul contact ~May 1940 re Mali's papers; Chaja's pending examination; Lisbon ticket request). Only anomalies are ordinary emphasis marks (underlined "40", heavy "3") and postal/censor stamps plus one penciled number of unknown origin.

---

## Letter 24 — 1940-04-10, Josef Bermann to Ewa Bermann; German; 2 PDF pages (transcript describes 3 letter-faces on one folded sheet)

CSV notes: "Folded paper, multiple directions"; HH: "Also contains letter from Ruchalen [?]"; "Text is blurred in top right-hand quarter and faint on bottom half of sheet."
Scan page 1: front of the folded sheet. Top half = Josef's letter in brown Kurrent ink (starts top-right "Wien 10 April 1940 / Liebe Frau und liebe Kinder!", continues down the right column, then the left column continues "ich muß noch abwarten…" ending "…von mir Josef"). Bottom half = Ruchalen's letter in much fainter blue-grey ink, written in vertical columns (rotated 90°) with a continuation upside-down along the top edge ("beste Gruß…"), signed "beste Gruße Ruchalen" at the bottom of the first page. A short note in a smaller darker hand runs across the central fold ("Vom [?] … Schon for der Zeit was hat zu dir zu geschrieben" — HH: likely a note explaining the second-author message). An irregular dark ink blot sits at the left edge where Ruchalen's text begins.
Scan page 2: back of the sheet — Josef's brown text shows through/bleeds from the front; Ruchalen's faint columns continue.

### i) Visible text
- Method: close reading of transcript + translation + footnotes against the image.
- Observations (Josef):
  - "Es wundert mich sehr daß habe von dir noch von den lieben Kinder kein einziges Schreiben bekommen aber von der liebe Regina habe eine Karte bekommen" (It greatly surprises me that I have not received a single letter from you or the dear children, but I did receive a card from dear Regina) — mail-gap anxiety; Regina's postcard is a referenced other message.
  - "Bist du gesund? Wohnst du in der Nähe von der Mina? Was macht der Onkel überhaupt die ganze Familie? Bekomms du von der liebe Mali Schreiben? Was schreibt sie Dir? Wie geht es ihr?" (Are you healthy? Do you live near Mina? What is uncle doing, indeed the whole family? Are you getting letters from dear Mali? What does she write? How is she?) — rapid questions; "der Onkel" and "Mina" are the New York family circle.
  - "Die Jetti Lachs hat am 20ten April zur Untersuchung und Ruche Lea. Ich hoffe daß es mir gelingen zur Mali zu kommen" (Jetti Lachs has her examination on 20 April, and Ruche Lea too. I hope I will manage to get to Mali) — dated visa-examination appointments (primary-source pointer: consulate/medical records, April 1940); "zur Mali zu kommen" = join daughter Mali in America.
  - "Von der Berta hat Ruchel Lea ein Brief bekommen wo sie schreibt daß unsere lieben Kinder bei der lieben Rojse waren zu Besuch. Bitte dich auch du sollst zu ihr hingehen" (Ruchel Lea got a letter from Berta saying our dear children visited dear Rojse [name uncertain — HH: "Rojse appears to be the likeliest reading"]. Please, you go visit her too) — referenced other message (Berta's letter); "Rojse" is an unidentified person, a genealogical lead.
  - "100000000000000 Pussi du kannst den Kindern austeilen statt meiner und wunsche Euch einen lustigen Pesach" (100,000,000,000,000 kisses — you can distribute them to the children for me — and I wish you a happy Passover) — "Pussi" is regional for "Bussi" (HH footnote); the 10^14 is hyperbolic affection, not gematria; "lustigen Pesach" is timely (Passover began the evening of 16 April 1940).
  - "Besondere Grusse an meiner lieben Schwester Rosa und Familie auch lasse die lieben Berta Willi und das suse Kind grussen von mir Josef" (Special greetings to my dear sister Rosa and family; greet dear Berta, Willi and the sweet child from me, Josef) — note "Willi" here vs. Ruchalen's "Wielen" (HH: likely a declined form of a "Willi" variant spelling).
- Observations (Ruchalen):
  - "Liebe Chawze Leben" (Dear Chawze, [my] life) — "Chawze" is a Yiddish-influenced spelling of Chava/Eva.
  - "Es freud mich sehr was die lieben Kinder Kinder senene gut aufgehoben" (I am very glad the dear children are well looked after).
  - "warst du bei mein Bertha warum hat die Bertha kein grus zu geschrieben [deletion]" (were you at my Bertha's — why didn't Bertha write a greeting; with a deletion) — the transcript notes one deletion; I could not resolve it at 170 dpi.
  - "die Bertha hat geschrieben sie schickt mir Afidawid bis heute keines erhalten" (Bertha wrote she is sending me an affidavit; to this day I have received none) — emigration-logistics fact: a promised US affidavit that never arrived (primary-source pointer).
  - "Ich habe erhalten fon meine Kinder ein Brief mit grossen sensucht nach 3 Monat auch Fategrafie von Wielen mit den susen Kind bis Hundert Jahr" (I received a letter from my children with great longing after 3 months, also a photograph of Willi(?) with the sweet child — [may it live] to a hundred years) — "Fategrafie" (Fotografie), "Afidawid" (affidavit) are phonetic spellings; "bis Hundert Jahr" is the traditional Jewish birthday blessing, natural here.
- Finding: The content is family news + emigration logistics (examination appointments 20 April, missing affidavit, mail gaps). No money amounts, no routes, no euphemisms for deportation, no message designed to fool a censor beyond ordinary discretion. "Rojse" [uncertain] is the one unidentified person worth flagging as a lead. The multi-author, multi-direction layout is space-maximizing on a folded sheet, not steganography.
- Confidence: high on Josef's portion; medium on Ruchalen's (faint, with [unclear] passages per HH).

### ii) Lighter words
- Method: compared ink weight across the sheet at full page and in crops.
- Observations: Ruchalen's ENTIRE contribution (bottom half, vertical columns, top-edge continuation) is written in a markedly lighter, blue-grey ink than Josef's brown ink — a different pen/ink, consistent across her whole text. Within Josef's text the ink is uniform; within Ruchalen's it is uniformly faint. No single word is selectively lightened within either author's text.
- Finding: the lightness differential is authorship-related (two writers, two pens), not a within-text code. Nothing found. Confidence: high.

### iii) Subtle markings
- Method: inspected Josef's text in crops, the fold area, and Ruchalen's columns.
- Observations: (1) One deletion in Ruchalen's text (per transcript: "warum hat die Bertha kein grus zu geschrieben [deletion]") — unresolvable at this resolution. (2) An irregular dark ink blot with a satellite spot at the left edge where Ruchalen's letter begins — accidental spill morphology, obscures nothing critical. (3) No underlines, dots, circles, carets, or margin ticks in Josef's text. (4) The fold-note across the central fold is in a smaller, darker hand — an editorial/explanatory note, per HH.
- Finding: nothing indicating a marking code. The blot is accidental; the deletion is an ordinary correction. Confidence: medium-high.

### iv) Word skips / layout
- Method: traced all text orientations on the sheet.
- Observations: Josef: two normal columns (right then left). Ruchalen: vertical columns at 90° rotation plus an upside-down continuation along the top edge; the fold-note squeezed across the central fold between the two halves; text blurred along the fold lines (noted by HH as limiting legibility). No skipped words, no squeezed insertions, no cross-out-and-rewrite beyond the single deletion.
- Finding: the multi-directional layout is a space-saving practice on a small folded sheet, fully explained by the second author using leftover space. Nothing found. Confidence: high.

### v) Anagram-like / transposed words
- Method: scripted strict permutation scan; manual name-spelling check.
- Observations: the only permutation pair is "als"/"las" — both ordinary German words in normal use, not significant. Inconsistent spellings: Bertha/Berta, Ruche Lea/Ruchel Lea/Ruchalen, Wielen/Willi, Chawze (Chava), Fategrafie, Afidawid, senene — all consistent with Ruchalen's phonetic/Yiddish-influenced orthography, not transposition play. Josef's spelling is consistent.
- Finding: nothing found. Confidence: high.

### vi) Jewish religious code patterns
- Method: scanned for Hebrew phrases, blessings, holidays, liturgical quotes; checked HH footnotes (none identify quotes).
- Observations: "lustigen Pesach" (timely Passover greeting); Ruchalen's "bis Hundert Jahr" blessing and Hebrew/Yiddish closing fragment. All are natural, context-appropriate Jewish formulae.
- Finding: no placed/liturgical signaling; no gezeirah shava pairs; no gematria (the 10^14 kisses are hyperbole). Nothing found. Confidence: high.

### vii) Cryptography / known techniques
- Method: sentence-initials (Josef's letter): WEBBWWBWWDIVBBB; last letters: RRTDAENRRANHHRN; Ruchalen's sentence-initials: L-E-I-b-b; per-sentence word-initial strings checked; looked for null patterns, book-cipher references, diagonal reads, deliberate misspellings.
- Observations: no sequence spells a word or name; the misspellings are phonetic/dialectal and unsystematic; the only other-message references are Regina's postcard and Berta's letter (ordinary). The multi-orientation layout was checked for a directional read (e.g., reading the vertical columns as an acrostic) — the columns are continuous prose, not word stacks.
- Finding: nothing found. Confidence: high.

### viii) Historical comparison
- Method: compared against the censorship-euphemism and jargon-code conventions.
- Observations: April 1940, pre-deportation; the letter concerns legal emigration steps (examinations, affidavit). No "emigrated/resettled" euphemisms, no forced-cheer formulas. The sheet shows no censor stamps (it presumably traveled in an envelope).
- Finding: no censorship-evasion motive is visible in the text; nothing found. Confidence: high.

Per-letter verdict: No hidden message. A two-author family letter (Josef + Ruchalen) whose forensic interest is purely material: two inks, multi-directional space-filling layout, one deletion, one accidental ink blot, and a fold-note. Content value is as primary-source pointers (20 April 1940 examination appointments; Bertha's missing affidavit; the unidentified "Rojse").

---

## Letter 25 — undated (content: "seit den 1ten Juni", "schon 2 mal geschrieben", "fast 3 Monate kein Schreiben"; HH: written twice since 1st June, no post for 3 months, no word from Mali since departure), Josef Bermann to Ewa Bermann; German; 2 PDF pages

Transcript + translation + 1 HH footnote ("Reichsgau Upper Danube, an administrative district of Austria under Nazi rule") read in full. Scan page 1: letter front, blue-grey ink, penciled "1820–2622" in the upper-left corner, several dark ink spots/splatter mid-page. Scan page 2: continuation; printed vertical "146" at the bottom-right edge (my reading — looks like a pre-printed sheet number); scattered tiny ink specks across the page.

### i) Visible text
- Method: close reading of transcript + translation against the image.
- Observations:
  - "Teile Euch mit daß bin auf Arbeit in Oberdonau es geht mir Gott sei dank sehr gut habe genug zu essen verdiene auch für ganzes Auskommen" (I inform you that I am on work-duty in Upper Danube; I am doing very well, thank God, have enough to eat, and earn my full livelihood) — a work claim ("verdiene", earning) tied to a named place (Reichsgau Oberdonau). The "es geht mir… sehr gut / habe genug zu essen" phrasing is the conventional reassurance formula; whether the labor deployment was voluntary or forced cannot be determined from this letter, but the posting itself is a fact likely to produce primary sources (labor-deployment records, ~mid-1940).
  - "habe schon 2 mal geschrieben habe" / "seit den 1ten Juni" / "schon fast 3 Monate kein Schreiben" (I have already written twice; since 1 June; already almost 3 months with no letter) — mail-gap accounting; references to two earlier (evidently undelivered or unanswered) letters.
  - "von der liebe Mali habe seitden du weggefahren bist kein einziges Schreiben" (from dear Mali I have not had a single letter since you [Ewa] left) — establishes that Mali (Josef and Ewa's daughter) is NOT in Vienna with Josef; she is elsewhere (America), distinct from Chaja's Mali in letter 23.
  - "Hast Du liebe Eva für meine Ausreise was unternommen" (Have you, dear Eva, done anything about my emigration) — direct emigration ask.
  - "zur Mali ich soll hinkommen besteht vorlaüfig für keine Moglichkeit vielleicht wird sich spater ergeben ob ich zur Mali werde fahren konnen" (as for joining Mali, there is for now no possibility; perhaps later it will become clear whether I can travel to Mali) — "keine Möglichkeit" stated plainly; no euphemism.
  - "Bitte wanes Dir moglich ist per Flugpost zu schreiben damit ich soll nicht so lange warten" (Please, if it is possible for you, write by airmail so I don't have to wait so long) — airmail request, consistent with the mail gaps.
  - Penciled "1820–2622" (upper-left corner, page 1) and printed "146" (bottom-right edge, page 2) — numbers of unknown origin; the "146" appears typeset, likely a pre-printed stationery sheet number.
- Finding: The letter's intelligence value is as a dated labor-posting record (Oberdonau, post-1-June, pre-autumn 1940) and a mail-gap record. No money amounts, no routes beyond the airmail request, no euphemisms, no odd repetitions, no non sequiturs. The cheerful formula is conventional and not, on textual evidence alone, a forced-deception signal (contrast with the 1942-44 camp Briefaktion context, which postdates this letter).
- Confidence: high on the reading; medium on the forced-vs-voluntary labor question (text alone does not decide it).

### ii) Lighter words
- Method: compared ink weight word by word on page 1 at full page and in a top-region crop.
- Observations: The ink cycles between darker blue and faded grey-blue: the salutation "An meine Lieben" and the word "Euch" in "Teile Euch mit" are in distinctly darker blue ink than the surrounding faded text; later "1ten Juni" and "keine" ("habe keine Nachricht") are also darker. Each darker passage is followed by gradual fading. On page 2 the first lines ("zur Mali ich soll hinkommen…") are brownish-dark, fading to grey-blue below.
- Finding: the pattern is consistent with a fountain pen freshly re-inked (or re-dipped) at intervals — dark right after inking, fading as the nib runs dry — not with word-selective emphasis. The darker words ("Euch", "1ten Juni", "keine") form no message. Nothing found. Confidence: medium-high.

### iii) Subtle markings
- Method: inspected both pages at full page and crops.
- Observations: (1) A prominent black ink blot mid-page 1 (over "kein einziges Schreiben") with satellite spatter, plus smaller dark spots (e.g., on "2 mal") and scattered tiny specks across page 2 — all with accidental-spill morphology. (2) No underlines, circles, dots, ticks, or corrections. (3) The printed "146" and penciled "1820–2622" as noted in (i).
- Finding: the blots/specks are pen-spatter accidents, not marks. Nothing found. Confidence: medium-high.

### iv) Word skips / layout
- Method: traced text flow on both pages.
- Observations: regular lines, text running to the page edges; no insertions, cross-outs, margin cramming, or orientation changes. The letter is undated and unsigned with "Josef" only in the closing ("von euer Josef").
- Finding: nothing found. Confidence: high.

### v) Anagram-like / transposed words
- Method: scripted strict permutation scan; manual name-spelling check.
- Observations: no permutation pairs. Spellings: "vorlaüfig" (vorläufig), "Moglichkeit", "Flugpost" — consistent phonetic/dialectal forms; names spelled consistently.
- Finding: nothing found. Confidence: high.

### vi) Jewish religious code patterns
- Method: scanned for Hebrew phrases, blessings, holidays, liturgical quotes; checked the HH footnote.
- Observations: "Gott sei Dank" is a standard idiom, not a placed quote. No Hebrew, no holidays, no blessings.
- Finding: nothing found. Confidence: high.

### vii) Cryptography / known techniques
- Method: sentence-initials AHBHWWBW; sentence-final letters INNNTTNE; per-sentence word-initial strings; checked for null patterns, book-cipher references, deliberate misspellings, diagonal reads.
- Observations: no initials sequence forms a word or name; the message-about-message content is limited to the two earlier letters and the mail gap (ordinary). No systematic misspellings.
- Finding: nothing found. Confidence: high.

### viii) Historical comparison
- Method: compared against the euphemism and forced-letter conventions.
- Observations: The letter predates the deportation period and the camp Briefaktion system (1942-44). Its cheerful formula ("es geht mir Gott sei Dank sehr gut") matches ordinary family reassurance of the period; there is no textual marker of coercion. The "auf Arbeit in Oberdonau" posting is stated openly.
- Finding: no coded layer indicated. Nothing found. Confidence: high.

Per-letter verdict: No hidden message. A plain reassurance-and-logistics letter whose forensic notes are material only (ink-density cycling from pen re-inking; accidental ink spatter; penciled "1820–2622"; printed sheet number "146"). Its research value is the dated Oberdonau labor posting and the mail-gap record (two letters since 1 June, ~3 months without word).

---

## Cross-letter notes

1. Two Malis: letters 23 and 25 together disambiguate two different Malis — Chaja Willner's daughter Mali, in Vienna in August 1940, badgering to emigrate ("meine Mali sekiert mich sehr oft wan werden wir schon nach U.S.A. fahren", letter 23); and Josef and Ewa's daughter Mali, already out of Vienna/Austria before Ewa's departure, from whom Josef has had no letter (letter 25: "von der liebe Mali habe seitden du weggefahren bist kein einziges Schreiben"). Any downstream analysis must not conflate them.
2. Recipient-name thread at 94 Sheriff St: "Frau Ewa Berman" (23), "Ewa Bermann" (24, 25), "Mrs Berman" (21), "M. E. Berman" (22), "Miss Malka Berman" (20). The Malka/M.E. forms are a genealogical identity lead (possibly Ewa's Jewish name), not a code observation; privacy caveat applies.
3. Penciled numbers appear on three items — "2511-1399a" (23), "n 1521" (22), "1820–2622" (25) — in similar hand/placement style, origin undetermined (family filing vs. postal processing). Worth one consolidated check by the coordinating team, not per-letter code-breaking.
4. Shared emigration vocabulary ("Untersuchung", affidavit/Afidawid, Schiffskarten/Lisabon, Flugpost) across 23-25 is the plain working language of 1940 Vienna emigration efforts, not jargon code: it is used openly in a demonstrably censored postcard (23, Wehrmacht "Geprüft" stamp), which is evidence AGAINST a hidden layer — a censor read and passed it.
5. Yiddish openness: letters 21 and 22 use Yiddish openly on US domestic postcards (1943, 1944) — consistent with Yiddish as family vernacular rather than cover, and with no censorship motive on those routes.

## Gaps and limits (honest)

- Letters 21 and 22: no transcript or translation exists; I cannot read handwritten Yiddish cursive reliably, and tesseract has no Yiddish/Hebrew traineddata installed, so no OCR was possible. Content-level findings for these two are not available from me; a Yiddish reader should transcribe them.
- Letter 24's Ruchalen section: partly [unclear] per HH even after rescan; one deletion unresolvable at 170 dpi.
- Letter 20: my transcription is my own (no official transcript exists); handwriting is clear and confidence is high, but it is not Helen Hunter-verified.

## Crop requests

1. Letter 20, PDF p.2 (message side), anchor "for East 4th St. which is the eastern section of the st." — crop the left margin from "At Lakewood ask directions" through "I will meet you at the station", showing the curved bracket stroke and the vertical margin strokes. Illustrates: family iii (subtle markings, unknown authorship).
2. Letter 20, PDF p.2, anchor "4/23/52" — crop the top-right corner showing the lighter date hand vs. the body ink. Illustrates: family ii (lighter words / second hand).
3. Letter 22, PDF p.2 (message side), anchor the top line beginning "9/8" — crop the top-right quadrant showing the cluster of ~7 vertical grey strokes over lines 2-3. Illustrates: family iii (unexplained tally-like marks).
4. Letter 22, PDF p.2, anchor mid-card text lines — crop the central-right area showing the second cluster of ~7 vertical grey strokes. Illustrates: family iii (same).
5. Letter 22, PDF p.1 (address side), anchor the right edge near the stamp — crop the vertical blue-ink "n 1521" notation. Illustrates: family i (penciled numbers).
6. Letter 24, PDF p.1, anchor "beste Gruße Ruchalen" / lower half — crop the lower half showing Ruchalen's faint blue-grey vertical columns against Josef's brown ink, including the ink blot at the left edge. Illustrates: families ii + iii + iv (two inks, blot, multi-orientation layout).
7. Letter 24, PDF p.1, anchor the central horizontal fold — crop the fold band showing the small dark hand note ("…Schon for der Zeit was hat zu dir zu geschrieben"). Illustrates: family iv (fold-note insertion).
8. Letter 25, PDF p.1, anchor "Teile Euch mit daß bin auf" — crop the top region showing darker-blue "An meine Lieben"/"Euch" against faded surrounding ink. Illustrates: family ii (ink-density cycling, assessed as pen re-inking).
9. Letter 25, PDF p.1, anchor the upper-left corner — crop the penciled "1820–2622". Illustrates: family i (penciled numbers).
10. Letter 25, PDF p.2, anchor the bottom-right edge — crop the printed vertical "146". Illustrates: family iii (sheet/stationery number).
11. Letter 23, PDF p.1 (address side), anchor "Taborstrasse 67/14" — crop showing the purple "1517" stamp, the boxed stamp over the street line, and the faint penciled "2511-1399a" along the lower edge. Illustrates: families i + iii (stamps and penciled number).
12. Letter 23, PDF p.2 (message side), anchor "Wien den 13/8 40" — crop the top showing the underlined "40" and the dark smudge at the top-right corner. Illustrates: family iii (emphasis marks).

## Bottom line

No hidden or coded messages found in any of the six letters. Letters 23, 24, and 25 are plain 1940 emigration-logistics correspondence (one of them demonstrably passed Wehrmacht censorship); their value is as primary-source pointers (US consul contact ~May 1940, 20 April 1940 examination appointments, Bertha's missing affidavit, the Oberdonau labor posting, the unidentified "Rojse", two distinct Malis). Letters 20, 21, 22 are post-war US domestic postcards with no censorship motive; 20 is a mundane 1952 directions card (with unexplained margin strokes), and 21/22 are Yiddish cards I could not transcribe — letter 22 carries the batch's one genuinely unexplained feature (two clusters of ~7 tally-like strokes over the text). All mechanical checks (initials, final letters, word-initials, anagram scan) were run and came back negative.

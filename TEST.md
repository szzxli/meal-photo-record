# Deploy test report — GitHub Pages static PWA, NOT published

Status: built in `deploy/` only, index.html at root, ready to push to GitHub
Pages. NOT published, NOT pushed, NOT sent to the user. No live-browser
click test was done by this subagent (generic subagents have no live
browser); the parent must do that before any link is given.

## Files
- `index.html` — app, mobile bottom nav (Record / Trend / Pre-visit /
  Bowls), desktop wide layout, camera capture input, localStorage records
- `manifest.webmanifest` — name 家庭餐食拍照记录, short_name 餐食记录,
  display standalone, theme #2f6f4e, start_url ".", scope "."
- `sw.js` — caches app shell only, relative paths for a GitHub Pages
  subpath, no external requests
- `icons/icon-192.png` (192×192), `icons/icon-512.png` (512×512),
  `icons/icon-maskable-512.png` (512×512), `icons/apple-touch-icon.png`
  (180×180) — real PNG files, sizes verified with PIL
- `calculator.py`, `test_deploy.py` — range math, same constants as JS
- `.nojekyll`

## Checks run
- `node --check` on extracted index.html JS: PASS
- `node --check` on sw.js: PASS
- `python3 test_deploy.py`: 30/30 individual range checks hit, 10/10 cases
  all-hit (see below). This is interval-propagation only: specific
  versions use the same generic bases as the intervals, so it does NOT
  prove a real kitchen matches, and no range was narrowed on n=1.
- No external http(s) URLs in index.html: 0 found
- No personal-health fields in index.html: 0 found after edit
- Manifest JSON parses; sw.js parses

## Exact numbers verified (Python, same constants as JS)
Chinese, whole-pot x share:
- Tomato-egg Omnivore 1/3: kcal 156.5–305.2 vs 211.1; fat 12.6–23.1 vs
  15.2; sodium 440.3–857.9 vs 843.3 (near upper edge, 14.6 mg margin)
- Tomato-egg second 1/4: kcal 117.4–228.9 vs 182.4; fat 9.4–17.3 vs
  15.2; sodium 330.3–643.4 vs 338.7
- Mapo video 1/4 (doubanjiang sodium = 1000 mg midpoint assumption, not
  a brand value): kcal 190.2–271.2 vs 199.9; fat 15.5–20.9 vs 16.0;
  sodium 365.8–774.1 vs 492.0
- Mapo second 1/4: kcal 190.2–271.2 vs 250.7; fat 15.5–20.9 vs 20.0;
  sodium 365.8–774.1 vs 647.0
- Cold cucumber 1/2: kcal 85.0–101.0 vs 95.0; fat 7.1–7.1 vs 7.1
  (artificially narrow: oil fixed at 1 tbsp in the recipe); sodium
  563.2–776.3 vs 564.0
- Cold cucumber + soy 1/2: sodium 563.2–776.3 vs 775.5 (other two same)

Western, plate area x coverage x thickness x density band 0.8–1.1 g/ml
(assumption, estimated grams, not weighed), salt added separately:
- Chicken, 20 cm plate / 50% / 1.5 cm / 0 g salt: volume 235.6 ml,
  grams 188.5–259.2 vs specific 220.0 in band; kcal 292.2–453.6 vs
  363.0; fat 5.7–11.7 vs 7.9; sodium 113.1–233.3 vs 162.8
- Salmon, same plate / 1 g salt: grams 188.5–259.2 vs 220.0 in band;
  kcal 358.1–570.2 vs 457.6; fat 20.7–38.9 vs 28.6; sodium 487.2–574.4
  vs 522.8
- Pasta tomato, 25 cm / 50% / 2.0 cm / 0.5 g salt: volume 490.9 ml,
  grams 392.7–540.0 vs 400.0 in band; kcal 353.4–701.9 vs 440.0;
  fat 3.9–10.8 vs 6.0; sodium 216.1–1006.4 vs 516.5 (very wide: sauce
  sodium base interval 5–150 mg/100 g)
- Brown rice, 25 cm / 33% / 2.0 cm / 0 g salt: volume 324.0 ml,
  grams 259.2–356.4 vs specific 250.0 — GRAMS MISS (see below);
  kcal 285.1–445.5 vs 295.0; fat 2.1–3.6 vs 2.2; sodium 2.6–17.8 vs 7.5

Bowls, volume only, never nutrition:
- Tiger 11 cm / 5.5 cm, bottom 6–8 cm: 321–393 ml
- Leaf 20 cm / 5–6 cm, bottom 9–14 cm assumed: 865–1376 ml
- Beaded 21 cm / 8 cm, bottom 10–15 cm assumed: 1573–2055 ml
- Shallow plate 25 cm: area 490.9 sq cm, plate method only

## Honest misses / limits (do not hide)
1. Brown-rice grams miss: specific 250 g is below the density-band
   grams 259.2–356.4 ml for that plate/coverage/thickness pairing
   (density 0.77 g/ml, below the 0.8 band floor). Nutrition still hit
   only because the ranges are wide. The density band is not universal
   for low-density foods; the band was NOT changed after seeing this,
   and the UI labels grams as estimated, not weighed.
2. Tomato-egg sodium case 1 is 14.6 mg from the upper bound; a little
   more salt would miss.
3. Mapo sodium width is driven by the doubanjiang 500–1500 mg
   assumption; its test value is the 1000 mg midpoint, not a brand value.
4. Cold-cucumber fat width is artificially narrow (oil fixed at 1 tbsp).
5. Pasta-tomato sodium width is very wide (216.1–1006.4 mg) because the
   sauce sodium base interval is wide.
6. No live-browser click test, no real-device camera/install test, no
   service-worker offline end-to-end test was done in this task.
   Parent must: push to GitHub Pages, open the live URL in a real
   browser, click Record / Trend / Pre-visit / Bowls, save a record,
   reload, check localStorage persistence, check manifest/install and
   offline reopen, before giving any link to the user.
7. Photo is record only in this build; there is no dish/portion
   recognition, by design.

## Generic mode — added 2026-10-30 (local deploy/ only, NOT pushed, NOT live)
New "通用记一碗" line on the Record page, added only; all 7 named dishes,
their ranges, and PWA files are unchanged (named-dish check still 30/30,
re-run above). Free-text dish name is a label only and does NOT change the
calculation. Inputs: main-ingredient group (10 groups), method (6, grouping
label only — it adds NO hidden oil/salt, to avoid double counting; oil and
salt/sauce levels carry the cooking difference), oil band, salt/sauce band
(soy unknown cluster 36.0–56.4 mg/ml, salt 393 mg/g), bowl gram band
(small 150–250 g, medium 200–350 g, large 300–500 g, estimated, not weighed).
Formula: per-100g group base interval x bowl grams band + oil band + salt/
soy band. Output only three ranges; sodium only vs FDA 2300 mg generic
reference, labelled non-personal, non-medical. Every generic result is
labelled "通用组区间，未按具体菜验证，范围更宽". Generic records use the
same localStorage records and flow into Trend and Pre-visit summary like
named records, with the free-text name shown and a [通用] tag. Photo is
still record only, no recognition, no upload, no external requests
(0 http(s) URLs in index.html, re-checked). Checks: node --check on
extracted index.html JS PASS, sw.js PASS, and JS generic() run in node
matches the Python numbers below exactly (to rounding).

Generic examples verified (Python test_generic.py + node generic()):
- Stir-fry pork, regular oil, regular salt, medium bowl 200–350 g:
  kcal 461.9–1103.8; fat 35.0–91.0 g; sodium 496.5–1750.5 mg
  (22–76% of FDA 2300 mg generic ref)
- Steamed fish, low oil, light salt, small bowl 150–250 g:
  kcal 191.5–461.9; fat 6.0–22.0 g; sodium 120.0–853.5 mg (5–37%)
- Cold-mixed vegetable (mixed_veg), low oil, light salt, medium bowl:
  kcal 86.5–271.9; fat 4.0–14.0 g; sodium 30.0–618.5 mg (1–27%)
- Extra propagation guards, same formula, all lo <= hi:
  braised pork, heavy oil, heavy salt, large bowl 300–500 g:
  kcal 723.8–1621.0; fat 56.0–135.0 g; sodium 1309.5–3321.0 mg (57–144%)
  steamed leafy vegetable, low oil, light salt, small bowl:
  kcal 56.5–161.9; fat 3.3–9.5 g; sodium 15.0–553.5 mg (1–24%)

Honest limits of this generic section (do not hide):
1. Group bases are generic assumptions per 100 g, NOT measured values for
   any specific dish. A passing example does NOT validate the group, and
   a generic range must never be quoted as that dish's validated range.
2. Ranges are deliberately very wide (e.g. stir-fry pork kcal width
   ~642 kcal, braised pork sodium up to 3321 mg): that width is the cost
   of covering many dishes with one group, not precision.
3. Method adds no coefficient: a steamed dish with "heavy" oil selected
   will still get the heavy oil band, because the user, not the method
   label, supplies the oil level. Contradictory selections are possible
   and are not corrected by the tool.
4. Bowl gram bands are user-selected estimates, not weighed and not
   derived from the bowl-volume page; a wrong band shifts all three
   ranges proportionally.
5. No live-browser click test of the generic UI, no real-device test,
   no recognition test (recognition is still absent by design). Parent
   must push, open the live URL in a real browser, and click the generic
   line, save a generic record, check Trend/Pre-visit include it, and
   reload, before giving any link to the user.
6. No case failed to propagate: every generic range checked had lo <= hi,
   and JS and Python agree. The only near-boundary note is inherited from
   the named section, not generic: tomato-egg sodium 14.6 mg from its
   upper bound.

# Chrysalis 🦋 PhD positions, project jobs & internships for Megha Pashupati

**Live site:** https://astrophysicist-abhi26.github.io/chrysalis/ · **Android app:** the *Android app* button on the site

Every morning at 07:00 IST a GitHub Action reads ~50 public sources and keeps what suits Megha
(MSc Life Sciences, IISc Bengaluru; CSIR-UGC NET JRF):

| Tab | What it shows |
|---|---|
| **PhD positions** | Funded PhD posts and doctoral fellowships in Europe and India |
| **Project & JRF jobs** | Project assistant/associate, JRF and research-assistant roles that suit an MSc (her NET-JRF counts) |
| **Internships** | Three columns: **Bengaluru & India**, **Abroad**, **AI & biotech companies**, plus curated schemes flagged when only enrolled students can apply |
| **AI & biotech** | Every role and internship at AI-for-biology and biotech companies |
| **Programmes** | PhD programmes in Europe (IMPRS-BI, EMBL, IMPRS Ageing, FLI, ERIBA, CBMR, Karolinska …), PhD routes in India with her JRF (IISc, NCBS, inStem), and funding |
| **My tracker** | Her applications (saved → applied → interview → offer), notes, documents, calendar export |
| **Search elsewhere** | Ready-made LinkedIn / Google / Indeed searches from her profile |
| **Sources** | Health of every source, refreshed daily |

Postdoc and faculty posts are dropped (`scraper/site.yaml`). Topics added for her: *extracellular vesicles &
cell–cell communication*, *muscle biology & myogenesis*, *metabolism & mitochondria*, *stem cells*, *gene & cell
therapy*, *cell signalling* (plus ageing and senescence). Each posting is compared with her CV
(`scraper/cv/megha.txt`) and scored 0–100 per ranking profile (`scraper/profiles.yaml`); every card says why.

The look: a sunny garden with tiny butterflies by day, a firefly-lit garden by night, faint muscle cells,
vesicles and mitochondria in the background — all behind the content, and still for reduced-motion users.

## Make it yours

| To change … | edit |
|---|---|
| name, person, which position types are dropped | `scraper/site.yaml` |
| how positions are ranked (topics, regions, “near Bengaluru” bonus, PhD-required penalty) | `scraper/profiles.yaml` — or live in the site’s **Tune** panel |
| PhD programmes and internship schemes | `scraper/programmes.yaml` (only checked dates are shown) |
| job boards, institutes, companies | `scraper/sources.yaml`, `institutes.yaml`, `companies.yaml` (test with `python scraper/doctor.py`) |
| the avatar, icon and launcher icon | `tools/make_art.py`, then `python tools/make_art.py` |

## Run it locally

```bash
pip install -r requirements.txt
python scraper/scrape.py --offline --out docs/jobs.json   # fixtures, no network
python scraper/scrape.py --out docs/jobs.json             # live run
cd docs && python -m http.server 8000                     # open http://localhost:8000
python -m pytest -q                                       # 55 tests
```

Deploying from scratch: **[RUNBOOK.md](RUNBOOK.md)**. Everything is plain Python and plain JavaScript; there is no
database and no build step. Data comes only from public adverts and official job-board APIs, respecting robots.txt.

Built for Megha by her friend Abhishek. A chrysalis is where a butterfly gets ready to fly.

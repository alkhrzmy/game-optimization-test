# Task 3 — Data Analysis (Eklipse)

**Deliverables**
- `Task3_Data_Analysis_Eklipse.pptx` — 9-slide deck (metrics + justification + insights).
- `sql/01..05_*.sql` — five SQL queries, each JOINs ≥2 tables.
- `Task3_submission.zip` — the deck + the 5 .sql files (as the brief requires).

**Reproduce**
```bash
python build_database.py     # builds eklipse.db from the 5 CSVs
python run_queries.py        # runs all 5 .sql, prints + saves results/*.csv
python generate_task3_ppt.py # rebuilds the deck
```

## The 5 metrics & real results

| # | Metric | Tables joined | Result |
|---|--------|---------------|--------|
| 1 | Clip Utilization Funnel (CTT) | clips + downloaded_clips + shared_clips | 552,031 generated → **2.34%** downloaded, **0.54%** shared |
| 2 | Free → Premium Conversion | gamesession + premium | 333 / 4,322 = **7.7%** |
| 3 | Premium Engagement Lift | clips + premium | Premium **125.0** vs Free **120.6** clips/user (+3.6%) |
| 4 | Top Games by Clip Yield | gamesession + clips | Warzone 139,790 clips; LoL highest yield ~24.4/stream |
| 5 | Premium Churn vs Engagement | premium + clips | Churn **~32%**; churned **106.8** vs retained **134.7** clips/user |

## Why these metrics
- **Funnel** = core product health (are AI clips actually used?).
- **Conversion** = monetisation headline.
- **Engagement lift** = does premium = heavier usage? (validates value prop).
- **Top games** = where to invest per-game AI models & marketing.
- **Churn vs engagement** = retention + an actionable early-warning signal.

## Key takeaways
1. Biggest lever = clip utilization (tiny download/share rates on a huge base).
2. Premium isn't about *more* clips — it's about features; message accordingly.
3. Low early engagement precedes churn → trigger save-flows.

> Data note: 5 CSVs are SQL table exports. Joins verified (download↔clip 99.9%, clip↔gamesession 97.6%). `clip_type_id = 2` = converted-to-TikTok (CTT).

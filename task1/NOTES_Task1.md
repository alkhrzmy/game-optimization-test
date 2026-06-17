# Task 1 — Game Understanding (Delta Force)

**Deliverable:** `Task1_Game_Understanding_DeltaForce.pptx` (12 slides, 16:9). Upload ke Google Slides.

> Regenerate kapan saja: `~/.eklipse-venv/bin/python generate_task1_ppt.py`

## Game
- **Garena Delta Force** — Genre: **Tactical FPS** (hero-shooter, class-based Operators).
- Dua mode dianalisis: **Operations (Hazard Ops, extraction)** & **Warfare (large-scale)**.

## Prinsip deteksi (inti jawaban)
3 lapisan sinyal + **sensor fusion** (event hanya nge-trigger kalau ≥2 lapisan setuju → false positive rendah):
1. **UI/HUD** — template matching + OCR (kill feed, timer, banner OVERTIME, vehicle HUD, ikon ability).
2. **Audio** — kill-confirm, SFX/voice line ability, sting overtime, suara meriam tank.
3. **Scene/State** — masuk vehicle, last-alive, result screen, perubahan state objektif.

## 6 Event & ringkasan trigger
| # | Event | Mode | Trigger inti | Pre/Post | Durasi |
|---|-------|------|--------------|----------|--------|
| 1 | MandelBrick Contest & Decoding | Operations | decode bar/timer + combat dalam protection window | 8s/5s | 45–60s |
| 2 | Solo Squad Wipe | Operations | ≥3 kill oleh local player dalam ≤30s (1 squad) | 10s/5s | 25–40s |
| 3 | Tank Multi-Kill | Warfare | tank HUD aktif + ≥2–3 kill via ikon meriam dalam ~10–15s | 6s/4s | 20–35s |
| 4 | Operator Skill Combo | Warfare | ability/ult aktif → payoff (≥2 kill / objektif) dalam ~8s | 7s/5s | 20–35s |
| 5 | Clutch 1v4 | Both | semua teammate mati + player menang outnumbered ≥1v3/1v4 | 12s/6s | 30–50s |
| 6 | Clutch Overtime | Warfare | state OVERTIME + aksi penentu → match berakhir menang | 15s/8s | 35–55s |

## Penamaan clip
`DF_<MODE>_<EVENT>_<context>_<UTCtimestamp>_<user>.mp4`

## Talking point penting
- Overtime & 1v4 = "importance multiplier" → dikasih pre/post-roll lebih panjang.
- Semua threshold/window = parameter → bisa di-A/B test terhadap engagement creator.

> Sumber detail game (MandelBrick, mode, operator) diverifikasi dari Wikipedia & wiki/guide Delta Force. Beberapa konten diparafrase agar sesuai pemahaman sendiri.

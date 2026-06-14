# Reconstruction Plan

## First Principles

1. **Data is the product** — questions, answers, knowledge points are the value. Extract to `data.json`.
2. **Presentation is disposable** — CSS can be swapped without touching logic. Extract to `styles.css`.
3. **Engine is the glue** — JS in `index.html` loads data, renders UI, handles quiz logic.
4. **Spaced repetition is the multiplier** — SM-2 algorithm turns passive review into active learning.

## What Changed

| Action | File | Rationale |
|--------|------|-----------|
| CREATE | `data.json` | All questions, knowledge points, formulas, errors — pure data, no presentation |
| CREATE | `styles.css` | All visual styles, separated from logic |
| REWRITE | `index.html` | Clean architecture: data loader, SR engine, modular renderers |

## Architecture

```
data.json    ← single source of truth (120 single + 45 multi + 15 subj + 7 topics)
styles.css   ← presentation layer (dark theme, responsive)
index.html   ← engine layer (nav, quiz, SR, timer)
```

## Spaced Repetition (New Feature)

- SM-2 simplified algorithm
- Cards: new → learning → review
- Quality ratings: forgot (1) / remembered (3) / easy (5)
- Interval expansion: 1 day → 3 days → EF × previous
- Per-card EFactor tracking (min 1.3)
- localStorage persistence under `mayuan_sr_v1`

## Result

- Files: 3 (was 1)
- Separation of concerns: data / style / logic
- New feature: spaced repetition review mode
- All original functionality preserved

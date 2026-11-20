# The Global Ledger — Thursday 19 November 2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/Goatleaf12/makefun-news-image-1119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/Goatleaf12/makefun-news-image-1119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One image that sums up the world's news of **Thursday 19 November 2026**:
a newspaper front page with 36 stories — three illustrated leads, ten
illustrated grid stories, a world map with the thirteen illustrated
stories pinned on it, and twenty-three more stories in the ALSO THURSDAY
briefs column. Every story happened, or was first reported, on that
Thursday; a DATE CHECK line names the tempting story reframed because
its milestone fell on 18 November.

The front page leads on the first Trump–Xi–Putin three-way summit in
Shenzhen and its four-point peace declaration, the World Court's 9–6
ruling that Myanmar committed genocide against the Rohingya, and
Anthropic's record-breaking Nasdaq debut.

## How it works

- Every story scene is an original illustration generated for this
  edition (`scenes/s01.webp` … `scenes/s13.webp`) in one consistent
  editorial style — no text inside the art, so nothing can garble.
- `gen_v4.py` composes the page with PIL: it centre-crops each scene
  into its story cell and typesets everything else — masthead, region
  count bar (computed from the story data), day-in-numbers strip,
  headlines, full prose decks with sources (never truncated), the pin
  map, complete one-line ALSO briefs (headline + key fact + source),
  the DATE CHECK and the footer. It writes `entry.png` (1024×1024,
  deterministic: identical SHA-256 on every run).
- Measured gate for this edition: **80,111 unique colours** and
  **461,607 bytes** for the final render.
- `main.ts` is the submitted program: it copies the shipped `entry.png`
  to `$MAKEFUN_OUTPUT_DIR/entry.png` (or `/output/entry.png`). It runs
  offline and writes identical bytes on every run.
- Earlier editions of this page are kept in `gen.py` (code-painted
  scenes) and `gen_v3.py` (the first generated-scene edition) for the
  record. This v4 edition keeps the generated scenes and restores the
  earlier editions' full text depth, with 36 stories.

## Run it

```sh
python3 gen_v4.py     # regenerate entry.png (deterministic)
node main.ts          # writes /output/entry.png
```

## License

MIT — see `LICENSE`.

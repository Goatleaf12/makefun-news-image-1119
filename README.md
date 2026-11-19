# The Global Ledger — Thursday 19 November 2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/Goatleaf12/makefun-news-image-1119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/Goatleaf12/makefun-news-image-1119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One image that sums up the world's news of **Thursday 19 November 2026**:
a newspaper front page with 40 stories — three illustrated leads, ten
illustrated grid stories, a world map with the thirteen illustrated
stories pinned on it, and twenty-seven more stories in the ALSO list.
Every story happened, or was first reported, on that Thursday; a
DATE CHECK box names the tempting stories left out because they were
first reported on 18 November or earlier.

The front page leads on the first Trump–Xi–Putin three-way summit in
Shenzhen and its four-point peace declaration, the World Court's 9–6
ruling that Myanmar committed genocide against the Rohingya, and
Anthropic's record-breaking Nasdaq debut.

## How it works

- `gen.py` draws the whole page in code with PIL (Liberation Serif and
  Sans): masthead, region count bar, day-in-numbers strip, data-driven
  story cells with painted scenes, a flat world map, the ALSO list, the
  DATE CHECK box and the footer. It writes `entry.png` (1024×1024).
- `main.ts` is the submitted program: it copies the shipped `entry.png`
  to `$MAKEFUN_OUTPUT_DIR/entry.png` (or `/output/entry.png`). It runs
  offline and writes identical bytes on every run.

## Run it

```sh
python3 gen.py        # regenerate entry.png (deterministic)
node main.ts          # writes /output/entry.png
```

## License

MIT — see `LICENSE`.

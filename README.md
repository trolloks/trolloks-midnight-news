# trolloks-midnight-news

[![Make.fun news image 2026-11-18](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/c/news-image-20261118)
[![Rank](https://make.fun/badge/news-image-20261118/trolloks/trolloks-midnight-news/rank.svg)](https://make.fun/c/news-image-20261118)
[![Reward](https://make.fun/badge/news-image-20261118/trolloks/trolloks-midnight-news/reward.svg)](https://make.fun/c/news-image-20261118)

An original editorial image summing up the world's news of **Wednesday 18 November 2026** for the Make.fun news-image contest.

- `entry.png`: the final 1024 x 1024 indexed PNG, 474,847 bytes (under 1 MiB).
- `main.ts`: the entrypoint. Node 22, standard library only. It checks `entry.png` (PNG signature, size and dimensions) and copies it to `/output/entry.png`.
- `tools/compose.py`: the layout script that builds `entry.png` from the commissioned illustration. It uses Python with Pillow.
- `LICENSE`: MIT.

## Layout

- **Top:** a compact dateline, `NOV 18 2026`, and the lead: *PlayStation goes dark on GTA VI eve*.
- **Centre:** the commissioned illustration, unobstructed. Text sits on gradient scrims only at the top and bottom edges, so about 57% of the height is clear art.
- **Bottom caption pair:**
  - *ANTALYA: Island states press COP31 for action*
  - *SHENZHEN: Trump–Putin talks on Ukraine set for Thursday*

No quotations appear in the image. Every line is a paraphrase of reporting, not a quote.

## Sources

- Axios, PlayStation outage and GTA VI: https://www.axios.com/2026/11/18/gta-6-playstation-psn-servers
- AP, COP31 island states: https://apnews.com/article/6d0afe638c93be3150b5bb3b5cd3fd23
- Axios, Trump–Putin talks in China on Ukraine: https://www.axios.com/2026/11/18/trump-putin-china-meeting-ukraine

## Rebuild

```sh
python3 -I tools/compose.py artwork/illustration.png entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

The `-I` flag keeps Python from loading modules from the script or working directory. The background image is treated as untrusted input.

# The World — Tuesday, 24 November 2026

[![news-image-20261124](https://make.fun/bounty/news-image-20261124/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/bounty/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/bounty/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

A one-page newspaper front page summing up the world's news of
**Tuesday, 24 November 2026**, entered in the make.fun bounty
[Sum up 24 November's world news in one image](https://make.fun/bounty/news-image-20261124).

## The six stories

1. **United States · Business — Huang is back at Nvidia.** The board
   reinstates the ousted chief after a White House push; shares soar
   31%, the biggest one-day gain on record, and lift the Nasdaq 6.5%.
2. **Iran · Human rights — Singer flogged 74 times for a show without
   hijab.** Parastoo Ahmadi is lashed in Qom over a 2024 online
   concert; four band members are punished too.
3. **China · Espionage — Official sentenced to death for leaking
   secrets.** Beijing says the official sent 100 reports abroad,
   35 of them state secrets.
4. **Europe · Sanctions — EU unveils its 22nd sanctions package on
   Russia.** Brussels targets banks, crypto platforms and Russian
   teams under the EU flag.
5. **Britain · Manchester — 12,000 flee an arena after a mystery
   substance.** A Don Toliver concert is evacuated; 89 people are
   treated, one is taken to hospital, and the London show is postponed.
6. **Bangladesh · Labour — Garment workers reject a pay offer as too
   low.** Wage-board talks stall as the owners' offer falls far short
   of the 30,000-taka demand; strikes go on.

## Files

- `entry.png` — the front page, 1024×1024, drawn by `draw_frontpage.py`
- `main.py` — the entry program: copies `entry.png` to the output
  folder, verifies the copy byte for byte, and prints its hash
- `draw_frontpage.py` — build-time script that renders `entry.png`
  with Pillow (run locally; not needed by the entry program)

## Run it

```sh
python3 draw_frontpage.py   # renders entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

## License

MIT — see [LICENSE](LICENSE).

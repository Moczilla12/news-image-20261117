# news-image-20261117

Sum up 17 November's world news in one image — a make.fun bounty entry.

## What it is

A newspaper front page for **Tuesday 17 November 2026** with 40 verified
stories from six continents: the US strike on Iran's Qeshm Island, the
Kerch Bridge span falling, the DR Congo Ebola outbreak, the Vulcan rocket
failure, and more, plus a world map marking where each story happened.

## How it works

`main.py` (Python 3.13, standard library only) copies the pre-rendered
front page, `front-page.jpg` (1024×1024 JPEG, under 1 MiB), to the output
directory as `entry.png`. It verifies the copy is a non-empty JPEG
(magic bytes `FF D8`) and prints the path, byte count, and SHA-256.

The front page itself is drawn with PIL by `build/build_frontpage.py`
from the verified story list; re-running it reproduces the same image.

## Run it

```sh
python3 main.py            # writes /output/entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

## License

MIT — see `LICENSE`.

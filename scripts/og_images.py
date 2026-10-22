#!/usr/bin/env python3
"""Tạo ảnh chia sẻ PNG 1200x630 cho từng bài (dist/og/<slug>.png) và ảnh mặc định (dist/og/default.png).

Cần Google Chrome (chạy ẩn) và mạng để tải phông Manrope. Ảnh đã sinh được commit cùng website,
nên chỉ cần chạy lại khi thêm bài hoặc đổi tiêu đề: python3 scripts/og_images.py
"""
import base64
import html
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build  # noqa: E402

ROOT = build.ROOT
OUT = build.DIST / "og"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
LOGO = "data:image/svg+xml;base64," + base64.b64encode((build.DIST / "assets" / "logo.svg").read_bytes()).decode()

TEMPLATE = """<!doctype html><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@500;700&family=Manrope:wght@800&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box}}body{{margin:0;width:1200px;height:630px;background:#e8eff9;font-family:'DM Sans',sans-serif;position:relative;overflow:hidden;color:#14202f}}
.c1{{position:absolute;width:760px;height:760px;border-radius:50%;background:#cfdcf2;right:-230px;top:-330px}}
.c2{{position:absolute;width:420px;height:420px;border-radius:50%;background:#dbe6f6;right:120px;bottom:-290px}}
.brand{{position:absolute;left:72px;top:60px;display:flex;align-items:center;gap:18px;font:800 38px Manrope,sans-serif;letter-spacing:-1.5px}}
.brand img{{width:68px;height:68px;border-radius:20px}}.brand b{{color:#2f6bd0;font-weight:800}}
.kicker{{position:absolute;left:72px;top:190px;font-size:24px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#2f6bd0}}
h1{{position:absolute;left:72px;top:236px;width:1000px;margin:0;font:800 {size}px/1.18 Manrope,sans-serif;letter-spacing:-.04em}}
.foot{{position:absolute;left:72px;bottom:56px;font-size:26px;font-weight:500;color:#4f6380}}
</style>
<div class="c1"></div><div class="c2"></div>
<div class="brand"><img src="{logo}"><span>aiagent<b>.vn</b></span></div>
<div class="kicker">{kicker}</div><h1>{title}</h1>
<div class="foot">{foot}</div>"""


def render(name, kicker, title, foot):
    size = 66 if len(title) <= 45 else 56 if len(title) <= 75 else 48
    page = TEMPLATE.format(size=size, logo=LOGO, kicker=html.escape(kicker), title=html.escape(title), foot=html.escape(foot))
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "og.html"
        src.write_text(page, encoding="utf-8")
        dest = OUT / f"{name}.png"
        subprocess.run(
            [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
             "--window-size=1200,630", "--virtual-time-budget=8000", f"--screenshot={dest}", f"file://{src}"],
            check=True, capture_output=True,
        )
    print("đã tạo", dest.relative_to(ROOT))


def main():
    OUT.mkdir(exist_ok=True)
    render("default", "Cổng kiến thức AI Agent", "Học, xây dựng và tự động hóa với AI Agent", "Hướng dẫn thực hành bằng tiếng Việt")
    for path in sorted(build.CONTENT.glob("*.html")):
        a = build.parse(path)
        render(a["slug"], a["category"], a["title"], f"{a['read']} phút đọc · aiagent.vn")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Sinh trang bài viết, trang chuyên mục, sitemap.xml và robots.txt từ content/*.html.

Chạy: python3 scripts/build.py
Mỗi file trong content/ gồm phần đầu dạng `khoá: giá trị`, một dòng trống, rồi thân bài HTML.
Khoá hỗ trợ: slug, title, description, category, keyword, published, updated, read, faq (lặp lại: `câu hỏi || trả lời`).
Thân bài dùng <h2 id="..."> để tự tạo mục lục.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
DIST = ROOT / "dist"
SITE = "https://aiagent.vn"
SITE_NAME = "AI Agent Việt Nam"
PHONE_LABEL = "Liên hệ Mr Phương · 0375 839 806"
ORDER = [
    "ai-agent-la-gi-khac-chatbot-the-nao",
    "cach-chon-cong-cu-xay-dung-ai-agent",
    "cach-tao-ai-agent-dau-tien-tu-a-den-z",
    "tu-dong-hoa-quy-trinh-cong-viec-bang-ai-agent",
    "huong-dan-tao-ai-agent-phan-loai-email-tu-dong",
    "khi-nao-nen-dung-ai-agent-cho-doanh-nghiep",
    "giao-thuc-mcp-ung-dung-doanh-nghiep",
    "json-prompt-la-gi",
    "9-prompt-bat-tu-duy-phan-bien",
    "huong-dan-su-dung-gamma-app-tao-bai-thuyet-trinh-tu-dong",
    "prompt-phuc-che-anh-cu-bang-chatgpt",
    "tu-hoc-ai-cho-nguoi-moi-bat-dau-tu-hoc-ai-trong-6-tuan",
]

e = html.escape


def parse(path):
    head, _, body = path.read_text(encoding="utf-8").partition("\n\n")
    meta = {"faq": []}
    for line in head.splitlines():
        key, _, value = line.partition(":")
        key, value = key.strip(), value.strip()
        if key == "faq":
            q, _, a = value.partition("||")
            meta["faq"].append((q.strip(), a.strip()))
        else:
            meta[key] = value
    meta["body"] = body.strip()
    return meta


def toc(body):
    items = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body)
    if not items:
        return ""
    lis = "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in items)
    return f'<nav class="toc" aria-label="Mục lục"><strong>Nội dung bài viết</strong><ol>{lis}</ol></nav>'


def faq_html(faq):
    if not faq:
        return ""
    rows = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in faq)
    return f'<section class="faq" aria-labelledby="faq-title"><h2 id="faq-title">Câu hỏi thường gặp</h2>{rows}</section>'


def head(title, description, url, og_type="website", extra=""):
    return f"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#0f2036">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
<link rel="canonical" href="{url}">
<meta property="og:locale" content="vi_VN">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/og.svg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/article.css">
{extra}</head>
"""


def chrome_top():
    return f"""<body>
<div class="topbar">Học AI Agent bằng tiếng Việt — <span>áp dụng vào công việc thật.</span></div>
<header class="wrap nav">
<a class="brand" href="/" aria-label="{SITE_NAME}, về trang chủ"><span class="brandmark"><img src="/assets/logo.svg" alt="" width="38" height="38"></span><span>aiagent<span style="color:#4a86e8">.vn</span></span></a>
<nav class="navlinks" aria-label="Điều hướng chính"><a href="/">Trang chủ</a><a href="/bai-viet/">Bài viết</a><a href="/#explore">Tài nguyên</a></nav>
</header>
"""


def chrome_bottom():
    return f"""<footer class="wrap footer"><div>© 2026 aiagent.vn · Cổng kiến thức AI Agent bằng tiếng Việt</div>
<nav aria-label="Điều hướng cuối trang"><a href="/">Trang chủ</a><a href="/bai-viet/">Tất cả bài viết</a><a href="tel:0375839806">{PHONE_LABEL}</a></nav></footer>
</body>
</html>
"""


def jsonld(*objs):
    return "".join(f'<script type="application/ld+json">{json.dumps(o, ensure_ascii=False)}</script>\n' for o in objs)


def article_page(a, all_articles):
    url = f"{SITE}/{a['slug']}/"
    crumbs = [("Trang chủ", f"{SITE}/"), ("Bài viết", f"{SITE}/bai-viet/"), (a["title"], url)]
    schema = [
        {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": a["title"],
            "description": a["description"],
            "inLanguage": "vi-VN",
            "datePublished": a["published"],
            "dateModified": a.get("updated", a["published"]),
            "mainEntityOfPage": url,
            "image": f"{SITE}/assets/og.svg",
            "keywords": a["keyword"],
            "author": {"@type": "Organization", "name": SITE_NAME, "url": SITE},
            "publisher": {"@type": "Organization", "name": SITE_NAME, "url": SITE},
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)
            ],
        },
    ]
    if a["faq"]:
        schema.append(
            {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": [
                    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}}
                    for q, ans in a["faq"]
                ],
            }
        )
    i = ORDER.index(a["slug"])
    related = [all_articles[ORDER[(i + k) % len(ORDER)]] for k in (1, 2, 3)]
    rel = "".join(
        f'<a href="/{r["slug"]}/"><small>{e(r["category"])}</small><strong>{e(r["title"])}</strong></a>' for r in related
    )
    return (
        head(f"{a['title']} | {SITE_NAME}", a["description"], url, "article", jsonld(*schema))
        + chrome_top()
        + f"""<main class="narrow">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Trang chủ</a> › <a href="/bai-viet/">Bài viết</a> › {e(a['category'])}</nav>
<header class="article-head"><span class="kicker">{e(a['category'])}</span><h1>{e(a['title'])}</h1>
<p class="lede">{e(a['description'])}</p>
<div class="meta"><span>Đăng ngày <time datetime="{a['published']}">{fmt_date(a['published'])}</time></span><span>Cập nhật <time datetime="{a.get('updated', a['published'])}">{fmt_date(a.get('updated', a['published']))}</time></span><span>{a['read']} phút đọc</span></div></header>
{toc(a['body'])}
<article class="prose">
{a['body']}
</article>
{faq_html(a['faq'])}
<aside class="related" aria-labelledby="related-title"><h2 id="related-title">Đọc tiếp</h2><div class="related-grid">{rel}</div></aside>
<section class="cta" aria-labelledby="cta-title"><h2 id="cta-title">Cần triển khai AI Agent cho công việc của bạn?</h2><p>Mô tả quy trình bạn muốn tự động hóa, chúng tôi sẽ giúp chọn hướng đi phù hợp và thử nghiệm với quy mô nhỏ trước.</p><a class="btn" href="tel:0375839806">{PHONE_LABEL}</a></section>
</main>
"""
        + chrome_bottom()
    )


def fmt_date(iso):
    y, m, d = iso.split("-")
    return f"{int(d)}/{int(m)}/{y}"


def index_page(all_articles):
    url = f"{SITE}/bai-viet/"
    title = f"Bài viết về AI Agent bằng tiếng Việt | {SITE_NAME}"
    desc = "Tổng hợp bài viết hướng dẫn AI Agent bằng tiếng Việt: khái niệm, cách chọn công cụ, cách tạo agent đầu tiên, tự động hóa quy trình và ứng dụng cho doanh nghiệp."
    cards = "".join(
        f'<a class="card" href="/{a["slug"]}/"><small>{e(a["category"])} · {a["read"]} phút đọc</small><h2>{e(a["title"])}</h2><p>{e(a["description"])}</p></a>'
        for a in (all_articles[s] for s in ORDER)
    )
    schema = [
        {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": "Bài viết về AI Agent",
            "url": url,
            "inLanguage": "vi-VN",
            "hasPart": [{"@type": "Article", "headline": all_articles[s]["title"], "url": f"{SITE}/{s}/"} for s in ORDER],
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Trang chủ", "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": "Bài viết", "item": url},
            ],
        },
    ]
    return (
        head(title, desc, url, "website", jsonld(*schema))
        + chrome_top()
        + f"""<main class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Trang chủ</a> › Bài viết</nav>
<header class="article-head"><span class="kicker">Thư viện</span><h1>Bài viết về AI Agent bằng tiếng Việt</h1><p class="lede" style="max-width:720px">Từ khái niệm nền tảng đến cách tự tay xây và triển khai agent trong công việc. Mỗi bài tập trung vào một câu hỏi cụ thể.</p></header>
<div class="index-grid">{cards}</div>
</main>
"""
        + chrome_bottom()
    )


def main():
    articles = {}
    for p in sorted(CONTENT.glob("*.html")):
        a = parse(p)
        articles[a["slug"]] = a
    missing = set(ORDER) ^ set(articles)
    if missing:
        raise SystemExit(f"ORDER và content/ không khớp: {sorted(missing)}")

    for a in articles.values():
        out = DIST / a["slug"]
        out.mkdir(parents=True, exist_ok=True)
        (out / "index.html").write_text(article_page(a, articles), encoding="utf-8")
    (DIST / "bai-viet").mkdir(exist_ok=True)
    (DIST / "bai-viet" / "index.html").write_text(index_page(articles), encoding="utf-8")

    urls = [(f"{SITE}/", "2026-10-22", "1.0"), (f"{SITE}/bai-viet/", "2026-10-22", "0.8")]
    urls += [(f"{SITE}/{s}/", articles[s].get("updated", articles[s]["published"]), "0.9") for s in ORDER]
    sm = "".join(
        f"<url><loc>{u}</loc><lastmod>{d}</lastmod><priority>{p}</priority></url>\n" for u, d, p in urls
    )
    (DIST / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sm}</urlset>\n',
        encoding="utf-8",
    )
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    print(f"Đã sinh {len(articles)} bài viết, trang chuyên mục, sitemap.xml, robots.txt")


if __name__ == "__main__":
    main()

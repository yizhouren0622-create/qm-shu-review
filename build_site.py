# -*- coding: utf-8 -*-
"""Build public static pages from local review HTML sources."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

NAV = """
<header class="site-top" id="siteTop">
  <div class="site-top-inner">
    <a class="site-brand" href="index.html">量子力学复习</a>
    <button type="button" class="site-menu-btn" aria-expanded="false" aria-controls="siteLinks">菜单</button>
    <nav class="site-links" id="siteLinks" aria-label="站点导航">
      <a href="index.html" data-page="index.html">首页</a>
      <a href="review.html" data-page="review.html">复习课</a>
      <a href="examples.html" data-page="examples.html">课件例题</a>
      <a href="exam.html" data-page="exam.html">综合卷</a>
      <a href="answers.html" data-page="answers.html">综合卷答案</a>
      <a href="exam-ch3.html" data-page="exam-ch3.html">第3章卷</a>
    </nav>
  </div>
</header>
"""

HEAD_EXTRA = """
<meta name="color-scheme" content="light">
<meta name="theme-color" content="#efeae2">
<link rel="stylesheet" href="assets/site.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.22/dist/katex.min.css" crossorigin="anonymous">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.22/katex.min.css" crossorigin="anonymous">
"""

FOOT_SCRIPTS = """
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.22/dist/katex.min.js" crossorigin="anonymous"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.22/dist/contrib/auto-render.min.js" crossorigin="anonymous"></script>
<script>
  window.addEventListener("error", function (e) {
    var t = e && e.target;
    if (!t || t.tagName !== "SCRIPT") return;
    if (String(t.src || "").indexOf("katex.min.js") === -1) return;
    var s1 = document.createElement("script");
    s1.src = "https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.22/katex.min.js";
    s1.defer = true;
    document.head.appendChild(s1);
    var s2 = document.createElement("script");
    s2.src = "https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.22/contrib/auto-render.min.js";
    s2.defer = true;
    document.head.appendChild(s2);
  }, true);
</script>
<script defer src="assets/site.js"></script>
"""

FOOTER = """
<footer class="site-footer">上海大学微电子 · 量子力学课件范围复习材料。公式需联网加载；离线时仍可阅读文字与图片。</footer>
"""


def strip_old_katex_and_scripts(html: str) -> str:
    html = re.sub(
        r'<link[^>]+katex[^>]*>\s*',
        "",
        html,
        flags=re.I,
    )
    html = re.sub(
        r'<script[^>]*katex[^>]*>.*?</script>\s*',
        "",
        html,
        flags=re.I | re.S,
    )
    html = re.sub(
        r'<script[^>]*auto-render[^>]*>.*?</script>\s*',
        "",
        html,
        flags=re.I | re.S,
    )
    # Remove inline renderMath bootstraps that duplicate site.js
    html = re.sub(
        r'<script>\s*document\.addEventListener\("DOMContentLoaded".*?</script>\s*',
        "",
        html,
        flags=re.S,
    )
    return html


def inject_chrome(html: str, title: str | None = None) -> str:
    html = strip_old_katex_and_scripts(html)
    if title:
        html = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", html, count=1, flags=re.S)

    # viewport already may exist — still add shared assets after charset/viewport block
    if "assets/site.css" not in html:
        if re.search(r'<meta[^>]+viewport', html, re.I):
            html = re.sub(
                r'(<meta[^>]+viewport[^>]*>)',
                r"\1\n" + HEAD_EXTRA,
                html,
                count=1,
                flags=re.I,
            )
        else:
            html = html.replace("<head>", "<head>\n" + HEAD_EXTRA, 1)

    # Remove duplicate viewport from HEAD_EXTRA if double — keep both ok or clean
    # Ensure body starts with nav
    if 'class="site-top"' not in html:
        html = re.sub(r"<body([^>]*)>", r"<body\1>\n" + NAV, html, count=1, flags=re.I)

    if "site-footer" not in html:
        html = re.sub(r"</body>", FOOTER + "\n" + FOOT_SCRIPTS + "\n</body>", html, count=1, flags=re.I)
    elif "assets/site.js" not in html:
        html = re.sub(r"</body>", FOOT_SCRIPTS + "\n</body>", html, count=1, flags=re.I)

    # Fix review page link to old knowledge梳理
    html = html.replace("../前三章知识梳理.html", "index.html")
    html = html.replace('href="模拟卷_答案.html"', 'href="answers.html"')
    html = html.replace('href="模拟卷.html"', 'href="exam.html"')
    return html


def build_hub() -> str:
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>量子力学复习站 · 上大微电子</title>
{HEAD_EXTRA}
</head>
<body>
{NAV}
<main class="hub">
  <div class="hub-card">
    <h1>量子力学前三章 · 复习站</h1>
    <p class="lead">上海大学微电子学院课程课件范围（Chapter 01–03）。手机、平板、电脑浏览器均可打开。</p>
    <div class="hub-grid">
      <a class="hub-link span2" href="review.html">
        <strong>复习课（带图精讲）</strong>
        <span>按考试顺序十二节，图文对照，适合系统复习。</span>
      </a>
      <a class="hub-link span2" href="examples.html">
        <strong>课件例题全解</strong>
        <span>按章节、知识点列出 PPT 里的例题和练习，每题都有概念、公式、思路和过程。</span>
      </a>
      <a class="hub-link" href="exam.html">
        <strong>综合模拟卷</strong>
        <span>前三章选择 / 填空 / 计算 / 简答，满分 100。AI 生成，不是官方试卷。</span>
      </a>
      <a class="hub-link" href="answers.html">
        <strong>综合卷答案</strong>
        <span>思路、公式、模式总结，中英对照。对应上面那份 AI 生成的综合卷。</span>
      </a>
      <a class="hub-link span2" href="exam-ch3.html">
        <strong>第3章力学算符卷</strong>
        <span>对易、厄米、测量、测不准。卷末附参考答案。AI 生成，优先级低于综合卷。</span>
      </a>
    </div>
    <div class="hub-note">
      建议：课件例题按知识点对照原题和全过程；综合卷做完再对答案。综合卷、第3章卷和答案都是 AI 生成的复习材料，不是课程官方试卷，请对照课件核对。公式排版需要联网（KaTeX）。本站只含课件范围内内容，不含固体物理。
    </div>
  </div>
</main>
{FOOTER}
{FOOT_SCRIPTS}
</body>
</html>
"""


def main() -> None:
    mapping = [
        ("review.source.html", "review.html", "量子力学复习课 · 上大微电子"),
        ("exam.source.html", "exam.html", "量子力学模拟卷 · 上大微电子"),
        ("answers.source.html", "answers.html", "模拟卷参考答案 · 上大微电子"),
        ("examples.source.html", "examples.html", "课件例题全解 · 上大微电子"),
        ("exam-ch3.source.html", "exam-ch3.html", "第3章力学算符模拟卷 · 上大微电子"),
    ]
    for src_name, out_name, title in mapping:
        src = ROOT / src_name
        text = src.read_text(encoding="utf-8")
        out = inject_chrome(text, title=title)
        (ROOT / out_name).write_text(out, encoding="utf-8")
        print("wrote", out_name, "bytes", len(out.encode("utf-8")))

    (ROOT / "index.html").write_text(build_hub(), encoding="utf-8")
    print("wrote index.html")

    # Remove noprint-only clutter is fine
    # .nojekyll for GitHub Pages
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")
    print("done")


if __name__ == "__main__":
    main()

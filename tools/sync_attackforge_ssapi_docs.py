#!/usr/bin/env python3
"""
Sync AttackForge Self-Service RESTful API (SSAPI) docs into a local repo folder.

Why this exists:
- The SSAPI docs are split across many GitBook pages.
- Page titles do NOT always match the URL slug (so you cannot guess URLs).
- This script crawls the SSAPI nav, extracts the real hrefs, downloads pages,
  and converts them to searchable Markdown for Codex to use locally.

Output structure:
  <out_dir>/
    manifest.json     # [{title,url,slug}, ...]
    urls.txt
    index.md
    raw_html/<slug>.html
    markdown/<slug>.md
"""

from __future__ import annotations

import argparse
import json
import os
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup  # type: ignore
from markdownify import markdownify as md  # type: ignore


@dataclass(frozen=True)
class Page:
    title: str
    url: str
    slug: str


def _slug_from_url(url: str) -> str:
    path = urlparse(url).path.rstrip("/")
    if not path:
        return "index"
    return path.split("/")[-1] or "index"


def _safe_filename(s: str) -> str:
    # Keep slugs stable, but sanitize just in case
    s = s.strip()
    s = re.sub(r"[^A-Za-z0-9._-]+", "_", s)
    return s[:120] if len(s) > 120 else s


def _extract_main_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    # GitBook layouts commonly use <main> or <article> for the content.
    main = soup.find("main")
    if main is not None:
        return str(main)

    article = soup.find("article")
    if article is not None:
        return str(article)

    # Fallback: whole doc
    return html


def _discover_ssapi_links(base_url: str, html: str) -> list[tuple[str, str]]:
    """
    Returns list of (title, absolute_url) discovered from nav/content.
    Filters to only the SSAPI section path.
    """
    origin = f"{urlparse(base_url).scheme}://{urlparse(base_url).netloc}"
    ssapi_prefix = "/attackforge-enterprise/modules/self-service-restful-api"

    soup = BeautifulSoup(html, "html.parser")

    found: list[tuple[str, str]] = []
    seen_urls: set[str] = set()

    for a in soup.find_all("a"):
        href = a.get("href")
        if not href:
            continue

        # GitBook uses relative hrefs frequently.
        abs_url = urljoin(origin, href)

        p = urlparse(abs_url)
        if not p.path.startswith(ssapi_prefix):
            continue

        # Exclude the SSAPI landing page itself unless you want it
        if p.path.rstrip("/") == ssapi_prefix.rstrip("/"):
            continue

        # Ignore fragment-only duplicates
        abs_url = abs_url.split("#", 1)[0]

        title = a.get_text(strip=True)
        if not title:
            continue

        # Drop obvious non-endpoint nav tokens
        if title.lower() in {"attackforge support", "modules"}:
            continue

        if abs_url in seen_urls:
            continue

        seen_urls.add(abs_url)
        found.append((title, abs_url))

    return found


def _http_get(session: requests.Session, url: str, timeout: int = 30) -> str:
    r = session.get(url, timeout=timeout)
    r.raise_for_status()
    return r.text


def _dedupe_slugs(pages: Iterable[Page]) -> list[Page]:
    used: dict[str, int] = {}
    out: list[Page] = []
    for p in pages:
        base = p.slug
        if base not in used:
            used[base] = 1
            out.append(p)
            continue
        used[base] += 1
        out.append(Page(title=p.title, url=p.url, slug=f"{base}__{used[base]}"))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--base-url",
        required=True,
        help="SSAPI section landing page URL (GitBook nav is crawled from here).",
    )
    ap.add_argument(
        "--out-dir",
        required=True,
        help="Output directory, e.g. docs/attackforge/ssapi",
    )
    ap.add_argument(
        "--sleep-seconds",
        type=float,
        default=0.4,
        help="Polite delay between page downloads to avoid rate limiting.",
    )
    ap.add_argument(
        "--refresh",
        action="store_true",
        help="Re-download pages even if they already exist on disk.",
    )
    ap.add_argument(
        "--max-pages",
        type=int,
        default=0,
        help="Optional cap for testing (0 means no limit).",
    )
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    raw_dir = out_dir / "raw_html"
    md_dir = out_dir / "markdown"
    raw_dir.mkdir(parents=True, exist_ok=True)
    md_dir.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "PyAttackForge-DocsSync/1.0 (+internal tooling)",
            "Accept": "text/html,application/xhtml+xml",
        }
    )

    print(f"==> Fetching base: {args.base_url}")
    base_html = _http_get(session, args.base_url)

    links = _discover_ssapi_links(args.base_url, base_html)
    if not links:
        raise SystemExit("No SSAPI links discovered. Site layout may have changed.")

    pages = [Page(title=t, url=u, slug=_safe_filename(_slug_from_url(u))) for t, u in links]
    pages = _dedupe_slugs(pages)

    if args.max_pages and args.max_pages > 0:
        pages = pages[: args.max_pages]

    # Write urls.txt
    urls_txt = out_dir / "urls.txt"
    urls_txt.write_text("\n".join([p.url for p in pages]) + "\n", encoding="utf-8")

    # Write manifest.json
    manifest = out_dir / "manifest.json"
    manifest.write_text(
        json.dumps([p.__dict__ for p in pages], indent=2, sort_keys=True),
        encoding="utf-8",
    )

    # Download pages and convert to markdown
    print(f"==> Discovered {len(pages)} pages. Downloading...")
    for i, p in enumerate(pages, start=1):
        raw_path = raw_dir / f"{p.slug}.html"
        md_path = md_dir / f"{p.slug}.md"

        if not args.refresh and raw_path.exists() and md_path.exists():
            print(f"[{i:03d}/{len(pages):03d}] SKIP {p.slug}")
            continue

        print(f"[{i:03d}/{len(pages):03d}] GET  {p.slug}  ({p.title})")
        html = _http_get(session, p.url)
        raw_path.write_text(html, encoding="utf-8")

        main_html = _extract_main_html(html)
        markdown = md(main_html, heading_style="ATX")

        # Add a small header for context
        markdown = f"# {p.title}\n\nSource: {p.url}\n\n---\n\n{markdown}\n"
        md_path.write_text(markdown, encoding="utf-8")

        time.sleep(max(args.sleep_seconds, 0.0))

    # Generate index.md
    index_path = out_dir / "index.md"
    lines = [
        "# AttackForge SSAPI Docs Cache",
        "",
        "This folder is auto-generated from the SSAPI docs navigation.",
        "Use `manifest.json` as the authoritative list of pages and slugs.",
        "",
        "## Pages",
        "",
    ]
    for p in pages:
        lines.append(f"- [{p.title}](markdown/{p.slug}.md)")
    lines.append("")

    index_path.write_text("\n".join(lines), encoding="utf-8")

    print("==> Done")
    print(f"   manifest: {manifest}")
    print(f"   index:    {index_path}")
    print(f"   markdown: {md_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


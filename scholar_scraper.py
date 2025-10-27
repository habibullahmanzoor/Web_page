
"""
scholar_scraper.py
------------------
Scrapes Google Scholar "All" metrics (Citations, h-index, i10-index).

Usage:
    from scholar_scraper import fetch_scholar_metrics
    metrics = fetch_scholar_metrics("https://scholar.google.com/citations?user=tKDhmdAAAAAJ&hl=en")
"""
from __future__ import annotations
import time
import json
from typing import Dict, Optional
from pathlib import Path

import requests
from bs4 import BeautifulSoup

CACHE_PATH = Path(__file__).with_name("scholar_metrics_cache.json")
CACHE_TTL_SECONDS = 60 * 60 * 12  # 12 hours


class ScholarBlocked(Exception):
    pass


def _load_cache() -> Optional[Dict]:
    if CACHE_PATH.exists():
        try:
            data = json.loads(CACHE_PATH.read_text())
            if time.time() - data.get("ts", 0) < CACHE_TTL_SECONDS:
                return data.get("metrics")
        except Exception:
            pass
    return None


def _save_cache(metrics: Dict) -> None:
    try:
        CACHE_PATH.write_text(json.dumps({"ts": time.time(), "metrics": metrics}, indent=2))
    except Exception:
        pass


def fetch_scholar_metrics(profile_url: str, timeout: int = 20, max_retries: int = 3) -> Dict[str, int]:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }

    cached = _load_cache()
    if cached:
        return cached

    last_exc = None
    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.get(profile_url, headers=headers, timeout=timeout)
            if resp.status_code != 200:
                raise ScholarBlocked(f"HTTP {resp.status_code} from Google Scholar")

            html = resp.text
            if "Our systems have detected unusual traffic" in html or "gs_captcha" in html:
                raise ScholarBlocked("Blocked by Google Scholar (CAPTCHA). Try later.")

            soup = BeautifulSoup(html, "html.parser")
            table = soup.find("table", id="gsc_rsb_st")
            if not table:
                raise ScholarBlocked("Metrics table not found (structure may have changed).")

            cells = table.select("td.gsc_rsb_std")
            if len(cells) < 5:
                raise ScholarBlocked("Unexpected metrics layout; not enough cells.")

            def to_int(text: str) -> int:
                return int(text.replace(",", "").strip())

            metrics = {
                "citations": to_int(cells[0].get_text()),
                "h_index": to_int(cells[2].get_text()),
                "i10_index": to_int(cells[4].get_text()),
            }
            _save_cache(metrics)
            return metrics

        except (requests.RequestException, ScholarBlocked) as e:
            last_exc = e
            time.sleep(1.5 * attempt)

    raise last_exc if last_exc else RuntimeError("Unknown error fetching Scholar metrics")



# --- Add to scholar_scraper.py ---
# --- Put this in scholar_scraper.py ---

from urllib.parse import urljoin, urlencode, urlparse, parse_qsl, urlunparse

def _url_with_pubdate(profile_url: str) -> str:
    """Return a Google Scholar profile URL with sortby=pubdate enforced."""
    u = urlparse(profile_url)
    q = dict(parse_qsl(u.query))
    q["sortby"] = "pubdate"         # force "Most recent"
    new_q = urlencode(q)
    return urlunparse((u.scheme, u.netloc, u.path, u.params, new_q, u.fragment))


def fetch_latest_publications(profile_url: str, count: int = 5) -> list[dict]:
    """
    Scrape the latest publications from a Google Scholar profile.
    Returns: [{'title','venue','authors','year','url'}]
    """
    import requests
    from bs4 import BeautifulSoup

    url = _url_with_pubdate(profile_url)
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
    }

    try:
        resp = requests.get(url, headers=headers, timeout=20)
        if resp.status_code != 200:
            return []
        html = resp.text
        if "unusual traffic" in html.lower() or "gs_captcha" in html:
            return []  # blocked

        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table", id="gsc_a_t")
        if not table:
            return []

        rows = table.select("tr.gsc_a_tr")[:count]
        pubs: list[dict] = []
        for r in rows:
            a = r.find("a", class_="gsc_a_at")
            title = a.get_text(strip=True) if a else ""
            href = urljoin("https://scholar.google.com", a["href"]) if a and a.has_attr("href") else ""

            gray = r.find_all("div", class_="gs_gray")
            authors = gray[0].get_text(" ", strip=True) if len(gray) > 0 else ""
            venue   = gray[1].get_text(" ", strip=True) if len(gray) > 1 else ""

            ycell = r.find("td", class_="gsc_a_y")
            year  = (ycell.find("span").get_text(strip=True) if ycell and ycell.find("span") else "")

            pubs.append({"title": title, "venue": venue, "authors": authors, "year": year, "url": href})
        return pubs
    except Exception:
        return []

# --- add in scholar_scraper.py ---
from urllib.parse import urljoin

def fetch_scholar_profile_photo(profile_url: str, timeout: int = 20, max_retries: int = 3) -> Optional[str]:
    """
    Return an absolute URL to the Scholar profile photo, or None if not found / blocked.
    We try a few selectors to be robust to minor Scholar changes.
    """
    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/124.0.0.0 Safari/537.36"),
        "Accept-Language": "en-US,en;q=0.9",
    }
    last_exc = None
    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.get(profile_url, headers=headers, timeout=timeout)
            if resp.status_code != 200:
                return None
            html = resp.text
            if "Our systems have detected unusual traffic" in html or "gs_captcha" in html:
                return None

            soup = BeautifulSoup(html, "html.parser")

            # 1) Try common <img> with id or class
            img = soup.find("img", id="gsc_prf_pup-img") or soup.find("img", class_="gsc_prf_pup")
            if img and img.get("src"):
                return urljoin("https://scholar.google.com", img["src"])

            # 2) Sometimes photo is in a DIV with background-image style
            div = soup.find(id="gsc_prf_pua") or soup.find("div", class_="gsc_prf_pua")
            if div and div.get("style"):
                # style="background-image:url('/citations/images/avatar_scholar_128.png')"
                style = div["style"]
                import re
                m = re.search(r"background-image\s*:\s*url\(['\"]?([^'\"\)]+)", style)
                if m:
                    return urljoin("https://scholar.google.com", m.group(1))

            return None
        except Exception as e:
            last_exc = e
    return None


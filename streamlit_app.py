# streamlit_app.py
from pathlib import Path
from typing import List, Dict, Optional, Union

import streamlit as st

from data import DATA
import scholar_scraper

# -----------------------------------------------------------------------------
# Paths & constants
# -----------------------------------------------------------------------------
APP_DIR = Path(__file__).resolve().parent
STATIC_DIR = APP_DIR / "static"

BIO_PATH = STATIC_DIR / "biography.txt"
PROFILE_IMG_PATH = STATIC_DIR / "habib.jpeg"
FALLBACK_AVATAR_URL = "https://via.placeholder.com/300x300.png?text=Profile"

SCHOLAR_URL = "https://scholar.google.com/citations?user=tKDhmdAAAAAJ&hl=en"

# -----------------------------------------------------------------------------
# Page config
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title=f"{DATA['name']} — Portfolio",
    page_icon="📄",
    layout="wide",
    menu_items={"Report a bug": None, "About": None},
)

# -----------------------------------------------------------------------------
# Helpers (robust image loading, caching)
# -----------------------------------------------------------------------------
@st.cache_data(ttl=60 * 60)  # 1 hour
def _read_image_bytes(p: Path) -> Optional[bytes]:
    """Read image bytes safely; return None on any failure."""
    try:
        return p.read_bytes()
    except Exception:
        return None

def get_profile_image_src() -> Union[bytes, str]:
    """
    Return bytes for the local image if it exists & is readable; otherwise a
    fallback URL. This prevents the app from crashing due to image issues.
    """
    data = _read_image_bytes(PROFILE_IMG_PATH)
    return data if data else FALLBACK_AVATAR_URL

@st.cache_data(ttl=3600, show_spinner=False)
def load_bio() -> str:
    try:
        return BIO_PATH.read_text(encoding="utf-8").strip()
    except Exception:
        return ""

@st.cache_data(ttl=60 * 60 * 12, show_spinner=False)
def get_metrics() -> Dict[str, int]:
    """Fetch Scholar metrics with caching; fallback to DATA metrics."""
    try:
        m = scholar_scraper.fetch_scholar_metrics(SCHOLAR_URL)
        return {**DATA.get("metrics", {}), **m}
    except Exception:
        return DATA.get("metrics", {})

@st.cache_data(ttl=60 * 60 * 12, show_spinner=False)
def get_latest_pubs(count: int = 5) -> List[Dict[str, Optional[str]]]:
    """Fetch latest publications with caching; fallback to static DATA list."""
    try:
        return scholar_scraper.fetch_latest_publications(SCHOLAR_URL, count=count)
    except Exception:
        pubs = sorted(DATA.get("publications", []), key=lambda p: p.get("year", 0), reverse=True)
        return [
            {"title": p["title"], "year": p.get("year"), "venue": p.get("venue", ""), "url": None, "authors": ""}
            for p in pubs[:count]
        ]

# -----------------------------------------------------------------------------
# Theme (Blue Academic)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
:root{
  --bg:#eaf2fb;--panel:#f8fbff;--text:#0b1a3f;--muted:#4b5563;--border:#cbdaf3;
  --chip:#e0edff;--brand:#2563eb;--brand-dark:#1e40af;--shadow:rgba(30,64,175,.12)
}
.block-container{max-width:1150px;padding-top:1.5rem}
html,body,.stApp{background:linear-gradient(180deg,#edf3ff 0%,#d8e6fa 100%)!important;
  color:var(--text)!important;font-family:Inter,system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,"Helvetica Neue",Arial}
.card{background:var(--panel);border:1px solid var(--border);border-radius:14px;
  padding:1.3rem 1.4rem;box-shadow:0 6px 18px var(--shadow);transition:all .25s ease}
.card:hover{transform:translateY(-2px);box-shadow:0 8px 26px rgba(37,99,235,.15)}
h1,h2,h3{color:var(--brand-dark)!important;font-weight:700;margin-bottom:.5rem}
.small{color:var(--muted);font-size:.92rem} .muted{color:var(--muted)} p{line-height:1.55}
ul{margin:.25rem 0 .25rem 1.1rem}
img.profile{width:100%;max-width:220px;aspect-ratio:1/1;object-fit:cover;border-radius:14px;
  border:2px solid var(--border);box-shadow:0 4px 16px rgba(37,99,235,.15)}
.metrics-wrap{display:grid;grid-template-columns:repeat(3,1fr);gap:.7rem}
.metric-chip{text-align:center;background:var(--chip);border:1px solid var(--border);
  border-radius:12px;padding:.8rem .5rem;box-shadow:0 1px 0 rgba(0,0,0,.03)}
.metric-chip .value{font-size:1.7rem;font-weight:700;line-height:1;color:var(--brand)}
.metric-chip .label{margin-top:.25rem;font-size:.9rem;color:var(--muted)}
.pills{display:flex;flex-wrap:wrap;gap:.5rem}
.pill{padding:.42rem .75rem;border-radius:999px;font-size:.9rem;background:var(--chip);
  border:1px solid var(--border);color:var(--brand-dark);font-weight:500;transition:background .2s ease,transform .2s ease}
.pill:hover{background:#d2e3ff;transform:translateY(-1px)}
a{color:var(--brand)!important;text-decoration:none;font-weight:500}
a:hover{text-decoration:underline;color:var(--brand-dark)!important}
.btn{display:inline-block;padding:.5rem .9rem;border-radius:10px;border:1px solid var(--border);
  background:var(--panel);color:var(--brand-dark);box-shadow:0 2px 6px var(--shadow);transition:all .2s ease}
.btn:hover{background:var(--brand);color:#fff!important;border-color:var(--brand);transform:translateY(-2px)}
hr,.stDivider{opacity:.5;border-color:var(--border)}
.stTabs [data-baseweb="tab-list"]{border-bottom:2px solid var(--border)}
.stTabs [data-baseweb="tab"]{color:var(--muted);font-weight:500;padding:.5rem 1rem}
.stTabs [aria-selected="true"]{color:var(--brand-dark);border-bottom:3px solid var(--brand)}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Load live data
# -----------------------------------------------------------------------------
metrics = get_metrics()

# -----------------------------------------------------------------------------
# HERO
# -----------------------------------------------------------------------------
c1, c2, c3 = st.columns([0.26, 0.52, 0.22], gap="large")

with c1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    try:
        st.image(get_profile_image_src(), use_container_width=True)
    except Exception:
        st.warning("Profile image could not be loaded — showing a placeholder.")
        st.image(FALLBACK_AVATAR_URL, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"### {DATA['name']}")
    st.markdown(f"**{DATA['title']}**")
    st.markdown(f"📍 {DATA['location']}")
    st.markdown(DATA["summary"])
    st.markdown(
        " ".join([f"<a class='btn' href='{v}' target='_blank'>{k}</a>" for k, v in DATA["links"].items()]),
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("**Publication metrics**")
    st.markdown('<div class="metrics-wrap">', unsafe_allow_html=True)
    st.markdown(
        f"<div class='metric-chip'><p class='value'>{metrics.get('h_index','—')}</p>"
        f"<div class='label'>h-index</div></div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<div class='metric-chip'><p class='value'>{metrics.get('i10_index','—')}</p>"
        f"<div class='label'>i10</div></div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<div class='metric-chip'><p class='value'>{metrics.get('citations','—')}</p>"
        f"<div class='label'>Citations</div></div>",
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("Refresh Google Scholar metrics"):
        get_metrics.clear()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Tabs
# -----------------------------------------------------------------------------
tabs = st.tabs([
    "About", "Education", "Experience", "Projects", "Funding", "Training",
    "Skills", "Publications", "Awards", "Contact"
])

# ---- About
with tabs[0]:
    st.markdown("### Biography")
    bio_text = load_bio()
    if bio_text:
        bio_html = bio_text.replace("\n\n", "</p><p>").replace("\n", "<br>")
        st.markdown(f"<div class='card'><p>{bio_html}</p></div>", unsafe_allow_html=True)
    else:
        st.markdown(
            "<div class='card'><p class='small'>No biography found. "
            "Create <code>static/biography.txt</code> to add your bio.</p></div>",
            unsafe_allow_html=True,
        )

# ---- Education
with tabs[1]:
    st.markdown("### Education")
    items = []
    for e in DATA["education"]:
        items.append(
            f"<li><p><strong>{e['degree']}</strong>, {e['school']}<br>"
            f"<em>{e['years']}</em><br>"
            f"<span class='small'>{e['details']}</span></p></li>"
        )
    st.markdown(f"<div class='card'><ul>{''.join(items)}</ul></div>", unsafe_allow_html=True)

# ---- Experience
with tabs[2]:
    st.markdown("### Teaching Experience")
    for x in DATA["experience"]["teaching"]:
        bullets = "".join(f"<li>{b}</li>" for b in x["bullets"])
        st.markdown(
            f"<div class='card'>"
            f"<p><strong>{x['role']}</strong> — {x['org']}<br><em>{x['dates']}</em></p>"
            f"<ul>{bullets}</ul></div>",
            unsafe_allow_html=True,
        )

    st.markdown("### Research Experience")
    for x in DATA["experience"]["research"]:
        bullets = "".join(f"<li>{b}</li>" for b in x["bullets"])
        st.markdown(
            f"<div class='card'>"
            f"<p><strong>{x['role']}</strong> — {x['org']}<br><em>{x['dates']}</em></p>"
            f"<ul>{bullets}</ul></div>",
            unsafe_allow_html=True,
        )

# ---- Projects
with tabs[3]:
    st.markdown("### Projects")
    cols = st.columns(2, gap="large")
    for i, p in enumerate(DATA.get("projects", [])):
        with cols[i % 2]:
            tags = "".join(f"<span class='pill'>{t}</span>" for t in p.get("tags", []))
            impact = f"<div class='small'>{p['impact']}</div>" if p.get("impact") else ""
            st.markdown(
                f"<div class='card'>"
                f"<p><strong>{p['title']}</strong></p>"
                f"<p>{p['summary']}</p>"
                f"{impact}"
                f"<div class='pills'>{tags}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

# ---- Funding
with tabs[4]:
    st.markdown("### Funding")
    items = []
    for f in DATA["funding"]:
        items.append(
            f"<li><p><strong>{f['project']}</strong> — {f['body']} · {f['amount']}<br>"
            f"<span class='small'>Role: {f['role']} · Outcome: {f['outcome']}</span></p></li>"
        )
    st.markdown(f"<div class='card'><ul>{''.join(items)}</ul></div>", unsafe_allow_html=True)

# ---- Training
with tabs[5]:
    st.markdown("### Training")
    train_items = "".join(f"<li>{t}</li>" for t in DATA["training"])
    st.markdown(f"<div class='card'><ul>{train_items}</ul></div>", unsafe_allow_html=True)

# ---- Skills
with tabs[6]:
    st.markdown("### Skills")
    left, right = st.columns(2, gap="large")
    cats = list(DATA["skills"].items())
    half = (len(cats) + 1) // 2

    def render_skills(col, items):
        for cat, values in items:
            pills = "".join(f"<span class='pill'>{x}</span>" for x in values)
            col.markdown(f"**{cat}**", unsafe_allow_html=True)
            col.markdown(f"<div class='card'><div class='pills'>{pills}</div></div>", unsafe_allow_html=True)

    render_skills(left, cats[:half])
    render_skills(right, cats[half:])

# ---- Publications
with tabs[7]:
    st.markdown("### Selected Publications")
    for p in DATA["publications"]:
        st.markdown(
            f"<div class='card' style='padding:.8rem 1rem;margin-bottom:.6rem'>"
            f"<span class='pill'>{p['year']}</span> "
            f"<strong>{p['title']}</strong> — <em class='muted'>{p['venue']}</em>"
            f"</div>",
            unsafe_allow_html=True,
        )

    st.markdown("### Latest Publications (auto-updated)")
    latest = get_latest_pubs(5)
    if latest:
        for p in latest:
            title = p.get("title", "")
            venue = p.get("venue", "")
            authors = p.get("authors", "")
            year = p.get("year", "")
            url = p.get("url", "")
            st.markdown(
                f"<div class='card' style='padding:.9rem 1rem;margin-bottom:.6rem'>"
                f"<span class='pill'>{year}</span> "
                f"<a href='{url}' target='_blank'><strong>{title}</strong></a>"
                + (f" — <em class='muted'>{venue}</em>" if venue else "")
                + (f"<div class='small muted' style='margin-top:.25rem'>{authors}</div>" if authors else "")
                + f"</div>",
                unsafe_allow_html=True,
            )
    else:
        st.info("Couldn’t fetch latest publications (Scholar may have rate-limited or blocked scraping).")

    st.markdown(
        f"<div class='small'>For the full publication list, visit "
        f"<a href='{DATA['links']['Google Scholar']}' target='_blank'>Google Scholar</a>.</div>",
        unsafe_allow_html=True,
    )

# ---- Awards
with tabs[8]:
    st.markdown("### Awards")
    awards_list = "".join(f"<li>{a}</li>" for a in DATA["awards"])
    st.markdown(f"<div class='card'><ul>{awards_list}</ul></div>", unsafe_allow_html=True)

# ---- Contact
with tabs[9]:
    st.markdown("### Contact")
    st.markdown(
        f"<div class='card'>"
        f"<p><strong>Email:</strong> {DATA['email_primary']}</p>"
        f"<p><strong>Phone:</strong> {DATA['phone']}</p>"
        f"</div>",
        unsafe_allow_html=True,
    )

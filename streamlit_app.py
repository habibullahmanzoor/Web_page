# streamlit_app.py
from pathlib import Path
from typing import List, Dict, Optional

import streamlit as st

from data import DATA
import scholar_scraper


# =========================
# CONFIG & PATHS
# =========================
APP_DIR = Path(__file__).resolve().parent
STATIC_DIR = APP_DIR / "static"

SCHOLAR_URL = "https://scholar.google.com/citations?user=tKDhmdAAAAAJ&hl=en"
PHOTO = STATIC_DIR / "habib.jpeg"
BIO_PATH = STATIC_DIR / "biography.txt"

st.set_page_config(
    page_title=f"{DATA['name']} — Portfolio",
    page_icon="📄",
    layout="wide",
    menu_items={"Report a bug": None, "About": None},
)


# =========================
# HELPERS / CACHED CALLS
# =========================
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
    """Fetch latest publications (by year) with caching; fallback to static DATA."""
    try:
        return scholar_scraper.fetch_latest_publications(SCHOLAR_URL, count=count)
    except Exception:
        pubs = sorted(
            DATA.get("publications", []),
            key=lambda p: p.get("year", 0),
            reverse=True,
        )
        return [
            {
                "title": p["title"],
                "year": p.get("year"),
                "venue": p.get("venue", ""),
                "url": None,
                "authors": "",
            }
            for p in pubs[:count]
        ]


def load_profile_photo_for_streamlit():
    """
    Return image data as bytes (best compatibility on Streamlit Cloud),
    or a fallback URL if the local file is missing/unreadable.
    """
    try:
        if PHOTO.exists() and PHOTO.is_file():
            return PHOTO.read_bytes()  # << bytes are safest for st.image
    except Exception as e:
        # keep quiet in prod; uncomment to debug:
        # st.caption(f"[img-debug] {e}")
        pass
    return "https://via.placeholder.com/220?text=Profile"


# =========================
# THEME (Blue Academic)
# =========================
st.markdown(
    """
<style>
/* ======== Blue Academic Theme ======== */
:root {
  --bg: #eaf2fb;
  --panel: #f8fbff;
  --text: #0b1a3f;
  --muted: #4b5563;
  --border: #cbdaf3;
  --chip: #e0edff;
  --brand: #2563eb;
  --brand-dark: #1e40af;
  --shadow: rgba(30, 64, 175, 0.12);
}

/* Layout */
.block-container { max-width: 1150px; padding-top: 1.5rem; }
html, body, .stApp {
  background: linear-gradient(180deg, #edf3ff 0%, #d8e6fa 100%) !important;
  color: var(--text) !important;
  font-family: 'Inter', sans-serif;
}

/* Cards */
.card {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 1.3rem 1.4rem;
  box-shadow: 0 6px 18px var(--shadow);
  transition: all 0.25s ease;
}
.card:hover { transform: translateY(-2px); box-shadow: 0 8px 26px rgba(37, 99, 235, 0.15); }

/* Typography */
h1, h2, h3 { color: var(--brand-dark) !important; font-weight: 700; margin-bottom: 0.5rem; }
.small { color: var(--muted); font-size: .92rem; }
.muted { color: var(--muted); }
p { line-height: 1.55; }
ul { margin: .25rem 0 .25rem 1.1rem; }

/* Profile image */
img.profile {
  width: 100%; max-width: 220px; aspect-ratio: 1/1; object-fit: cover;
  border-radius: 14px; border: 2px solid var(--border);
  box-shadow: 0 4px 16px rgba(37, 99, 235, 0.15);
}

/* Metrics */
.metrics-wrap { display: grid; grid-template-columns: repeat(3, 1fr); gap: .7rem; }
.metric-chip {
  text-align: center; background: var(--chip); border: 1px solid var(--border);
  border-radius: 12px; padding: .8rem .5rem; box-shadow: 0 1px 0 rgba(0,0,0,.03);
}
.metric-chip .value { font-size: 1.7rem; font-weight: 700; line-height: 1; color: var(--brand); }
.metric-chip .label { margin-top: .25rem; font-size: .9rem; color: var(--muted); }

/* Pills (tags) */
.pills { display: flex; flex-wrap: wrap; gap: .5rem; }
.pill  {
  padding: .42rem .75rem; border-radius: 999px; font-size: .9rem;
  background: var(--chip); border: 1px solid var(--border);
  color: var(--brand-dark); font-weight: 500;
  transition: background 0.2s ease, transform 0.2s ease;
}
.pill:hover { background: #d2e3ff; transform: translateY(-1px); }

/* Links / buttons */
a { color: var(--brand) !important; text-decoration: none; font-weight: 500; }
a:hover { text-decoration: underline; color: var(--brand-dark) !important; }
.btn {
  display: inline-block; padding: .5rem .9rem; border-radius: 10px;
  border: 1px solid var(--border); background: var(--panel); color: var(--brand-dark);
  box-shadow: 0 2px 6px var(--shadow); transition: all 0.2s ease;
}
.btn:hover { background: var(--brand); color: white !important; border-color: var(--brand); transform: translateY(-2px); }

/* Dividers / Tabs */
hr, .stDivider { opacity: .5; border-color: var(--border); }
.stTabs [data-baseweb="tab-list"] { border-bottom: 2px solid var(--border); }
.stTabs [data-baseweb="tab"] { color: var(--muted); font-weight: 500; padding: 0.5rem 1rem; }
.stTabs [aria-selected="true"] { color: var(--brand-dark); border-bottom: 3px solid var(--brand); }
</style>
""",
    unsafe_allow_html=True,
)


# =========================
# DATA & HERO
# =========================
# =========================
# DATA & HERO
# =========================
metrics = get_metrics()

c1, c2, c3 = st.columns([0.26, 0.52, 0.22], gap="large")

with c1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    try:
        img_data = load_profile_photo_for_streamlit()
        st.image(img_data, use_container_width=True)
    except Exception as e:
        st.warning("Profile image could not be loaded — skipping image display.")
        # st.write(f"Debug: {e}")  # Uncomment to see the actual error if needed
    st.markdown("</div>", unsafe_allow_html=True)


with c2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"### {DATA['name']}")
    st.markdown(f"**{DATA['title']}**")
    st.markdown(f"📍 {DATA['location']}")
    st.markdown(DATA["summary"])
    st.markdown(
        " ".join(
            f"<a class='btn' href='{url}' target='_blank'>{label}</a>"
            for label, url in DATA["links"].items()
        ),
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

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
    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("Refresh Google Scholar metrics"):
        get_metrics.clear()
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


# =========================
# TABS
# =========================
tabs = st.tabs(
    [
        "About",
        "Education",
        "Experience",
        "Projects",
        "Funding",
        "Training",
        "Skills",
        "Publications",
        "Awards",
        "Contact",
    ]
)

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
    edu_items = []
    for e in DATA["education"]:
        edu_items.append(
            f"<li><p><strong>{e['degree']}</strong>, {e['school']}<br>"
            f"<em>{e['years']}</em><br>"
            f"<span class='small'>{e['details']}</span></p></li>"
        )
    st.markdown(f"<div class='card'><ul>{''.join(edu_items)}</ul></div>", unsafe_allow_html=True)

# ---- Experience
with tabs[2]:
    st.markdown("### Teaching Experience")
    for x in DATA["experience"]["teaching"]:
        bullets = "".join(f"<li>{b}</li>" for b in x["bullets"])
        st.markdown(
            f"""
            <div class="card">
              <p><strong>{x['role']}</strong> — {x['org']}<br><em>{x['dates']}</em></p>
              <ul>{bullets}</ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### Research Experience")
    for x in DATA["experience"]["research"]:
        bullets = "".join(f"<li>{b}</li>" for b in x["bullets"])
        st.markdown(
            f"""
            <div class="card">
              <p><strong>{x['role']}</strong> — {x['org']}<br><em>{x['dates']}</em></p>
              <ul>{bullets}</ul>
            </div>
            """,
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
                f"""
                <div class="card">
                  <p><strong>{p['title']}</strong></p>
                  <p>{p['summary']}</p>
                  {impact}
                  <div class="pills">{tags}</div>
                </div>
                """,
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
    st.markdown(
        f"<div class='card'><ul>{''.join(f'<li>{t}</li>' for t in DATA['training'])}</ul></div>",
        unsafe_allow_html=True,
    )

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
            col.markdown(
                f"""
                <div class="card">
                  <div class="pills">{pills}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

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
    latest_pubs = get_latest_pubs(5)
    if latest_pubs:
        for p in latest_pubs:
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
                + (
                    f"<div class='small muted' style='margin-top:.25rem'>{authors}</div>"
                    if authors
                    else ""
                )
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
        f"""
        <div class="card">
          <p><strong>Email:</strong> {DATA['email_primary']}</p>
          <p><strong>Phone:</strong> {DATA['phone']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )



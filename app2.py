"""
AI Model Arena — Data Uploader & API Key Manager
================================================
Run alongside app1.py. This page lets you:
  1. Store API keys (saved to session state, never persisted to disk)
  2. Upload CSV / JSON datasets of model benchmark data
  3. Preview, validate, and push the data into the Arena (app1.py session state)

Usage:
    Add this file next to app1.py and run:
        streamlit run data_uploader.py
    Or add it as a page in a multipage app (pages/data_uploader.py).
"""

import streamlit as st
import pandas as pd
import json
import io
from datetime import datetime

# ═══════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════
st.set_page_config(
    page_title="Arena · Data Uploader",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════
# STYLES  (same design language as app1.py)
# ═══════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@300;400;500;600&display=swap');

:root {
  --bg:#050508; --s1:#0c0c14; --s2:#111120; --s3:#181828;
  --border:#1f1f38; --border2:#2a2a50;
  --text:#eeeef8; --muted:#5a5a80; --muted2:#8888b0;
  --a1:#7c6fff; --a2:#00d4aa; --a3:#ff5e7d; --a4:#ffb340; --a5:#4dc9f6;
}
*,*::before,*::after{box-sizing:border-box;margin:0}
html,body,[class*="css"]{font-family:'Outfit',sans-serif!important;color:var(--text)!important}
.stApp{background:var(--bg)!important}
section[data-testid="stSidebar"]{background:var(--s1)!important;border-right:1px solid var(--border)!important}
section[data-testid="stSidebar"] *{color:var(--text)!important}

.stTextInput>div>div>input,.stTextArea>div>div>textarea,.stNumberInput>div>div>input,
.stSelectbox>div>div,.stMultiSelect>div>div{
  background:var(--s2)!important;border:1px solid var(--border)!important;
  border-radius:10px!important;color:var(--text)!important;
  font-family:'Outfit',sans-serif!important;font-size:.9rem!important}

.stButton>button{
  background:linear-gradient(135deg,#7c6fff,#00d4aa)!important;
  border:none!important;border-radius:10px!important;color:#fff!important;
  font-family:'Outfit',sans-serif!important;font-weight:700!important;
  font-size:.9rem!important;padding:.55rem 1.4rem!important;
  transition:opacity .2s,transform .1s!important}
.stButton>button:hover{opacity:.85!important;transform:translateY(-1px)!important}

.stTabs [data-baseweb="tab-list"]{
  background:var(--s2)!important;border-radius:14px!important;
  padding:5px!important;gap:4px!important;border:1px solid var(--border)!important}
.stTabs [data-baseweb="tab"]{
  background:transparent!important;border-radius:10px!important;
  color:var(--muted)!important;font-family:'JetBrains Mono',monospace!important;
  font-size:.78rem!important;padding:.5rem 1rem!important}
.stTabs [aria-selected="true"]{
  background:var(--s3)!important;color:var(--text)!important;
  border:1px solid var(--border2)!important}

.stExpander{background:var(--s2)!important;border:1px solid var(--border)!important;border-radius:12px!important}
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:var(--border2);border-radius:10px}

.section-label{
  font-family:'JetBrains Mono',monospace;font-size:.68rem;
  letter-spacing:.2em;color:var(--a2);text-transform:uppercase;margin-bottom:.5rem}
.glass-card{
  background:var(--s2);border:1px solid var(--border);border-radius:16px;
  padding:1.4rem 1.6rem;position:relative;overflow:hidden;margin-bottom:1rem}
.glass-card::before{
  content:'';position:absolute;inset:0;
  background:linear-gradient(135deg,rgba(124,111,255,.06),transparent 60%);
  pointer-events:none}
.glow-chip{
  display:inline-flex;align-items:center;gap:.3rem;
  padding:.18rem .6rem;border-radius:999px;
  font-family:'JetBrains Mono',monospace;font-size:.7rem;font-weight:500}
.chip-purple{background:rgba(124,111,255,.15);border:1px solid rgba(124,111,255,.3);color:#7c6fff}
.chip-green{background:rgba(0,212,170,.12);border:1px solid rgba(0,212,170,.3);color:#00d4aa}
.chip-red{background:rgba(255,94,125,.12);border:1px solid rgba(255,94,125,.3);color:#ff5e7d}
.chip-yellow{background:rgba(255,179,64,.12);border:1px solid rgba(255,179,64,.3);color:#ffb340}
.chip-blue{background:rgba(77,201,246,.12);border:1px solid rgba(77,201,246,.3);color:#4dc9f6}
.key-row{display:flex;align-items:center;justify-content:space-between;padding:.5rem 0;border-bottom:1px solid var(--border)}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════
DIMS       = ["accuracy","speed","reasoning","creativity","safety","cost_eff","multilingual","instruction"]
DIM_LABELS = ["Accuracy","Speed","Reasoning","Creativity","Safety","Cost Eff.","Multilingual","Instruction"]

# Required columns for CSV/JSON upload
REQUIRED_COLS = ["name"]
NUMERIC_COLS  = DIMS + ["price_in","price_out","context","mmlu","gsm8k","humaneval"]
OPTIONAL_COLS = ["provider","version","category","release_date","license","modalities",
                 "tags","notes","benchmark","public_resp","open_source"] + NUMERIC_COLS

# ═══════════════════════════════════════════════════════
# SESSION STATE INIT
# ═══════════════════════════════════════════════════════
for k, v in {
    "models":        [],          # shared with app1.py if multipage
    "api_keys":      {},          # {"OpenAI": "sk-...", ...}
    "upload_log":    [],          # history of uploads
    "preview_data":  None,        # parsed but not yet committed
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ═══════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════
def compute_overall(m):
    w = dict(accuracy=.25,speed=.15,reasoning=.22,creativity=.10,
             safety=.10,cost_eff=.10,multilingual=.05,instruction=.03)
    return round(sum(m.get(k,0)*v for k,v in w.items()), 1)

def safe_float(val, default=0.0):
    try:    return float(val)
    except: return default

def safe_int(val, default=0):
    try:    return int(float(val))
    except: return default

def safe_list(val):
    """Turn a string like 'Text,Image' or ['Text','Image'] into a list."""
    if isinstance(val, list):
        return [str(v).strip() for v in val if str(v).strip()]
    if isinstance(val, str):
        return [v.strip() for v in val.split(",") if v.strip()]
    return []

def row_to_model(row: dict) -> dict:
    """Normalise a raw dict (from CSV/JSON row) into the Arena model schema."""
    m = {}
    m["name"]         = str(row.get("name","")).strip()
    m["provider"]     = str(row.get("provider","")).strip()
    m["version"]      = str(row.get("version","")).strip()
    m["category"]     = str(row.get("category","General")).strip() or "General"
    m["release_date"] = str(row.get("release_date","")).strip()
    m["license"]      = str(row.get("license","Proprietary")).strip() or "Proprietary"
    m["modalities"]   = safe_list(row.get("modalities","Text"))
    m["tags"]         = safe_list(row.get("tags",""))
    m["notes"]        = str(row.get("notes","")).strip()
    m["benchmark"]    = str(row.get("benchmark","")).strip()
    m["public_resp"]  = str(row.get("public_resp","")).strip()
    m["open_source"]  = str(row.get("open_source","false")).lower() in ("true","1","yes","open source")
    # numeric perf scores
    for d in DIMS:
        m[d] = min(100, max(0, safe_int(row.get(d, 0))))
    # pricing / context / benchmarks
    m["price_in"]   = safe_float(row.get("price_in",  0.0))
    m["price_out"]  = safe_float(row.get("price_out", 0.0))
    m["context"]    = safe_int(row.get("context", 128000))
    m["mmlu"]       = safe_float(row.get("mmlu",      0.0))
    m["gsm8k"]      = safe_float(row.get("gsm8k",     0.0))
    m["humaneval"]  = safe_float(row.get("humaneval",  0.0))
    m["added_at"]   = datetime.now().strftime("%Y-%m-%d %H:%M")
    m["overall"]    = compute_overall(m)
    return m

def validate_models(models: list) -> tuple[list, list]:
    """Return (valid_models, error_messages)."""
    valid, errors = [], []
    seen_names = set()
    for i, m in enumerate(models):
        row_errors = []
        if not m.get("name"):
            row_errors.append("Missing 'name'")
        elif m["name"] in seen_names:
            row_errors.append(f"Duplicate name '{m['name']}'")
        else:
            seen_names.add(m["name"])
        # warn if all performance scores are 0
        if all(m.get(d, 0) == 0 for d in DIMS):
            row_errors.append("All performance scores are 0 — did you map the columns?")
        if row_errors:
            errors.append(f"Row {i+1} ({m.get('name','?')}): " + "; ".join(row_errors))
        else:
            valid.append(m)
    return valid, errors

def parse_csv(file) -> list[dict]:
    df = pd.read_csv(file)
    df.columns = [c.strip().lower().replace(" ","_") for c in df.columns]
    return df.to_dict(orient="records")

def parse_json(file) -> list[dict]:
    data = json.load(file)
    if isinstance(data, dict):
        # maybe it's {"models": [...]}
        data = data.get("models", [data])
    if isinstance(data, list):
        return data
    raise ValueError("JSON must be a list of model objects or {'models': [...]}")

def mask_key(k: str) -> str:
    if len(k) <= 8:
        return "•" * len(k)
    return k[:4] + "•" * (len(k)-8) + k[-4:]

# ═══════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════
st.markdown("""
<div style="text-align:center;padding:2rem 0 1.5rem">
  <div style="font-family:'Outfit',sans-serif;font-weight:900;font-size:2.5rem;
    background:linear-gradient(135deg,#7c6fff 0%,#00d4aa 50%,#ffb340 100%);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
    letter-spacing:-1.5px;line-height:1">📡 Arena · Data Hub</div>
  <div style="font-family:'JetBrains Mono',monospace;font-size:.75rem;color:#5a5a80;
    letter-spacing:.15em;margin-top:.5rem">API KEYS · DATASET UPLOAD · LIVE SYNC</div>
</div>""", unsafe_allow_html=True)

# quick status bar
n_models = len(st.session_state.models)
n_keys   = len(st.session_state.api_keys)
s1,s2,s3,s4 = st.columns(4)
s1.metric("Models in Arena", n_models)
s2.metric("API Keys Stored", n_keys)
s3.metric("Uploads This Session", len(st.session_state.upload_log))
s4.metric("Preview Pending", "Yes" if st.session_state.preview_data else "No")

st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════
tabs = st.tabs(["🔑 API Keys", "📂 Upload Dataset", "🔄 Sync & Preview", "📋 Schema Guide", "🗑️ Manage Arena"])

# ══════════════════════════════════════════
# TAB 0 — API KEYS
# ══════════════════════════════════════════
with tabs[0]:
    st.markdown('<p class="section-label">STORE API KEYS</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="glass-card" style="border-color:#ffb340">
      <div style="font-family:'JetBrains Mono',monospace;font-size:.75rem;color:#ffb340;margin-bottom:.4rem">⚠ SECURITY NOTICE</div>
      <div style="font-family:'Outfit',sans-serif;font-size:.88rem;color:#8888b0;line-height:1.6">
        Keys are stored <strong style="color:#eeeef8">only in this browser session</strong> and are never written to disk or sent anywhere.
        They disappear when you close the tab. Do not commit API keys to version control.
      </div>
    </div>""", unsafe_allow_html=True)

    with st.form("add_key_form", clear_on_submit=True):
        st.markdown('<p class="section-label">ADD / UPDATE KEY</p>', unsafe_allow_html=True)
        k1, k2 = st.columns([1, 2])
        key_provider = k1.selectbox("Provider", [
            "OpenAI", "Anthropic", "Google", "Meta", "Mistral",
            "Cohere", "Together AI", "Groq", "HuggingFace", "Custom"
        ])
        custom_provider = k1.text_input("Custom provider name", placeholder="e.g. MyOrg")
        api_key_val = k2.text_input("API Key", type="password", placeholder="sk-... or key-...")
        key_label   = k2.text_input("Label (optional)", placeholder="e.g. prod-key, personal")
        if st.form_submit_button("💾 Save Key", use_container_width=True):
            provider_name = custom_provider.strip() if key_provider == "Custom" and custom_provider.strip() else key_provider
            if not api_key_val.strip():
                st.error("Please enter an API key.")
            else:
                label = key_label.strip() or provider_name
                st.session_state.api_keys[label] = api_key_val.strip()
                st.success(f"✓ Key saved for '{label}'")
                st.rerun()

    if st.session_state.api_keys:
        st.markdown('<p class="section-label" style="margin-top:1.2rem">STORED KEYS</p>', unsafe_allow_html=True)
        for label, key_val in list(st.session_state.api_keys.items()):
            c1, c2, c3 = st.columns([3, 4, 1])
            c1.markdown(
                f'<div class="key-row"><span style="font-family:JetBrains Mono,monospace;font-size:.82rem;color:#eeeef8">{label}</span></div>',
                unsafe_allow_html=True
            )
            c2.markdown(
                f'<div class="key-row"><span style="font-family:JetBrains Mono,monospace;font-size:.78rem;color:#5a5a80">{mask_key(key_val)}</span></div>',
                unsafe_allow_html=True
            )
            if c3.button("🗑", key=f"del_key_{label}"):
                del st.session_state.api_keys[label]
                st.rerun()

        st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)
        # export keys as env snippet
        env_txt = "\n".join(f'{k.upper().replace(" ","_")}_API_KEY="{v}"' for k,v in st.session_state.api_keys.items())
        st.download_button(
            "⬇ Export as .env snippet",
            env_txt, "arena_keys.env", "text/plain",
            use_container_width=True
        )
    else:
        st.info("No keys stored yet. Add one above.")

# ══════════════════════════════════════════
# TAB 1 — UPLOAD DATASET
# ══════════════════════════════════════════
with tabs[1]:
    st.markdown('<p class="section-label">UPLOAD CSV OR JSON</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
      <div style="font-family:'JetBrains Mono',monospace;font-size:.72rem;color:#00d4aa;margin-bottom:.6rem">SUPPORTED FORMATS</div>
      <div style="font-family:'Outfit',sans-serif;font-size:.88rem;color:#8888b0;line-height:1.8">
        <strong style="color:#eeeef8">CSV</strong> — one row per model, column headers match schema (see Schema Guide tab)<br>
        <strong style="color:#eeeef8">JSON</strong> — array of model objects <code style="color:#7c6fff">[ {...}, {...} ]</code>
        or <code style="color:#7c6fff">{"models": [{...}]}</code>
      </div>
    </div>""", unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Drop your dataset here",
        type=["csv","json"],
        help="CSV or JSON file. See Schema Guide tab for column definitions."
    )

    col_mode = st.radio(
        "On upload, models should:",
        ["Replace all current Arena models", "Merge with existing Arena models (skip duplicates)", "Append all (allow duplicates)"],
        horizontal=True
    )

    if uploaded_file is not None:
        st.markdown('<p class="section-label" style="margin-top:1rem">RAW PARSE</p>', unsafe_allow_html=True)
        try:
            if uploaded_file.name.endswith(".csv"):
                raw_rows = parse_csv(uploaded_file)
            else:
                raw_rows = parse_json(uploaded_file)

            st.success(f"✓ Parsed {len(raw_rows)} row(s) from **{uploaded_file.name}**")

            # show raw preview
            with st.expander("👁 Raw parsed rows (first 5)"):
                st.json(raw_rows[:5])

            # normalise
            parsed_models = [row_to_model(r) for r in raw_rows]
            valid_models, errors = validate_models(parsed_models)

            if errors:
                st.markdown('<p class="section-label" style="margin-top:.8rem;color:#ff5e7d">VALIDATION ISSUES</p>', unsafe_allow_html=True)
                for e in errors:
                    st.warning(e)

            if valid_models:
                st.markdown(f'<p class="section-label" style="margin-top:.8rem">PREVIEW ({len(valid_models)} valid models)</p>', unsafe_allow_html=True)
                preview_df = pd.DataFrame([{
                    "Name": m["name"], "Provider": m["provider"],
                    "Overall": m["overall"],
                    **{l: m.get(d,0) for d,l in zip(DIMS, DIM_LABELS)},
                    "Context(K)": m.get("context",0)//1000,
                    "In$/1M": m.get("price_in",0),
                } for m in valid_models])
                st.dataframe(preview_df, use_container_width=True, hide_index=True)

                # stash for Sync tab
                st.session_state.preview_data = {
                    "models": valid_models,
                    "mode": col_mode,
                    "filename": uploaded_file.name,
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                }
                st.info("✅ Data is ready. Go to the **Sync & Preview** tab to commit it to the Arena.")
            else:
                st.error("No valid models found after validation. Check your column names (see Schema Guide).")

        except Exception as ex:
            st.error(f"Parse error: {ex}")
            st.caption("Make sure your file matches the expected format. See Schema Guide tab.")

# ══════════════════════════════════════════
# TAB 2 — SYNC & PREVIEW
# ══════════════════════════════════════════
with tabs[2]:
    st.markdown('<p class="section-label">COMMIT TO ARENA</p>', unsafe_allow_html=True)

    if not st.session_state.preview_data:
        st.info("No data pending. Upload a dataset in the **Upload Dataset** tab first.")
    else:
        pd_data = st.session_state.preview_data
        st.markdown(f"""
        <div class="glass-card" style="border-color:#00d4aa">
          <div style="font-family:'JetBrains Mono',monospace;font-size:.7rem;color:#00d4aa">PENDING UPLOAD</div>
          <div style="font-family:'Outfit',sans-serif;font-weight:800;font-size:1.3rem;color:#eeeef8;margin:.3rem 0">{pd_data['filename']}</div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:.72rem;color:#5a5a80">
            {len(pd_data['models'])} models · parsed at {pd_data['timestamp']} · mode: {pd_data['mode']}
          </div>
        </div>""", unsafe_allow_html=True)

        # detailed preview cards
        st.markdown('<p class="section-label">MODELS TO IMPORT</p>', unsafe_allow_html=True)
        PALETTE = ["#7c6fff","#00d4aa","#ff5e7d","#ffb340","#4dc9f6","#a78bfa","#34d399","#f87171","#60a5fa","#fbbf24"]
        cols_p = st.columns(min(3, len(pd_data["models"])))
        for i, m in enumerate(pd_data["models"]):
            c = PALETTE[i % len(PALETTE)]
            with cols_p[i % len(cols_p)]:
                tag_html = "".join([f'<span class="glow-chip chip-purple">{t}</span>' for t in m.get("tags",[])])
                st.markdown(f"""
                <div class="glass-card" style="border-color:{c};padding:1rem">
                  <div style="font-family:'Outfit',sans-serif;font-weight:800;color:{c};font-size:1rem">{m["name"]}</div>
                  <div style="font-family:'JetBrains Mono',monospace;font-size:.65rem;color:#5a5a80;margin:.2rem 0">
                    {m.get("provider","")} · {m.get("category","")}
                  </div>
                  <div style="font-family:'Outfit',sans-serif;font-weight:900;font-size:1.8rem;color:{c};margin:.4rem 0">{m["overall"]}</div>
                  <div style="font-family:'JetBrains Mono',monospace;font-size:.65rem;color:#5a5a80">Overall Score</div>
                  <div style="margin-top:.5rem;display:flex;flex-wrap:wrap;gap:.2rem">{tag_html}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)
        commit_col, discard_col = st.columns(2)

        if commit_col.button("✅ Commit to Arena", use_container_width=True):
            new_models = pd_data["models"]
            mode = pd_data["mode"]

            if "Replace" in mode:
                st.session_state.models = new_models
            elif "Merge" in mode:
                existing_names = {m["name"] for m in st.session_state.models}
                added = [m for m in new_models if m["name"] not in existing_names]
                st.session_state.models.extend(added)
            else:  # Append all
                st.session_state.models.extend(new_models)

            st.session_state.upload_log.append({
                "file": pd_data["filename"],
                "count": len(new_models),
                "mode": mode,
                "time": pd_data["timestamp"],
            })
            st.session_state.preview_data = None
            st.success(f"✓ {len(new_models)} model(s) synced to Arena! Switch to app1.py to see the updated dashboard.")
            st.rerun()

        if discard_col.button("🗑 Discard Preview", use_container_width=True):
            st.session_state.preview_data = None
            st.rerun()

    # upload history
    if st.session_state.upload_log:
        st.markdown('<p class="section-label" style="margin-top:1.5rem">UPLOAD HISTORY</p>', unsafe_allow_html=True)
        for entry in reversed(st.session_state.upload_log):
            st.markdown(
                f'<div style="display:flex;gap:1.5rem;padding:.5rem 0;border-bottom:1px solid var(--border);'
                f'font-family:JetBrains Mono,monospace;font-size:.75rem">'
                f'<span style="color:#5a5a80">{entry["time"]}</span>'
                f'<span style="color:#eeeef8">{entry["file"]}</span>'
                f'<span class="glow-chip chip-green">{entry["count"]} models</span>'
                f'<span style="color:#5a5a80">{entry["mode"].split()[0]}</span>'
                f'</div>',
                unsafe_allow_html=True
            )

# ══════════════════════════════════════════
# TAB 3 — SCHEMA GUIDE
# ══════════════════════════════════════════
with tabs[3]:
    st.markdown('<p class="section-label">COLUMN SCHEMA</p>', unsafe_allow_html=True)

    schema_rows = [
        ("name",         "string",  "✅ Required", "Model name, e.g. GPT-4o"),
        ("provider",     "string",  "Optional",    "Company, e.g. OpenAI"),
        ("version",      "string",  "Optional",    "Model version string"),
        ("category",     "string",  "Optional",    "General / Code / Multimodal / Reasoning / Vision / Audio / Embedding"),
        ("release_date", "string",  "Optional",    "YYYY-MM-DD format"),
        ("license",      "string",  "Optional",    "Proprietary / Open Source / Mixed / Research"),
        ("modalities",   "string",  "Optional",    "Comma-separated: Text,Image,Audio,Video"),
        ("tags",         "string",  "Optional",    "Comma-separated keywords: flagship,coding,fast"),
        ("open_source",  "bool",    "Optional",    "true / false / yes / no / 1 / 0"),
        ("accuracy",     "int 0-100","Optional",   "Accuracy score 0–100"),
        ("speed",        "int 0-100","Optional",   "Speed score 0–100"),
        ("reasoning",    "int 0-100","Optional",   "Reasoning score 0–100"),
        ("creativity",   "int 0-100","Optional",   "Creativity score 0–100"),
        ("safety",       "int 0-100","Optional",   "Safety score 0–100"),
        ("cost_eff",     "int 0-100","Optional",   "Cost efficiency score 0–100"),
        ("multilingual", "int 0-100","Optional",   "Multilingual score 0–100"),
        ("instruction",  "int 0-100","Optional",   "Instruction-following score 0–100"),
        ("price_in",     "float",   "Optional",    "Input price in $/1M tokens"),
        ("price_out",    "float",   "Optional",    "Output price in $/1M tokens"),
        ("context",      "int",     "Optional",    "Context window in tokens, e.g. 128000"),
        ("mmlu",         "float",   "Optional",    "MMLU benchmark % (0–100)"),
        ("gsm8k",        "float",   "Optional",    "GSM8K benchmark % (0–100)"),
        ("humaneval",    "float",   "Optional",    "HumanEval benchmark % (0–100)"),
        ("benchmark",    "string",  "Optional",    "Free-text benchmark summary"),
        ("public_resp",  "string",  "Optional",    "Sample model output / public response"),
        ("notes",        "string",  "Optional",    "Any additional notes"),
    ]

    schema_df = pd.DataFrame(schema_rows, columns=["Column","Type","Required","Description"])
    st.dataframe(schema_df, use_container_width=True, hide_index=True, height=600)

    st.markdown('<p class="section-label" style="margin-top:1.5rem">SAMPLE CSV</p>', unsafe_allow_html=True)
    sample_csv = """name,provider,version,category,accuracy,speed,reasoning,creativity,safety,cost_eff,multilingual,instruction,price_in,price_out,context,mmlu,gsm8k,humaneval,release_date,license,modalities,tags,open_source,notes
GPT-4o,OpenAI,2024-11,Multimodal,92,85,91,88,90,72,88,93,5.0,15.0,128000,88.7,92.0,90.2,2024-05-13,Proprietary,"Text,Image,Audio","flagship,api",false,Best overall balance
Claude 3.5 Sonnet,Anthropic,20241022,Reasoning,91,88,93,90,95,75,85,95,3.0,15.0,200000,88.3,93.7,92.0,2024-10-22,Proprietary,"Text,Image","safety,coding",false,Best for coding
Llama 3.1 405B,Meta,405B,General,85,65,84,80,78,95,80,87,0.9,2.7,131072,87.3,89.1,89.0,2024-07-23,Open Source,Text,"open-source,free",true,Self-hostable
"""
    st.code(sample_csv, language="csv")
    st.download_button(
        "⬇ Download sample CSV",
        sample_csv, "arena_sample.csv", "text/csv",
        use_container_width=True
    )

    st.markdown('<p class="section-label" style="margin-top:1.5rem">SAMPLE JSON</p>', unsafe_allow_html=True)
    sample_json = json.dumps([
        {"name":"GPT-4o","provider":"OpenAI","category":"Multimodal",
         "accuracy":92,"speed":85,"reasoning":91,"creativity":88,"safety":90,
         "cost_eff":72,"multilingual":88,"instruction":93,
         "price_in":5.0,"price_out":15.0,"context":128000,
         "mmlu":88.7,"gsm8k":92.0,"humaneval":90.2,
         "release_date":"2024-05-13","license":"Proprietary",
         "modalities":"Text,Image,Audio","tags":"flagship,api","open_source":False},
        {"name":"Llama 3.1 405B","provider":"Meta","category":"General",
         "accuracy":85,"speed":65,"reasoning":84,"creativity":80,"safety":78,
         "cost_eff":95,"multilingual":80,"instruction":87,
         "price_in":0.9,"price_out":2.7,"context":131072,
         "release_date":"2024-07-23","license":"Open Source",
         "modalities":"Text","tags":"open-source,free","open_source":True}
    ], indent=2)
    st.code(sample_json, language="json")
    st.download_button(
        "⬇ Download sample JSON",
        sample_json, "arena_sample.json", "application/json",
        use_container_width=True
    )

# ══════════════════════════════════════════
# TAB 4 — MANAGE ARENA
# ══════════════════════════════════════════
with tabs[4]:
    st.markdown('<p class="section-label">CURRENT ARENA MODELS</p>', unsafe_allow_html=True)

    if not st.session_state.models:
        st.info("No models in the Arena yet. Upload a dataset or use Load Presets in app1.py.")
    else:
        PALETTE = ["#7c6fff","#00d4aa","#ff5e7d","#ffb340","#4dc9f6","#a78bfa","#34d399","#f87171","#60a5fa","#fbbf24"]
        # table view
        manage_df = pd.DataFrame([{
            "Name": m["name"],
            "Provider": m.get("provider",""),
            "Category": m.get("category",""),
            "Overall": m.get("overall",0),
            "Price In": f"${m.get('price_in',0):.2f}",
            "Context": f"{m.get('context',0)//1000}K",
            "Added": m.get("added_at",""),
        } for m in st.session_state.models])
        st.dataframe(manage_df, use_container_width=True, hide_index=True)

        st.markdown('<p class="section-label" style="margin-top:1rem">REMOVE INDIVIDUAL MODELS</p>', unsafe_allow_html=True)
        for i, m in enumerate(list(st.session_state.models)):
            c = PALETTE[i % len(PALETTE)]
            col_a, col_b = st.columns([6, 1])
            col_a.markdown(
                f'<div style="display:flex;align-items:center;gap:.8rem;padding:.4rem 0;'
                f'border-bottom:1px solid var(--border)">'
                f'<span style="font-family:JetBrains Mono,monospace;font-size:.78rem;color:{c};min-width:1.5rem">{i+1}</span>'
                f'<span style="font-family:Outfit,sans-serif;font-weight:700;color:#eeeef8">{m["name"]}</span>'
                f'<span style="font-family:JetBrains Mono,monospace;font-size:.68rem;color:#5a5a80">{m.get("provider","")}</span>'
                f'<span class="glow-chip chip-purple" style="margin-left:auto">{m.get("overall",0)}</span>'
                f'</div>',
                unsafe_allow_html=True
            )
            if col_b.button("🗑", key=f"rm_{i}_{m['name']}"):
                st.session_state.models = [x for x in st.session_state.models if x["name"] != m["name"]]
                st.rerun()

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        da, db, dc = st.columns(3)
        if da.button("🗑 Clear All Models", use_container_width=True):
            st.session_state.models = []
            st.rerun()

        # export current arena
        export_json = json.dumps(st.session_state.models, indent=2)
        db.download_button(
            "⬇ Export Arena JSON",
            export_json, "arena_export.json", "application/json",
            use_container_width=True
        )
        export_csv_df = pd.DataFrame(st.session_state.models)
        dc.download_button(
            "⬇ Export Arena CSV",
            export_csv_df.to_csv(index=False), "arena_export.csv", "text/csv",
            use_container_width=True
        )

# ═══════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════
st.markdown("""
<div style="text-align:center;padding:3rem 0 1.5rem;border-top:1px solid #1f1f38;margin-top:2rem">
  <div style="font-family:'JetBrains Mono',monospace;font-size:.65rem;color:#2a2a50;letter-spacing:.15em">
    📡 ARENA DATA HUB · KEYS STORED IN SESSION ONLY · NEVER PERSISTED
  </div>
</div>""", unsafe_allow_html=True)

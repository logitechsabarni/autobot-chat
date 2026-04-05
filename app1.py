import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
import math

# ═══════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════
st.set_page_config(
    page_title="AI Model Arena",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════
# GLOBAL STYLES
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
.stSlider>div>div>div>div{background:var(--a1)!important}

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

div[data-testid="stMetric"]{
  background:var(--s2)!important;border:1px solid var(--border)!important;
  border-radius:14px!important;padding:1.1rem 1.3rem!important}
div[data-testid="stMetric"] label{
  color:var(--muted)!important;font-family:'JetBrains Mono',monospace!important;
  font-size:.72rem!important;letter-spacing:.06em}
div[data-testid="stMetric"] div[data-testid="stMetricValue"]{
  font-family:'Outfit',sans-serif!important;font-weight:800!important;
  font-size:1.6rem!important;color:var(--text)!important}

.stExpander{background:var(--s2)!important;border:1px solid var(--border)!important;border-radius:12px!important}
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:var(--border2);border-radius:10px}
::-webkit-scrollbar-thumb:hover{background:var(--a1)}

.section-label{
  font-family:'JetBrains Mono',monospace;font-size:.68rem;
  letter-spacing:.2em;color:var(--a2);text-transform:uppercase;margin-bottom:.5rem}
.glass-card{
  background:var(--s2);border:1px solid var(--border);border-radius:16px;
  padding:1.4rem 1.6rem;transition:border-color .2s,box-shadow .2s;
  position:relative;overflow:hidden}
.glass-card::before{
  content:'';position:absolute;inset:0;
  background:linear-gradient(135deg,rgba(124,111,255,.06),transparent 60%);
  pointer-events:none}
.glass-card:hover{border-color:var(--border2);box-shadow:0 0 30px rgba(124,111,255,.08)}

.glow-chip{
  display:inline-flex;align-items:center;gap:.3rem;
  padding:.18rem .6rem;border-radius:999px;
  font-family:'JetBrains Mono',monospace;font-size:.7rem;font-weight:500}
.chip-purple{background:rgba(124,111,255,.15);border:1px solid rgba(124,111,255,.3);color:var(--a1)}
.chip-green{background:rgba(0,212,170,.12);border:1px solid rgba(0,212,170,.3);color:var(--a2)}
.chip-red{background:rgba(255,94,125,.12);border:1px solid rgba(255,94,125,.3);color:var(--a3)}
.chip-yellow{background:rgba(255,179,64,.12);border:1px solid rgba(255,179,64,.3);color:var(--a4)}
.chip-blue{background:rgba(77,201,246,.12);border:1px solid rgba(77,201,246,.3);color:var(--a5)}

.hero-title{
  font-family:'Outfit',sans-serif;font-weight:900;font-size:3rem;
  background:linear-gradient(135deg,#7c6fff 0%,#00d4aa 50%,#ffb340 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  letter-spacing:-1.5px;line-height:1}
.hero-sub{
  font-family:'JetBrains Mono',monospace;font-size:.78rem;
  color:var(--muted);letter-spacing:.15em;margin-top:.5rem}
.rank-bar{height:8px;background:var(--border);border-radius:4px;overflow:hidden}
.rank-bar-fill{height:100%;border-radius:4px;transition:width .6s ease}
.vs-divider{
  display:flex;align-items:center;justify-content:center;
  font-family:'Outfit',sans-serif;font-weight:900;font-size:1.5rem;color:var(--muted)}
.tag-row{display:flex;flex-wrap:wrap;gap:.3rem;margin-top:.5rem}
.timeline-dot{width:10px;height:10px;border-radius:50%;display:inline-block;margin-right:.4rem}
.ring-svg{transform:rotate(-90deg)}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# CONSTANTS & HELPERS
# ═══════════════════════════════════════════════════════
PALETTE = ["#7c6fff","#00d4aa","#ff5e7d","#ffb340","#4dc9f6","#a78bfa","#34d399","#f87171","#60a5fa","#fbbf24"]
DIMS       = ["accuracy","speed","reasoning","creativity","safety","cost_eff","multilingual","instruction"]
DIM_LABELS = ["Accuracy","Speed","Reasoning","Creativity","Safety","Cost Eff.","Multilingual","Instruction"]

PRESET_MODELS = [
    dict(name="GPT-4o",provider="OpenAI",version="2024-11",category="Multimodal",
         accuracy=92,speed=85,reasoning=91,creativity=88,safety=90,cost_eff=72,multilingual=88,instruction=93,
         price_in=5.0,price_out=15.0,context=128000,open_source=False,release_date="2024-05-13",
         modalities=["Text","Image","Audio"],license="Proprietary",
         public_resp="GPT-4o excels at complex reasoning while maintaining low latency for a frontier model.",
         benchmark="MMLU 88.7 | GSM8K 92.0 | HumanEval 90.2",mmlu=88.7,gsm8k=92.0,humaneval=90.2,
         notes="Flagship multimodal; best overall balance.",tags=["flagship","multimodal","api"]),
    dict(name="Claude 3.5 Sonnet",provider="Anthropic",version="20241022",category="Reasoning",
         accuracy=91,speed=88,reasoning=93,creativity=90,safety=95,cost_eff=75,multilingual=85,instruction=95,
         price_in=3.0,price_out=15.0,context=200000,open_source=False,release_date="2024-10-22",
         modalities=["Text","Image"],license="Proprietary",
         public_resp="Claude 3.5 Sonnet is best-in-class for coding, analysis, and nuanced writing tasks.",
         benchmark="MMLU 88.3 | GSM8K 93.7 | HumanEval 92.0",mmlu=88.3,gsm8k=93.7,humaneval=92.0,
         notes="Best-in-class for coding and safety.",tags=["safety","coding","200k"]),
    dict(name="Gemini 1.5 Pro",provider="Google",version="002",category="Multimodal",
         accuracy=89,speed=90,reasoning=88,creativity=85,safety=88,cost_eff=80,multilingual=92,instruction=89,
         price_in=3.5,price_out=10.5,context=1000000,open_source=False,release_date="2024-09-24",
         modalities=["Text","Image","Video","Audio"],license="Proprietary",
         public_resp="Gemini 1.5 Pro features a groundbreaking 1M token context window for long-context tasks.",
         benchmark="MMLU 85.9 | GSM8K 90.8 | HumanEval 84.1",mmlu=85.9,gsm8k=90.8,humaneval=84.1,
         notes="Unbeatable context window; strong multilingual.",tags=["1m-context","multilingual","video"]),
    dict(name="Llama 3.1 405B",provider="Meta",version="405B",category="General",
         accuracy=85,speed=65,reasoning=84,creativity=80,safety=78,cost_eff=95,multilingual=80,instruction=87,
         price_in=0.9,price_out=2.7,context=131072,open_source=True,release_date="2024-07-23",
         modalities=["Text"],license="Open Source",
         public_resp="Llama 3.1 405B is the best open-source model, rivaling proprietary counterparts at a fraction of the cost.",
         benchmark="MMLU 87.3 | GSM8K 89.1 | HumanEval 89.0",mmlu=87.3,gsm8k=89.1,humaneval=89.0,
         notes="Open source champion; self-hostable.",tags=["open-source","self-host","free"]),
    dict(name="Mistral Large 2",provider="Mistral",version="2407",category="Code",
         accuracy=83,speed=82,reasoning=85,creativity=78,cost_eff=88,multilingual=87,safety=80,instruction=88,
         price_in=2.0,price_out=6.0,context=131072,open_source=False,release_date="2024-07-24",
         modalities=["Text"],license="Mixed",
         public_resp="Mistral Large 2 is exceptional for code generation and multilingual tasks with top HumanEval scores.",
         benchmark="MMLU 84.0 | GSM8K 87.5 | HumanEval 92.1",mmlu=84.0,gsm8k=87.5,humaneval=92.1,
         notes="Best code model per dollar.",tags=["code","multilingual","efficient"]),
]

def compute_overall(m):
    w = dict(accuracy=.25,speed=.15,reasoning=.22,creativity=.10,safety=.10,cost_eff=.10,multilingual=.05,instruction=.03)
    return round(sum(m.get(k,0)*v for k,v in w.items()), 1)

# Base layout dict WITHOUT margin — callers add margin themselves
def pd_():
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="JetBrains Mono", color="#eeeef8"),
        margin=dict(l=10, r=10, t=30, b=10)
    )

def gs_():
    return dict(gridcolor="#1f1f38",tickfont=dict(color="#5a5a80",size=10))

def col_(i):
    return PALETTE[i % len(PALETTE)]

def make_radar(ml):
    fig = go.Figure()
    cats = DIM_LABELS + [DIM_LABELS[0]]
    for i, m in enumerate(ml):
        vals = [m.get(d, 0) for d in DIMS] + [m.get(DIMS[0], 0)]
        c = col_(i)
        r = int(c[1:3], 16); g = int(c[3:5], 16); b = int(c[5:7], 16)
        fill = f"rgba({r},{g},{b},0.13)"
        fig.add_trace(go.Scatterpolar(
            r=vals, theta=cats, fill='toself', name=m["name"],
            line=dict(color=c, width=2.5), fillcolor=fill
        ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(17,17,32,0.7)",
            radialaxis=dict(visible=True, range=[0,100], gridcolor="#1f1f38",
                            tickfont=dict(color="#5a5a80", size=8)),
            angularaxis=dict(gridcolor="#1f1f38", tickfont=dict(color="#eeeef8", size=11))
        ),
        showlegend=True,
        legend=dict(bgcolor="rgba(12,12,20,.8)", bordercolor="#1f1f38",
                    font=dict(color="#eeeef8", size=11)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="JetBrains Mono", color="#eeeef8"),
        height=420,
        margin=dict(l=50, r=50, t=30, b=30)
    )
    return fig

def make_heatmap(ml):
    z = [[m.get(d, 0) for d in DIMS] for m in ml]
    y = [m["name"] for m in ml]
    fig = go.Figure(go.Heatmap(
        z=z, x=DIM_LABELS, y=y,
        colorscale=[[0,"#0c0c14"],[0.5,"#7c6fff"],[1,"#00d4aa"]],
        text=[[str(v) for v in row] for row in z],
        texttemplate="%{text}", textfont=dict(size=11, family="JetBrains Mono"),
        hovertemplate="%{y} · %{x}: %{z}<extra></extra>", zmin=0, zmax=100
    ))
    fig.update_layout(
        **pd_(),
        height=max(250, len(ml)*55+80),
        xaxis=dict(tickfont=dict(color="#eeeef8", size=10), side="top"),
        yaxis=dict(tickfont=dict(color="#eeeef8", size=10))
    )
    return fig

def make_bar(ml, key, label):
    fig = go.Figure(go.Bar(
        x=[m["name"] for m in ml],
        y=[m.get(key, 0) for m in ml],
        text=[str(m.get(key, 0)) for m in ml],
        textposition="outside",
        marker=dict(color=[col_(i) for i in range(len(ml))], line=dict(color="rgba(0,0,0,0)")),
        textfont=dict(color="#eeeef8", family="JetBrains Mono", size=11)
    ))
    fig.update_layout(
        **pd_(),
        height=280,
        yaxis=dict(range=[0,115], **gs_()),
        xaxis=dict(tickfont=dict(color="#eeeef8", size=10)),
        title=dict(text=label, font=dict(size=12, color="#5a5a80"))
    )
    return fig

def make_bubble(ml):
    fig = go.Figure()
    for i, m in enumerate(ml):
        fig.add_trace(go.Scatter(
            x=[m.get("price_in", 0)],
            y=[m.get("overall", 0)],
            mode="markers+text",
            name=m["name"],
            text=[m["name"]],
            textposition="top center",
            marker=dict(
                size=max(m.get("context", 10000)/15000, 12),
                color=col_(i), opacity=0.85,
                line=dict(color="#eeeef8", width=1)
            ),
            textfont=dict(color="#eeeef8", family="JetBrains Mono", size=10)
        ))
    fig.update_layout(
        **pd_(),
        height=380,
        showlegend=False,
        xaxis=dict(title="Input $/1M tokens", **gs_(), titlefont=dict(color="#5a5a80")),
        yaxis=dict(title="Overall Score", **gs_(), titlefont=dict(color="#5a5a80"))
    )
    return fig

def make_timeline(ml):
    rows = [m for m in ml if m.get("release_date")]
    if not rows:
        return None
    rows.sort(key=lambda m: m["release_date"])
    fig = go.Figure()
    for i, m in enumerate(rows):
        fig.add_trace(go.Scatter(
            x=[m["release_date"]],
            y=[m.get("overall", 0)],
            mode="markers+text",
            name=m["name"],
            text=[m["name"]],
            textposition="top center",
            marker=dict(size=14, color=col_(i), symbol="diamond",
                        line=dict(color="#eeeef8", width=1)),
            textfont=dict(color="#eeeef8", family="JetBrains Mono", size=10)
        ))
    fig.update_layout(
        **pd_(),
        height=320,
        showlegend=False,
        xaxis=dict(title="Release Date", **gs_(), titlefont=dict(color="#5a5a80")),
        yaxis=dict(title="Overall Score", **gs_(), titlefont=dict(color="#5a5a80"))
    )
    return fig

def score_ring_html(score, color, size=80):
    r = (size - 10) / 2
    circ = 2 * math.pi * r
    dash = circ * (score / 100)
    return (
        f'<svg width="{size}" height="{size}" class="ring-svg">'
        f'<circle cx="{size/2}" cy="{size/2}" r="{r}" fill="none" stroke="#1f1f38" stroke-width="7"/>'
        f'<circle cx="{size/2}" cy="{size/2}" r="{r}" fill="none" stroke="{color}" stroke-width="7" '
        f'stroke-dasharray="{dash:.1f} {circ:.1f}" stroke-linecap="round"/>'
        f'</svg>'
    )

# ═══════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════
for k, v in {
    "models": [],
    "prompt": "",
    "responses": {},
    "weights": {d: 1.0 for d in DIMS}
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ═══════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="padding:.8rem 0 1.2rem">
      <div style="font-family:'Outfit',sans-serif;font-weight:900;font-size:1.3rem;background:linear-gradient(135deg,#7c6fff,#00d4aa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text">🧠 AI Model Arena</div>
      <div style="font-family:'JetBrains Mono',monospace;font-size:.65rem;color:#5a5a80;letter-spacing:.15em;margin-top:.2rem">COMPARE · BENCHMARK · DECIDE</div>
    </div>""", unsafe_allow_html=True)

    cp1, cp2 = st.columns(2)
    if cp1.button("Load Presets", use_container_width=True):
        ps = []
        for p in PRESET_MODELS:
            p2 = p.copy()
            p2["overall"] = compute_overall(p2)
            ps.append(p2)
        st.session_state.models = ps
        st.rerun()
    if cp2.button("Clear All", use_container_width=True):
        st.session_state.models = []
        st.session_state.responses = {}
        st.rerun()

    st.divider()

    with st.expander("➕ Add New Model", expanded=len(st.session_state.models) == 0):
        with st.form("add_form", clear_on_submit=True):
            st.markdown('<p class="section-label">Identity</p>', unsafe_allow_html=True)
            f1, f2 = st.columns(2)
            name = f1.text_input("Model Name*", placeholder="GPT-4o")
            provider = f2.text_input("Provider", placeholder="OpenAI")
            f3, f4 = st.columns(2)
            version = f3.text_input("Version", placeholder="2024-11")
            category = f4.selectbox("Category", ["General","Code","Vision","Audio","Multimodal","Reasoning","Embedding"])
            release_date = st.text_input("Release Date", placeholder="YYYY-MM-DD")
            license_type = st.selectbox("License", ["Proprietary","Open Source","Research","Mixed"])
            modalities = st.multiselect("Modalities", ["Text","Image","Audio","Video","Code"], default=["Text"])
            tags = st.text_input("Tags (comma-separated)", placeholder="flagship, coding, fast")

            st.markdown('<p class="section-label" style="margin-top:.8rem">Performance (0–100)</p>', unsafe_allow_html=True)
            g1, g2 = st.columns(2)
            accuracy    = g1.slider("Accuracy", 0, 100, 75)
            speed       = g2.slider("Speed", 0, 100, 70)
            reasoning   = g1.slider("Reasoning", 0, 100, 75)
            creativity  = g2.slider("Creativity", 0, 100, 65)
            safety      = g1.slider("Safety", 0, 100, 80)
            cost_eff    = g2.slider("Cost Efficiency", 0, 100, 65)
            multilingual= g1.slider("Multilingual", 0, 100, 70)
            instruction = g2.slider("Instruction Following", 0, 100, 75)

            st.markdown('<p class="section-label" style="margin-top:.8rem">Benchmarks (%)</p>', unsafe_allow_html=True)
            b1, b2, b3 = st.columns(3)
            mmlu      = b1.number_input("MMLU", 0.0, 100.0, 0.0, 0.1)
            gsm8k     = b2.number_input("GSM8K", 0.0, 100.0, 0.0, 0.1)
            humaneval = b3.number_input("HumanEval", 0.0, 100.0, 0.0, 0.1)

            st.markdown('<p class="section-label" style="margin-top:.8rem">Pricing ($/1M tokens)</p>', unsafe_allow_html=True)
            p1, p2 = st.columns(2)
            price_in  = p1.number_input("Input", 0.0, 9999.0, 5.0, step=0.1, format="%.2f")
            price_out = p2.number_input("Output", 0.0, 9999.0, 15.0, step=0.1, format="%.2f")
            context   = st.number_input("Context Window (tokens)", 0, 10_000_000, 128000, 1000)

            st.markdown('<p class="section-label" style="margin-top:.8rem">Content</p>', unsafe_allow_html=True)
            public_resp   = st.text_area("Public Response / Output", height=90, placeholder="Paste model output…")
            notes         = st.text_area("Notes", height=60, placeholder="Key observations…")
            benchmark_txt = st.text_input("Benchmark Summary", placeholder="MMLU: 88.5 | HumanEval: 90%")

            if st.form_submit_button("Add to Arena ➜", use_container_width=True):
                if not name.strip():
                    st.error("Model name required.")
                else:
                    m = dict(
                        name=name.strip(), provider=provider, version=version, category=category,
                        release_date=release_date, license=license_type, modalities=modalities,
                        tags=[t.strip() for t in tags.split(",") if t.strip()],
                        accuracy=accuracy, speed=speed, reasoning=reasoning, creativity=creativity,
                        safety=safety, cost_eff=cost_eff, multilingual=multilingual, instruction=instruction,
                        mmlu=mmlu, gsm8k=gsm8k, humaneval=humaneval,
                        price_in=price_in, price_out=price_out, context=context,
                        open_source=license_type == "Open Source",
                        public_resp=public_resp, notes=notes, benchmark=benchmark_txt,
                        added_at=datetime.now().strftime("%Y-%m-%d %H:%M")
                    )
                    m["overall"] = compute_overall(m)
                    st.session_state.models.append(m)
                    st.success(f"✓ {name} added!")
                    st.rerun()

    if st.session_state.models:
        with st.expander("⚖️ Custom Score Weights"):
            st.caption("Adjust metric importance for ranking")
            for d, label in zip(DIMS, DIM_LABELS):
                st.session_state.weights[d] = st.slider(
                    label, 0.0, 3.0,
                    float(st.session_state.weights.get(d, 1.0)),
                    0.1, key=f"w_{d}"
                )
            if st.button("Apply Weights", use_container_width=True):
                w = st.session_state.weights
                total = sum(w.values()) or 1
                for m in st.session_state.models:
                    m["overall"] = round(sum(m.get(d, 0) * w[d] / total * 8 for d in DIMS), 1)
                st.rerun()

# ═══════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════
models = st.session_state.models

st.markdown("""
<div style="text-align:center;padding:2rem 0 1.5rem">
  <div class="hero-title">🧠 AI Model Arena</div>
  <div class="hero-sub">BENCHMARK · COMPARE · VISUALIZE · DECIDE</div>
</div>""", unsafe_allow_html=True)

if not models:
    st.markdown("""
    <div style="text-align:center;padding:5rem 2rem;color:#5a5a80">
      <div style="font-size:5rem">🤖</div>
      <div style="font-family:'Outfit',sans-serif;font-size:1.8rem;font-weight:800;color:#eeeef8;margin:.6rem 0">Arena is empty</div>
      <div style="font-family:'JetBrains Mono',monospace;font-size:.82rem">Use the sidebar to add models or click Load Presets</div>
    </div>""", unsafe_allow_html=True)
    st.stop()

sorted_models = sorted(models, key=lambda m: m["overall"], reverse=True)
winner = sorted_models[0]

# Hero strip
license_chip = "green" if winner.get("open_source") else "yellow"
benchmark_html = (
    f"<div style='margin-top:.8rem;font-family:JetBrains Mono,monospace;font-size:.78rem;"
    f"color:#8888b0;border-top:1px solid #1f1f38;padding-top:.8rem'>{winner.get('benchmark','')}</div>"
    if winner.get("benchmark") else ""
)
st.markdown(f"""
<div class="glass-card" style="border-color:#7c6fff;margin-bottom:1.5rem;background:linear-gradient(135deg,rgba(124,111,255,.07),rgba(0,212,170,.04))">
  <div style="display:flex;align-items:center;gap:1.5rem;flex-wrap:wrap">
    <div>
      <div class="section-label">🏆 Arena Leader</div>
      <div style="font-family:'Outfit',sans-serif;font-weight:900;font-size:2rem;color:#eeeef8;line-height:1.1">{winner["name"]}</div>
      <div style="font-family:'JetBrains Mono',monospace;font-size:.72rem;color:#5a5a80;margin-top:.2rem">{winner.get("provider","")} · {winner.get("version","")} · {winner.get("category","")}</div>
      <div class="tag-row">
        {"".join([f'<span class="glow-chip chip-purple">{t}</span>' for t in winner.get("tags",[])])}
        {"".join([f'<span class="glow-chip chip-blue">{mod}</span>' for mod in winner.get("modalities",[])])}
        <span class="glow-chip chip-{license_chip}">{winner.get("license","")}</span>
      </div>
    </div>
    <div style="margin-left:auto;display:flex;gap:2.5rem;flex-wrap:wrap;align-items:center">
      {score_ring_html(min(winner["overall"],100),"#7c6fff",90)}
      <div style="text-align:center">
        <div style="font-family:'Outfit',sans-serif;font-weight:900;font-size:2.5rem;color:#7c6fff;line-height:1">{winner["overall"]}</div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:.65rem;color:#5a5a80">OVERALL</div>
      </div>
      <div style="display:flex;flex-direction:column;gap:.6rem">
        <div><span style="font-family:'JetBrains Mono',monospace;font-size:.65rem;color:#5a5a80">ACCURACY</span><span style="font-family:'Outfit',sans-serif;font-weight:800;font-size:1.2rem;color:#00d4aa;margin-left:.5rem">{winner.get("accuracy",0)}</span></div>
        <div><span style="font-family:'JetBrains Mono',monospace;font-size:.65rem;color:#5a5a80">CONTEXT</span><span style="font-family:'Outfit',sans-serif;font-weight:800;font-size:1.2rem;color:#ffb340;margin-left:.5rem">{winner.get("context",0)//1000}K</span></div>
        <div><span style="font-family:'JetBrains Mono',monospace;font-size:.65rem;color:#5a5a80">IN $/1M</span><span style="font-family:'Outfit',sans-serif;font-weight:800;font-size:1.2rem;color:#ff5e7d;margin-left:.5rem">${winner.get("price_in",0):.2f}</span></div>
      </div>
    </div>
  </div>
  {benchmark_html}
</div>""", unsafe_allow_html=True)

# KPIs
kc = st.columns(6)
kc[0].metric("Models", len(models))
kc[1].metric("Leader Score", f"{winner['overall']}")
kc[2].metric("Avg Accuracy", f"{sum(m.get('accuracy',0) for m in models)/len(models):.1f}")
kc[3].metric("Lowest Cost", f"${min(m.get('price_in',999) for m in models):.2f}/1M")
kc[4].metric("Max Context", f"{max(m.get('context',0) for m in models)//1000}K")
kc[5].metric("Open Source", sum(1 for m in models if m.get("open_source")))

st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════
tabs = st.tabs(["📊 Leaderboard","🕸 Radar & Heat","📈 Analytics","💰 Cost Lab",
                "💬 Responses","⚔️ Head-to-Head","📅 Timeline","🔬 Deep Dive","📋 Full Data"])

# ── TAB 0: LEADERBOARD ──────────────────────────────
with tabs[0]:
    st.markdown('<p class="section-label" style="margin-top:.5rem">RANKED LEADERBOARD</p>', unsafe_allow_html=True)
    for rank, m in enumerate(sorted_models):
        color = col_(rank)
        pct = min(int(m["overall"]), 100)
        medal = ["🥇","🥈","🥉"][rank] if rank < 3 else f"#{rank+1}"
        ring = score_ring_html(pct, color, 52)
        badge_html = '<span class="glow-chip chip-green" style="font-size:.7rem">👑 LEADER</span>' if rank == 0 else ""
        if m.get("open_source"):
            badge_html += '<span class="glow-chip chip-blue" style="font-size:.65rem">OSS</span>'
        tag_html = "".join([f'<span class="glow-chip chip-purple" style="font-size:.63rem">{t}</span>' for t in m.get("tags",[])])
        mod_html = "".join([f'<span class="glow-chip chip-yellow" style="font-size:.63rem">{mod}</span>' for mod in m.get("modalities",[])])
        dim_mini = "".join([
            f'<div style="flex:1;min-width:60px">'
            f'<div style="font-family:JetBrains Mono,monospace;font-size:.6rem;color:#5a5a80;margin-bottom:.2rem">{l[:5].upper()}</div>'
            f'<div class="rank-bar"><div class="rank-bar-fill" style="width:{m.get(d,0)}%;background:{color}"></div></div></div>'
            for d, l in zip(DIMS[:6], DIM_LABELS[:6])
        ])
        border_color = "#7c6fff" if rank == 0 else "#1f1f38"
        st.markdown(f"""
        <div class="glass-card" style="margin-bottom:.8rem;padding:1rem 1.4rem;border-color:{border_color}">
          <div style="display:flex;align-items:center;gap:1rem;flex-wrap:wrap">
            <div style="font-size:1.4rem;min-width:2rem;text-align:center">{medal}</div>
            {ring}
            <div style="flex:1;min-width:140px">
              <div style="font-family:'Outfit',sans-serif;font-weight:800;font-size:1.05rem;color:#eeeef8;display:flex;align-items:center;gap:.4rem">{m["name"]} {badge_html}</div>
              <div style="font-family:'JetBrains Mono',monospace;font-size:.68rem;color:#5a5a80;margin:.2rem 0">{m.get("provider","")} · {m.get("version","")} · {m.get("category","")}</div>
              <div style="display:flex;gap:.25rem;flex-wrap:wrap">{tag_html}{mod_html}</div>
            </div>
            <div style="flex:3;min-width:280px;display:flex;flex-direction:column;gap:.4rem">
              <div style="display:flex;align-items:center;gap:.8rem">
                <div class="rank-bar" style="flex:1;height:10px"><div class="rank-bar-fill" style="width:{pct}%;background:linear-gradient(90deg,{color},{color}88)"></div></div>
                <span style="font-family:'Outfit',sans-serif;font-weight:900;font-size:1.3rem;color:{color};min-width:2.5rem">{m["overall"]}</span>
              </div>
              <div style="display:flex;gap:.4rem;flex-wrap:wrap">{dim_mini}</div>
            </div>
            <div style="display:flex;flex-direction:column;gap:.3rem;min-width:100px;text-align:right">
              <span style="font-family:'JetBrains Mono',monospace;font-size:.7rem;color:#5a5a80">Context</span>
              <span style="font-family:'Outfit',sans-serif;font-weight:800;font-size:1.1rem">{m.get("context",0)//1000}K</span>
              <span style="font-family:'JetBrains Mono',monospace;font-size:.7rem;color:#ff5e7d">${m.get("price_in",0):.2f}/1M</span>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

    bench_data = [m for m in sorted_models if m.get("mmlu",0)>0 or m.get("gsm8k",0)>0 or m.get("humaneval",0)>0]
    if bench_data:
        st.markdown('<p class="section-label" style="margin-top:1.5rem">BENCHMARK SCORES</p>', unsafe_allow_html=True)
        fig_b = go.Figure()
        for bench, bc in [("mmlu","#7c6fff"),("gsm8k","#00d4aa"),("humaneval","#ffb340")]:
            fig_b.add_trace(go.Bar(
                name=bench.upper(),
                x=[m["name"] for m in bench_data],
                y=[m.get(bench, 0) for m in bench_data],
                marker_color=bc,
                text=[f"{m.get(bench,0):.1f}" for m in bench_data],
                textposition="outside",
                textfont=dict(color="#eeeef8", size=10)
            ))
        fig_b.update_layout(
            barmode="group", **pd_(), height=300,
            yaxis=dict(range=[0,115], **gs_()),
            xaxis=dict(tickfont=dict(color="#eeeef8", size=10)),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#eeeef8"))
        )
        st.plotly_chart(fig_b, use_container_width=True, config={"displayModeBar": False})

# ── TAB 1: RADAR & HEAT ─────────────────────────────
with tabs[1]:
    cr, ch = st.columns([1, 1])
    with cr:
        st.markdown('<p class="section-label">RADAR CHART</p>', unsafe_allow_html=True)
        sel_r = st.multiselect(
            "Models",
            [m["name"] for m in models],
            default=[m["name"] for m in models[:min(4, len(models))]],
            key="radar_sel"
        )
        selected_radar = [m for m in models if m["name"] in sel_r]
        if selected_radar:
            st.plotly_chart(make_radar(selected_radar), use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Select at least one model to display the radar chart.")
    with ch:
        st.markdown('<p class="section-label">PERFORMANCE HEATMAP</p>', unsafe_allow_html=True)
        st.plotly_chart(make_heatmap(sorted_models), use_container_width=True, config={"displayModeBar": False})

# ── TAB 2: ANALYTICS ────────────────────────────────
with tabs[2]:
    st.markdown('<p class="section-label">PER-METRIC BREAKDOWN</p>', unsafe_allow_html=True)
    for row_i in range(2):
        cols_row = st.columns(4)
        for col_i in range(4):
            dim_idx = row_i * 4 + col_i
            if dim_idx < len(DIMS):
                d, l = DIMS[dim_idx], DIM_LABELS[dim_idx]
                with cols_row[col_i]:
                    st.plotly_chart(make_bar(sorted_models, d, l), use_container_width=True, config={"displayModeBar": False})

    if len(models) >= 2:
        st.markdown('<p class="section-label" style="margin-top:1rem">PARALLEL COORDINATES</p>', unsafe_allow_html=True)
        df_par = pd.DataFrame([{**{d: m.get(d,0) for d in DIMS}, "overall": m.get("overall",0)} for m in models])
        fig_par = go.Figure(go.Parcoords(
            line=dict(color=df_par["overall"],
                      colorscale=[[0,"#1f1f38"],[0.5,"#7c6fff"],[1,"#00d4aa"]],
                      showscale=True),
            dimensions=[dict(label=l, values=df_par[d]) for d, l in zip(DIMS, DIM_LABELS)] +
                       [dict(label="Overall", values=df_par["overall"])]
        ))
        fig_par.update_layout(**pd_(), height=320)
        st.plotly_chart(fig_par, use_container_width=True, config={"displayModeBar": False})

# ── TAB 3: COST LAB ─────────────────────────────────
with tabs[3]:
    cl1, cl2 = st.columns([3, 2])
    with cl1:
        st.markdown('<p class="section-label">VALUE MAP: COST VS. SCORE</p>', unsafe_allow_html=True)
        st.plotly_chart(make_bubble(sorted_models), use_container_width=True, config={"displayModeBar": False})
    with cl2:
        st.markdown('<p class="section-label">COST EFFICIENCY RANKING</p>', unsafe_allow_html=True)
        for i, m in enumerate(sorted(models, key=lambda m: m.get("cost_eff",0), reverse=True)):
            pct = m.get("cost_eff", 0)
            c = col_(i)
            st.markdown(
                f'<div style="margin-bottom:.7rem">'
                f'<div style="display:flex;justify-content:space-between;margin-bottom:.25rem">'
                f'<span style="font-family:JetBrains Mono,monospace;font-size:.78rem">{m["name"]}</span>'
                f'<span style="font-family:Outfit,sans-serif;font-weight:800;color:{c}">{pct}</span></div>'
                f'<div class="rank-bar"><div class="rank-bar-fill" style="width:{pct}%;background:{c}"></div></div></div>',
                unsafe_allow_html=True
            )

    st.markdown('<p class="section-label">PRICING COMPARISON ($/1M TOKENS)</p>', unsafe_allow_html=True)
    sp = sorted(models, key=lambda m: m.get("price_in", 0))
    fig_p = go.Figure()
    fig_p.add_trace(go.Bar(
        name="Input $/1M", x=[m["name"] for m in sp], y=[m.get("price_in",0) for m in sp],
        marker_color="#7c6fff",
        text=[f'${m.get("price_in",0):.2f}' for m in sp],
        textposition="outside", textfont=dict(color="#eeeef8", size=10)
    ))
    fig_p.add_trace(go.Bar(
        name="Output $/1M", x=[m["name"] for m in sp], y=[m.get("price_out",0) for m in sp],
        marker_color="#00d4aa",
        text=[f'${m.get("price_out",0):.2f}' for m in sp],
        textposition="outside", textfont=dict(color="#eeeef8", size=10)
    ))
    fig_p.update_layout(
        barmode="group", **pd_(), height=300,
        yaxis=dict(**gs_()),
        xaxis=dict(tickfont=dict(color="#eeeef8", size=10)),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#eeeef8"))
    )
    st.plotly_chart(fig_p, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<p class="section-label" style="margin-top:1rem">💡 COST CALCULATOR</p>', unsafe_allow_html=True)
    cc1, cc2, cc3, cc4 = st.columns(4)
    in_tok   = cc1.number_input("Input Tokens", 0, 10_000_000, 10_000, 1000)
    out_tok  = cc2.number_input("Output Tokens", 0, 10_000_000, 2_000, 500)
    calls    = cc3.number_input("Calls/Day", 1, 1_000_000, 100, 10)
    days_sel = cc4.selectbox("Period", ["Day","Week","Month","Year"])
    mult = {"Day":1,"Week":7,"Month":30,"Year":365}[days_sel]
    num_calc_cols = min(5, len(models))
    calc_cols = st.columns(num_calc_cols)
    for i, m in enumerate(sorted_models[:num_calc_cols]):
        per_call = (in_tok/1_000_000 * m.get("price_in",0)) + (out_tok/1_000_000 * m.get("price_out",0))
        total = per_call * calls * mult
        c = col_(i)
        with calc_cols[i]:
            st.markdown(
                f'<div class="glass-card" style="text-align:center;border-color:{c};padding:1rem">'
                f'<div style="font-family:Outfit,sans-serif;font-weight:800;color:{c};font-size:.9rem">{m["name"]}</div>'
                f'<div style="font-family:Outfit,sans-serif;font-weight:900;font-size:1.9rem;color:{c};line-height:1.1;margin:.3rem 0">${total:.2f}</div>'
                f'<div style="font-family:JetBrains Mono,monospace;font-size:.65rem;color:#5a5a80">per {days_sel.lower()}</div>'
                f'<div style="font-family:JetBrains Mono,monospace;font-size:.65rem;color:#5a5a80;margin-top:.3rem">'
                f'${per_call*calls:.2f}/day · ${per_call*calls*365:.0f}/year</div></div>',
                unsafe_allow_html=True
            )

# ── TAB 4: RESPONSES ────────────────────────────────
with tabs[4]:
    st.markdown('<p class="section-label">SHARED PROMPT</p>', unsafe_allow_html=True)
    prompt = st.text_area("Prompt used to test all models", value=st.session_state.prompt,
                           placeholder="What is the speed of light?", height=80)
    st.session_state.prompt = prompt
    if prompt.strip():
        st.markdown(
            f'<div class="glass-card" style="margin-bottom:1rem;border-color:#7c6fff">'
            f'<div style="font-family:JetBrains Mono,monospace;font-size:.65rem;color:#5a5a80;margin-bottom:.4rem;letter-spacing:.1em">PROMPT</div>'
            f'<div style="font-family:Outfit,sans-serif;font-size:.95rem;color:#c8c8e8">{prompt}</div></div>',
            unsafe_allow_html=True
        )

    with st.expander("➕ Log a Response", expanded=False):
        rl1, rl2, rl3 = st.columns(3)
        log_model   = rl1.selectbox("Model", [m["name"] for m in models], key="log_m")
        log_latency = rl2.number_input("Latency (ms)", 0, 120000, 500)
        log_tokens  = rl3.number_input("Tokens Used", 0, 100000, 500)
        log_text    = st.text_area("Response Text", height=110, placeholder="Paste the model response…")
        log_rating  = st.slider("Quality (1–10)", 1, 10, 7, key="log_rating")
        log_notes   = st.text_input("Notes", placeholder="e.g. Hallucinated dates, great formatting…")
        if st.button("Log Response", key="log_btn"):
            if log_text.strip():
                key = prompt or "general"
                st.session_state.responses.setdefault(key, []).append(dict(
                    model=log_model, response=log_text, latency=log_latency,
                    tokens=log_tokens, rating=log_rating, notes=log_notes,
                    ts=datetime.now().strftime("%H:%M:%S")
                ))
                st.success("Logged!")
                st.rerun()
            else:
                st.warning("Paste a response first.")

    resp_models = [m for m in models if m.get("public_resp","").strip()]
    if resp_models:
        st.markdown('<p class="section-label" style="margin-top:1rem">MODEL OUTPUTS</p>', unsafe_allow_html=True)
        cols_r = st.columns(min(2, len(resp_models)))
        for i, m in enumerate(resp_models):
            c = col_(models.index(m))
            benchmark_part = (
                f"<div style='margin-top:.6rem;font-family:JetBrains Mono,monospace;font-size:.7rem;color:#5a5a80'>{m.get('benchmark','')}</div>"
                if m.get("benchmark") else ""
            )
            notes_part = (
                f"<div style='margin-top:.4rem;font-family:JetBrains Mono,monospace;font-size:.7rem;color:#8888b0'>{m.get('notes','')}</div>"
                if m.get("notes") else ""
            )
            with cols_r[i % 2]:
                st.markdown(
                    f'<div class="glass-card" style="border-color:{c};margin-bottom:1rem">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.7rem">'
                    f'<span style="font-family:Outfit,sans-serif;font-weight:800;color:{c}">{m["name"]}</span>'
                    f'<span style="font-family:JetBrains Mono,monospace;font-size:.68rem;color:#5a5a80">{m.get("provider","")}</span></div>'
                    f'<div style="background:var(--s1);border-radius:10px;padding:.9rem;font-family:JetBrains Mono,monospace;'
                    f'font-size:.78rem;color:#c8c8e8;line-height:1.7;white-space:pre-wrap;max-height:200px;overflow:auto">{m["public_resp"]}</div>'
                    f'{benchmark_part}{notes_part}</div>',
                    unsafe_allow_html=True
                )

    if st.session_state.responses:
        st.markdown('<p class="section-label" style="margin-top:1rem">LOGGED SESSIONS</p>', unsafe_allow_html=True)
        for prompt_key, entries in st.session_state.responses.items():
            with st.expander(f"📌 {prompt_key[:80]}"):
                cols_e = st.columns(min(3, len(entries)))
                for j, e in enumerate(entries):
                    mi = next((idx for idx, m in enumerate(models) if m["name"] == e["model"]), j)
                    c = col_(mi)
                    notes_e = (
                        f"<div style='font-family:JetBrains Mono,monospace;font-size:.68rem;color:#5a5a80;margin-top:.4rem'>{e['notes']}</div>"
                        if e.get("notes") else ""
                    )
                    with cols_e[j % len(cols_e)]:
                        st.markdown(
                            f'<div class="glass-card" style="border-color:{c}">'
                            f'<div style="display:flex;justify-content:space-between;margin-bottom:.5rem">'
                            f'<span style="font-family:Outfit,sans-serif;font-weight:800;color:{c}">{e["model"]}</span>'
                            f'<span style="font-family:JetBrains Mono,monospace;font-size:.65rem;color:#5a5a80">{e["ts"]}</span></div>'
                            f'<div style="background:var(--s1);border-radius:8px;padding:.7rem;font-family:JetBrains Mono,monospace;'
                            f'font-size:.75rem;color:#c8c8e8;line-height:1.6;white-space:pre-wrap;max-height:140px;overflow:auto">'
                            f'{e["response"][:400]}{"…" if len(e["response"])>400 else ""}</div>'
                            f'<div style="display:flex;gap:.3rem;margin-top:.5rem;flex-wrap:wrap">'
                            f'<span class="glow-chip chip-purple">⭐ {e["rating"]}/10</span>'
                            f'<span class="glow-chip chip-green">⚡ {e["latency"]}ms</span>'
                            f'<span class="glow-chip chip-yellow">🪙 {e["tokens"]} tok</span></div>'
                            f'{notes_e}</div>',
                            unsafe_allow_html=True
                        )

# ── TAB 5: HEAD-TO-HEAD ─────────────────────────────
with tabs[5]:
    if len(models) < 2:
        st.warning("Add at least 2 models.")
    else:
        hh1, hh2 = st.columns(2)
        m1n = hh1.selectbox("Model A", [m["name"] for m in models], key="hha")
        remaining = [m["name"] for m in models if m["name"] != m1n]
        if not remaining:
            st.warning("Need at least 2 different models.")
        else:
            m2n = hh2.selectbox("Model B", remaining, key="hhb")
            ma = next(m for m in models if m["name"] == m1n)
            mb = next(m for m in models if m["name"] == m2n)
            ca = col_(models.index(ma))
            cb = col_(models.index(mb))
            wins_a = wins_b = 0
            rows_hh = []
            for d, l in zip(DIMS, DIM_LABELS):
                va, vb = ma.get(d, 0), mb.get(d, 0)
                if va > vb: wins_a += 1
                elif vb > va: wins_b += 1
                rows_hh.append((l, va, vb))

            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:0;margin:1rem 0 1.5rem">
              <div class="glass-card" style="flex:1;text-align:center;border-color:{ca}">
                <div style="font-family:'Outfit',sans-serif;font-weight:900;font-size:1.5rem;color:{ca}">{ma["name"]}</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:.7rem;color:#5a5a80">{ma.get("provider","")}</div>
                <div style="font-family:'Outfit',sans-serif;font-weight:900;font-size:2rem;color:{ca};margin-top:.3rem">{ma.get("overall",0)}</div>
              </div>
              <div class="vs-divider" style="padding:0 1.5rem">VS</div>
              <div class="glass-card" style="flex:1;text-align:center;border-color:{cb}">
                <div style="font-family:'Outfit',sans-serif;font-weight:900;font-size:1.5rem;color:{cb}">{mb["name"]}</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:.7rem;color:#5a5a80">{mb.get("provider","")}</div>
                <div style="font-family:'Outfit',sans-serif;font-weight:900;font-size:2rem;color:{cb};margin-top:.3rem">{mb.get("overall",0)}</div>
              </div>
            </div>""", unsafe_allow_html=True)

            for label, va, vb in rows_hh:
                win_a = va > vb
                win_b = vb > va
                style_a = f"color:{ca};font-weight:700" if win_a else "color:#5a5a80"
                style_b = f"color:{cb};font-weight:700" if win_b else "color:#5a5a80"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:.8rem;margin-bottom:.6rem">
                  <div style="flex:1;text-align:right">
                    <div style="height:8px;background:var(--border);border-radius:4px;overflow:hidden;display:flex;justify-content:flex-end"><div style="width:{va}%;height:100%;background:{ca};border-radius:4px"></div></div>
                    <span style="font-family:'JetBrains Mono',monospace;font-size:.72rem;{style_a}">{va}</span>
                  </div>
                  <div style="min-width:90px;text-align:center;font-family:'JetBrains Mono',monospace;font-size:.7rem;color:#5a5a80">{label}</div>
                  <div style="flex:1">
                    <div style="height:8px;background:var(--border);border-radius:4px;overflow:hidden"><div style="width:{vb}%;height:100%;background:{cb};border-radius:4px"></div></div>
                    <span style="font-family:'JetBrains Mono',monospace;font-size:.72rem;{style_b}">{vb}</span>
                  </div>
                </div>""", unsafe_allow_html=True)

            st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)
            v1, v2 = st.columns(2)
            for col_w, mn, wins, other_wins, col_c in [(v1, m1n, wins_a, wins_b, ca), (v2, m2n, wins_b, wins_a, cb)]:
                icon = "🏆" if wins > other_wins else "🤝" if wins == other_wins else "🥈"
                is_w = wins > other_wins
                winner_badge = "<div class='glow-chip chip-green' style='margin-top:.5rem;font-size:.8rem'>WINNER 🏆</div>" if is_w else ""
                border = col_c if is_w else "#1f1f38"
                with col_w:
                    st.markdown(
                        f'<div class="glass-card" style="text-align:center;border-color:{border}">'
                        f'<div style="font-size:2rem">{icon}</div>'
                        f'<div style="font-family:Outfit,sans-serif;font-weight:800;font-size:1.1rem;color:{col_c}">{mn}</div>'
                        f'<div style="font-family:JetBrains Mono,monospace;font-size:.8rem;color:#5a5a80">{wins} dimension wins</div>'
                        f'{winner_badge}</div>',
                        unsafe_allow_html=True
                    )

            st.markdown('<p class="section-label" style="margin-top:1.2rem">RADAR OVERLAY</p>', unsafe_allow_html=True)
            st.plotly_chart(make_radar([ma, mb]), use_container_width=True, config={"displayModeBar": False})

            st.markdown('<p class="section-label">SPEC SHEET</p>', unsafe_allow_html=True)
            specs = [
                ("Context", f"{ma.get('context',0)//1000}K", f"{mb.get('context',0)//1000}K"),
                ("Input $/1M", f"${ma.get('price_in',0):.2f}", f"${mb.get('price_in',0):.2f}"),
                ("Output $/1M", f"${ma.get('price_out',0):.2f}", f"${mb.get('price_out',0):.2f}"),
                ("License", ma.get("license","—"), mb.get("license","—")),
                ("Release", ma.get("release_date","—"), mb.get("release_date","—")),
                ("Category", ma.get("category","—"), mb.get("category","—")),
            ]
            st.dataframe(pd.DataFrame(specs, columns=["Spec", ma["name"], mb["name"]]),
                         use_container_width=True, hide_index=True)

# ── TAB 6: TIMELINE ─────────────────────────────────
with tabs[6]:
    st.markdown('<p class="section-label">RELEASE TIMELINE</p>', unsafe_allow_html=True)
    tl_fig = make_timeline(models)
    if tl_fig:
        st.plotly_chart(tl_fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("Add release dates to models to see the timeline.")
    tl_data = sorted([m for m in models if m.get("release_date")], key=lambda m: m["release_date"])
    if tl_data:
        st.markdown('<p class="section-label" style="margin-top:1rem">CHRONOLOGICAL ORDER</p>', unsafe_allow_html=True)
        for m in tl_data:
            c = col_(models.index(m))
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:1rem;padding:.6rem 0;border-bottom:1px solid var(--border)">'
                f'<span class="timeline-dot" style="background:{c}"></span>'
                f'<span style="font-family:JetBrains Mono,monospace;font-size:.8rem;color:#5a5a80;min-width:90px">{m["release_date"]}</span>'
                f'<span style="font-family:Outfit,sans-serif;font-weight:700;color:{c}">{m["name"]}</span>'
                f'<span style="font-family:JetBrains Mono,monospace;font-size:.72rem;color:#5a5a80">{m.get("provider","")}</span>'
                f'<span class="glow-chip chip-purple" style="margin-left:auto">{m.get("overall",0)}</span></div>',
                unsafe_allow_html=True
            )

# ── TAB 7: DEEP DIVE ────────────────────────────────
with tabs[7]:
    st.markdown('<p class="section-label">SELECT MODEL FOR DEEP DIVE</p>', unsafe_allow_html=True)
    dive_name = st.selectbox("Model", [m["name"] for m in models], key="dive_sel")
    dm = next(m for m in models if m["name"] == dive_name)
    dc = col_(models.index(dm))

    dd1, dd2, dd3 = st.columns([2, 1, 1])
    with dd1:
        license_chip_dm = "green" if dm.get("open_source") else "yellow"
        st.markdown(f"""
        <div class="glass-card" style="border-color:{dc}">
          <div style="font-family:'Outfit',sans-serif;font-weight:900;font-size:1.6rem;color:{dc}">{dm["name"]}</div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:.72rem;color:#5a5a80;margin:.2rem 0">{dm.get("provider","")} · {dm.get("version","")} · {dm.get("category","")}</div>
          <div class="tag-row">
            {"".join([f'<span class="glow-chip chip-purple">{t}</span>' for t in dm.get("tags",[])])}
            {"".join([f'<span class="glow-chip chip-blue">{mod}</span>' for mod in dm.get("modalities",[])])}
            <span class="glow-chip chip-{license_chip_dm}">{dm.get("license","")}</span>
          </div>
          <div style="margin-top:1rem;font-family:'JetBrains Mono',monospace;font-size:.78rem;color:#8888b0;line-height:1.7">{dm.get("notes","No notes.")}</div>
        </div>""", unsafe_allow_html=True)
    with dd2:
        st.markdown('<p class="section-label">PERFORMANCE</p>', unsafe_allow_html=True)
        for d, l in zip(DIMS, DIM_LABELS):
            val = dm.get(d, 0)
            st.markdown(
                f'<div style="margin-bottom:.5rem">'
                f'<div style="display:flex;justify-content:space-between;margin-bottom:.15rem">'
                f'<span style="font-family:JetBrains Mono,monospace;font-size:.7rem;color:#5a5a80">{l}</span>'
                f'<span style="font-family:Outfit,sans-serif;font-weight:700;color:{dc}">{val}</span></div>'
                f'<div class="rank-bar"><div class="rank-bar-fill" style="width:{val}%;background:{dc}"></div></div></div>',
                unsafe_allow_html=True
            )
    with dd3:
        st.markdown('<p class="section-label">SPECS</p>', unsafe_allow_html=True)
        specs_dd = [
            ("Overall Score", str(dm.get("overall","—"))),
            ("Context", f"{dm.get('context',0)//1000}K tokens"),
            ("Input Cost", f"${dm.get('price_in',0):.2f}/1M"),
            ("Output Cost", f"${dm.get('price_out',0):.2f}/1M"),
            ("Release Date", dm.get("release_date","—")),
            ("MMLU", f"{dm.get('mmlu',0):.1f}%" if dm.get("mmlu") else "—"),
            ("GSM8K", f"{dm.get('gsm8k',0):.1f}%" if dm.get("gsm8k") else "—"),
            ("HumanEval", f"{dm.get('humaneval',0):.1f}%" if dm.get("humaneval") else "—"),
        ]
        for label, val in specs_dd:
            st.markdown(
                f'<div style="display:flex;justify-content:space-between;padding:.35rem 0;border-bottom:1px solid var(--border)">'
                f'<span style="font-family:JetBrains Mono,monospace;font-size:.7rem;color:#5a5a80">{label}</span>'
                f'<span style="font-family:Outfit,sans-serif;font-weight:700;font-size:.85rem;color:#eeeef8">{val}</span></div>',
                unsafe_allow_html=True
            )

    if len(models) > 1:
        st.markdown('<p class="section-label" style="margin-top:1.2rem">VS. FIELD RADAR</p>', unsafe_allow_html=True)
        field_models = [dm] + [m for m in sorted_models[:4] if m["name"] != dm["name"]]
        st.plotly_chart(make_radar(field_models), use_container_width=True, config={"displayModeBar": False})

    if dm.get("public_resp"):
        st.markdown('<p class="section-label" style="margin-top:1rem">SAMPLE RESPONSE</p>', unsafe_allow_html=True)
        st.markdown(
            f'<div style="background:var(--s1);border:1px solid var(--border);border-radius:12px;padding:1rem;'
            f'font-family:JetBrains Mono,monospace;font-size:.82rem;color:#c8c8e8;line-height:1.7;white-space:pre-wrap">'
            f'{dm["public_resp"]}</div>',
            unsafe_allow_html=True
        )

# ── TAB 8: FULL DATA ────────────────────────────────
with tabs[8]:
    st.markdown('<p class="section-label">FULL COMPARISON TABLE</p>', unsafe_allow_html=True)
    df_full = pd.DataFrame([{
        "Model": m["name"], "Provider": m["provider"], "Version": m.get("version",""),
        "Category": m.get("category",""), "Overall": m["overall"],
        "Accuracy": m.get("accuracy",0), "Speed": m.get("speed",0), "Reasoning": m.get("reasoning",0),
        "Creativity": m.get("creativity",0), "Safety": m.get("safety",0), "Cost Eff.": m.get("cost_eff",0),
        "Multilingual": m.get("multilingual",0), "Instruction": m.get("instruction",0),
        "MMLU %": m.get("mmlu",0), "GSM8K %": m.get("gsm8k",0), "HumanEval %": m.get("humaneval",0),
        "In $/1M": m.get("price_in",0), "Out $/1M": m.get("price_out",0),
        "Context (K)": m.get("context",0)//1000, "License": m.get("license",""),
        "Release": m.get("release_date",""), "OSS": "✅" if m.get("open_source") else "❌",
        "Tags": ", ".join(m.get("tags",[])),
    } for m in sorted_models])

    num_cols = ["Overall","Accuracy","Speed","Reasoning","Creativity","Safety","Cost Eff.","Multilingual","Instruction"]
    st.dataframe(
        df_full.style.background_gradient(subset=num_cols, cmap="Blues"),
        use_container_width=True, hide_index=True, height=420
    )

    dl1, dl2, dl3 = st.columns(3)
    dl1.download_button("⬇ CSV", df_full.to_csv(index=False), "ai_arena.csv", "text/csv", use_container_width=True)
    dl2.download_button("⬇ JSON", json.dumps(models, indent=2), "ai_arena.json", "application/json", use_container_width=True)
    dl3.download_button("⬇ Markdown", df_full.to_markdown(index=False), "ai_arena.md", "text/markdown", use_container_width=True)

    st.markdown('<p class="section-label" style="margin-top:1.5rem">STATISTICAL SUMMARY</p>', unsafe_allow_html=True)
    st.dataframe(
        df_full[num_cols + ["MMLU %","GSM8K %","HumanEval %"]].describe().round(2),
        use_container_width=True
    )

st.markdown("""
<div style="text-align:center;padding:3rem 0 1.5rem;border-top:1px solid #1f1f38;margin-top:2rem">
  <div style="font-family:'JetBrains Mono',monospace;font-size:.65rem;color:#2a2a50;letter-spacing:.15em">
    🧠 AI MODEL ARENA · STREAMLIT + PLOTLY · ALL DATA IS USER-INPUT
  </div>
</div>""", unsafe_allow_html=True)

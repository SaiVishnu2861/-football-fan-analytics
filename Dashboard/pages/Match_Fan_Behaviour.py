from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Match & Fan Behaviour",
    page_icon="🏉",
    layout="wide",
)


# ============================================================
# PATHS + COLOURS
# ============================================================
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "Data"
RAW_DIR = DATA_DIR / "Raw"

YELLOW = "#F5C518"
CHARCOAL = "#111111"
PANEL = "#1B1B1B"
BAR = "#5A5A5A"
TEXT = "#F4F4F4"
MUTED = "#A9A9A9"
GRID = "#333333"


# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data
def load_data():
    matches = pd.read_csv(
        RAW_DIR / "afl_matches_2025.csv"
    )

    member_attendance = pd.read_csv(
        DATA_DIR / "attendance_analysis.csv"
    )

    for df in (matches, member_attendance):
        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

    matches["date"] = pd.to_datetime(
        matches["date"],
        format="%d-%b-%Y",
        errors="coerce",
    )

    return matches, member_attendance


matches, member_attendance = load_data()


# ============================================================
# RICHMOND HOME MATCHES
# ============================================================
richmond_matches = matches[
    matches["home_team"]
    .str.strip()
    .str.lower()
    .eq("richmond")
].copy()

richmond_matches = richmond_matches.sort_values(
    "date"
)

richmond_matches["result"] = richmond_matches.apply(
    lambda row:
        "Win"
        if row["home_score"] > row["away_score"]
        else "Loss"
        if row["home_score"] < row["away_score"]
        else "Draw",
    axis=1,
)

richmond_matches["margin"] = (
    richmond_matches["home_score"]
    - richmond_matches["away_score"]
)

# ============================================================
# STREAMLIT STYLING
# ============================================================
st.markdown(
    f"""
    <style>

    .stApp {{
        background-color: {CHARCOAL};
        color: {TEXT};
    }}

    .block-container {{
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }}

    /* MAIN HEADINGS */
    h1, h2, h3 {{
        color: {TEXT} !important;
        -webkit-text-fill-color: {TEXT} !important;
    }}

    /* KPI CARDS */
    div[data-testid="stMetric"] {{
        background: linear-gradient(145deg, #202020, #191919);
        border: 1px solid #343434;
        border-top: 4px solid {YELLOW};
        padding: 18px 20px;
        border-radius: 12px;
        min-height: 135px;
    }}

    /* KPI LABELS */
    div[data-testid="stMetricLabel"],
    div[data-testid="stMetricLabel"] *,
    div[data-testid="stMetricLabel"] p,
    div[data-testid="stMetricLabel"] div {{
        color: {MUTED} !important;
        -webkit-text-fill-color: {MUTED} !important;
        opacity: 1 !important;
        font-weight: 600 !important;
    }}

    /* KPI VALUES */
    div[data-testid="stMetricValue"],
    div[data-testid="stMetricValue"] *,
    div[data-testid="stMetricValue"] p,
    div[data-testid="stMetricValue"] div {{
        color: {TEXT} !important;
        -webkit-text-fill-color: {TEXT} !important;
        opacity: 1 !important;
        font-weight: 700 !important;
    }}

    /* SUBTITLE */
    .dashboard-subtitle {{
        color: {MUTED} !important;
        -webkit-text-fill-color: {MUTED} !important;
        font-size: 1rem;
        margin-top: -12px;
        margin-bottom: 25px;
    }}

    /* SECTION TITLES */
    .section-title {{
        font-size: 1.35rem;
        font-weight: 700;
        color: {TEXT} !important;
        -webkit-text-fill-color: {TEXT} !important;
        border-left: 5px solid {YELLOW};
        padding-left: 12px;
        margin-top: 22px;
        margin-bottom: 12px;
    }}

    /* INSIGHT BOXES */
    .insight-box {{
        background: linear-gradient(145deg, #202020, #191919);
        border: 1px solid #343434;
        border-radius: 10px;
        padding: 20px 24px;
        color: {TEXT} !important;
        -webkit-text-fill-color: {TEXT} !important;
        line-height: 1.6;
        margin-top: 10px;
        margin-bottom: 18px;
    }}

    .insight-box b {{
        color: {TEXT} !important;
        -webkit-text-fill-color: {TEXT} !important;
    }}

    /* DATA DISCLOSURE */
    .disclosure-box {{
        background: linear-gradient(145deg, #202020, #191919);
        border: 1px solid #343434;
        border-radius: 10px;
        padding: 20px 24px;
        margin-top: 28px;
        color: {MUTED} !important;
        -webkit-text-fill-color: {MUTED} !important;
        font-size: 0.88rem;
        line-height: 1.6;
    }}

    .disclosure-title {{
        color: {TEXT} !important;
        -webkit-text-fill-color: {TEXT} !important;
        font-weight: 700;
        margin-bottom: 12px;
    }}

    .disclosure-note {{
        color: #8F8F8F !important;
        -webkit-text-fill-color: #8F8F8F !important;
        margin-top: 12px;
    }}

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# COMMON PLOTLY STYLE
# ============================================================
def style_chart(fig, height=400):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=PANEL,
        plot_bgcolor=PANEL,
        height=height,
        margin=dict(
            l=35,
            r=65,
            t=65,
            b=45,
        ),
        font=dict(
            color=TEXT,
            size=13,
        ),
        title=dict(
            font=dict(
                color=TEXT,
                size=18,
            ),
        ),
        hoverlabel=dict(
            bgcolor="#252525",
            font=dict(
                color=TEXT,
                size=13,
            ),
        ),
        showlegend=False,
    )

    fig.update_xaxes(
        color=MUTED,
        title_font=dict(
            color=MUTED,
            size=14,
        ),
        tickfont=dict(
            color=MUTED,
            size=12,
        ),
        gridcolor=GRID,
        zeroline=False,
        linecolor=GRID,
    )

    fig.update_yaxes(
        color=MUTED,
        title_font=dict(
            color=MUTED,
            size=14,
        ),
        tickfont=dict(
            color=MUTED,
            size=12,
        ),
        gridcolor=GRID,
        zeroline=False,
        linecolor=GRID,
    )

    fig.update_traces(
        textfont=dict(
            color=TEXT,
            size=12,
        )
    )

    return fig


# ============================================================
# HEADER
# ============================================================
st.title("Match & Fan Behaviour")

st.markdown(
    """
    <div class="dashboard-subtitle">
        Richmond home-match performance, stadium attendance and
        simulated member engagement • 2025 Season
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# KPI CALCULATIONS
# ============================================================
home_matches = len(
    richmond_matches
)

avg_stadium_attendance = (
    richmond_matches["attendance"].mean()
)

highest_attendance = (
    richmond_matches["attendance"].max()
)

wins = (
    richmond_matches["result"]
    .eq("Win")
    .sum()
)


# ============================================================
# KPI CARDS
# ============================================================
k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "HOME MATCHES",
    f"{home_matches}",
)

k2.metric(
    "AVG STADIUM ATTENDANCE",
    f"{avg_stadium_attendance:,.0f}",
)

k3.metric(
    "HIGHEST ATTENDANCE",
    f"{highest_attendance:,.0f}",
)

k4.metric(
    "HOME WINS",
    f"{wins}",
)


# ============================================================
# RICHMOND HOME MATCH ENVIRONMENT
# ============================================================
st.markdown(
    """
    <div class="section-title">
        Richmond Home Match Environment
    </div>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns(2)


# ============================================================
# CHART 1 — STADIUM ATTENDANCE BY OPPONENT
# ============================================================
attendance_by_opponent = (
    richmond_matches[
        [
            "away_team",
            "attendance",
        ]
    ]
    .sort_values(
        "attendance",
        ascending=True,
    )
)

max_attendance = (
    attendance_by_opponent["attendance"].max()
)

opponent_colors = [
    YELLOW if value == max_attendance else BAR
    for value in attendance_by_opponent["attendance"]
]

fig_opponent = go.Figure()

fig_opponent.add_trace(
    go.Bar(
        x=attendance_by_opponent["attendance"],
        y=attendance_by_opponent["away_team"],
        orientation="h",
        marker_color=opponent_colors,
        text=[
            f"{x:,.0f}"
            for x in attendance_by_opponent["attendance"]
        ],
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "<b>vs %{y}</b><br>"
            "Stadium Attendance: %{x:,.0f}"
            "<extra></extra>"
        ),
    )
)

fig_opponent.update_layout(
    title="Stadium Attendance by Opponent",
)

fig_opponent.update_xaxes(
    title="Attendance",
    range=[
        0,
        max_attendance * 1.16,
    ],
)

fig_opponent.update_yaxes(
    title=None,
)

style_chart(
    fig_opponent,
    height=455,
)

left.plotly_chart(
    fig_opponent,
    use_container_width=True,
)


# ============================================================
# CHART 2 — ATTENDANCE THROUGH THE SEASON
# ============================================================
fig_season = go.Figure()

fig_season.add_trace(
    go.Scatter(
        x=richmond_matches["date"],
        y=richmond_matches["attendance"],
        mode="lines+markers",
        line=dict(
            color=YELLOW,
            width=3,
        ),
        marker=dict(
            size=9,
            color=YELLOW,
        ),
        customdata=richmond_matches[
            [
                "away_team",
                "result",
                "home_score",
                "away_score",
            ]
        ],
        hovertemplate=(
            "<b>%{x|%d %b 2025}</b><br>"
            "Opponent: %{customdata[0]}<br>"
            "Attendance: %{y:,.0f}<br>"
            "Result: %{customdata[1]}<br>"
            "Score: %{customdata[2]}–%{customdata[3]}"
            "<extra></extra>"
        ),
    )
)

fig_season.update_layout(
    title="Home Attendance Through the Season",
)

fig_season.update_xaxes(
    title=None,
)

fig_season.update_yaxes(
    title="Attendance",
)

style_chart(
    fig_season,
    height=455,
)

right.plotly_chart(
    fig_season,
    use_container_width=True,
)


# ============================================================
# MATCH PERFORMANCE
# ============================================================
st.markdown(
    """
    <div class="section-title">
        Match Performance
    </div>
    """,
    unsafe_allow_html=True,
)

performance = (
    richmond_matches
    .sort_values(
        "margin",
        ascending=True,
    )
)

performance_colors = [
    YELLOW if result == "Win" else BAR
    for result in performance["result"]
]

fig_margin = go.Figure()

fig_margin.add_trace(
    go.Bar(
        x=performance["margin"],
        y=performance["away_team"],
        orientation="h",
        marker_color=performance_colors,
        text=[
            f"{margin:+.0f}"
            for margin in performance["margin"]
        ],
        textposition="outside",
        cliponaxis=False,
        customdata=performance[
            [
                "home_score",
                "away_score",
                "result",
                "attendance",
            ]
        ],
        hovertemplate=(
            "<b>vs %{y}</b><br>"
            "Margin: %{x:+.0f}<br>"
            "Richmond: %{customdata[0]}<br>"
            "Opponent: %{customdata[1]}<br>"
            "Result: %{customdata[2]}<br>"
            "Attendance: %{customdata[3]:,.0f}"
            "<extra></extra>"
        ),
    )
)

max_margin = max(
    abs(performance["margin"].min()),
    abs(performance["margin"].max()),
)

fig_margin.update_layout(
    title="Match Result Margin by Opponent",
)

fig_margin.update_xaxes(
    title="Score Margin",
    range=[
        -max_margin * 1.20,
        max_margin * 1.20,
    ],
    zeroline=True,
    zerolinecolor="#888888",
    zerolinewidth=1,
)

fig_margin.update_yaxes(
    title=None,
)

style_chart(
    fig_margin,
    height=480,
)

st.plotly_chart(
    fig_margin,
    use_container_width=True,
)


# ============================================================
# MATCH ENGAGEMENT PROFILE
# ============================================================
st.markdown(
    """
    <div class="section-title">
        Match Engagement Profile
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SUMMARISE SIMULATED MEMBER ATTENDANCE
# ============================================================
member_match = (
    member_attendance
    .groupby(
        "away_team",
        as_index=False,
    )["member_id"]
    .nunique()
    .rename(
        columns={
            "member_id": "members_attending"
        }
    )
)


# ============================================================
# JOIN PUBLIC MATCH DATA + SIMULATED CRM DATA
# ============================================================
match_profile = pd.merge(
    richmond_matches[
        [
            "away_team",
            "attendance",
        ]
    ],
    member_match,
    on="away_team",
    how="left",
)


# ============================================================
# CREATE RELATIVE INDEXES
#
# 100 = SEASON AVERAGE FOR EACH METRIC
# ============================================================
match_profile["crowd_index"] = (
    match_profile["attendance"]
    / match_profile["attendance"].mean()
    * 100
)

match_profile["member_index"] = (
    match_profile["members_attending"]
    / match_profile["members_attending"].mean()
    * 100
)

match_profile = (
    match_profile
    .sort_values(
        "crowd_index",
        ascending=True,
    )
)


# ============================================================
# CHART 4 — PUBLIC CROWD VS SIMULATED MEMBER ENGAGEMENT
# ============================================================
fig_profile = go.Figure()

fig_profile.add_trace(
    go.Bar(
        y=match_profile["away_team"],
        x=match_profile["crowd_index"],
        name="Public Crowd Index",
        orientation="h",
        marker_color=YELLOW,
        customdata=match_profile[
            ["attendance"]
        ],
        hovertemplate=(
            "<b>vs %{y}</b><br>"
            "Crowd Index: %{x:.0f}<br>"
            "Stadium Attendance: %{customdata[0]:,.0f}"
            "<extra></extra>"
        ),
    )
)

fig_profile.add_trace(
    go.Bar(
        y=match_profile["away_team"],
        x=match_profile["member_index"],
        name="Simulated Member Index",
        orientation="h",
        marker_color=BAR,
        customdata=match_profile[
            ["members_attending"]
        ],
        hovertemplate=(
            "<b>vs %{y}</b><br>"
            "Member Index: %{x:.0f}<br>"
            "Simulated Members Attending: %{customdata[0]:,.0f}"
            "<extra></extra>"
        ),
    )
)

fig_profile.add_vline(
    x=100,
    line_width=1,
    line_dash="dash",
    line_color="#AAAAAA",
    annotation_text="Season Average",
    annotation_position="top",
    annotation_font_color=MUTED,
)

fig_profile.update_layout(
    title=(
        "Public Crowd Demand vs "
        "Simulated Member Engagement"
    ),
    barmode="group",
)

fig_profile.update_xaxes(
    title=(
        "Engagement Index "
        "(100 = Season Average)"
    ),
)

fig_profile.update_yaxes(
    title=None,
)

style_chart(
    fig_profile,
    height=540,
)

fig_profile.update_layout(
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(
            color=TEXT,
            size=12,
        ),
    ),
)

st.plotly_chart(
    fig_profile,
    use_container_width=True,
)


# ============================================================
# MODEL OBSERVATION
# ============================================================
st.markdown(
    """<div class="insight-box">
<b>How to read the engagement profile:</b><br><br>
Each measure is indexed against its own season average. An index of <b>100 represents an average Richmond home match</b> for that metric.<br><br>
Public stadium demand varies substantially between fixtures, while simulated member attendance remains comparatively stable.<br><br>
This is an important modelling observation rather than a finding about Richmond members. The synthetic attendance model does not include a strong opponent-specific demand effect.
</div>""",
    unsafe_allow_html=True,
)


# ============================================================
# WHAT THIS PAGE DEMONSTRATES
# ============================================================
st.markdown(
    """<div class="section-title">What This Page Demonstrates</div>""",
    unsafe_allow_html=True,
)

st.markdown(
    """<div class="insight-box">
<b>Match demand:</b> Public stadium attendance varies considerably across Richmond's 2025 home fixtures, with the strongest crowd observed against Carlton.<br><br>
<b>Performance context:</b> Match results and scoring margins provide an additional layer for interpreting the home-match environment rather than viewing attendance in isolation.<br><br>
<b>CRM integration:</b> Simulated member attendance records are joined to real fixture-level data to demonstrate how internal CRM behaviour could be analysed alongside external match information.<br><br>
<b>Model limitation:</b> The simulated attendance model produces relatively stable match-level engagement. A more advanced model could incorporate opponent attractiveness, fixture timing, venue characteristics, recent team performance and other match-level drivers.
</div>""",
    unsafe_allow_html=True,
)


# ============================================================
# DATA DISCLOSURE
# ============================================================
st.markdown(
    """<div class="disclosure-box">
<div class="disclosure-title">Data Disclosure</div>
Match fixtures, scores, venues and stadium attendance are derived from publicly available AFL Tables data.<br><br>
Member and CRM behaviour is simulated for portfolio demonstration purposes. No proprietary Richmond Football Club data is used.
<div class="disclosure-note">Simulated behaviour should not be interpreted as actual Richmond member behaviour or as evidence of a causal relationship with real stadium attendance.</div>
</div>""",
    unsafe_allow_html=True,
)
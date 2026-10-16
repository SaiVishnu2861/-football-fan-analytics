from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# CONFIG
# ============================================================
st.set_page_config(
    page_title="AFL Member Intelligence",
    page_icon="🏉",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "Data"

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
    members = pd.read_csv(DATA_DIR / "member_360.csv")
    attendance = pd.read_csv(DATA_DIR / "attendance_analysis.csv")
    transactions = pd.read_csv(DATA_DIR / "transaction_analysis.csv")

    for df in (members, attendance, transactions):
        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

    return members, attendance, transactions


members, attendance, transactions = load_data()


def bool_to_int(series):
    if pd.api.types.is_bool_dtype(series):
        return series.astype(int)

    return (
        series.astype(str)
        .str.strip()
        .str.lower()
        .map({
            "true": 1,
            "false": 0,
            "1": 1,
            "0": 0,
            "yes": 1,
            "no": 0,
        })
    )


members["renewed_numeric"] = bool_to_int(
    members["renewed_2026"]
)

# ============================================================
# STREAMLIT STYLING
# ============================================================
st.markdown(
    f"""
    <style>

    /* ========================================================
       APP BACKGROUND
       ======================================================== */
    .stApp {{
        background-color: {CHARCOAL};
        color: {TEXT};
    }}

    .block-container {{
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }}


    /* ========================================================
       MAIN HEADINGS
       ======================================================== */
    h1, h2, h3 {{
        color: {TEXT} !important;
        -webkit-text-fill-color: {TEXT} !important;
    }}


    /* ========================================================
       KPI CARDS
       ======================================================== */
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


    /* ========================================================
       DASHBOARD SUBTITLE
       ======================================================== */
    .dashboard-subtitle {{
        color: {MUTED} !important;
        -webkit-text-fill-color: {MUTED} !important;
        font-size: 1rem;
        margin-top: -12px;
        margin-bottom: 25px;
    }}


    /* ========================================================
       SECTION HEADERS
       ======================================================== */
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


    /* ========================================================
       INSIGHT CARDS
       ======================================================== */
    .insight-card {{
        background: linear-gradient(145deg, #202020, #191919);
        border: 1px solid #343434;
        border-radius: 10px;
        padding: 18px 20px;
        height: 100%;
    }}

    .insight-heading {{
        color: {YELLOW} !important;
        -webkit-text-fill-color: {YELLOW} !important;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        margin-bottom: 7px;
    }}

    .insight-text {{
        color: {TEXT} !important;
        -webkit-text-fill-color: {TEXT} !important;
        font-size: 0.95rem;
        line-height: 1.5;
    }}


    /* ========================================================
       GENERAL INSIGHT BOX — USED ON PAGE 2
       ======================================================== */
    .insight-box {{
        background: linear-gradient(145deg, #202020, #191919);
        border: 1px solid #343434;
        border-radius: 10px;
        padding: 20px 24px;
        margin-top: 10px;
        margin-bottom: 22px;
        color: {TEXT} !important;
        -webkit-text-fill-color: {TEXT} !important;
        font-size: 0.95rem;
        line-height: 1.6;
    }}

    .insight-box b {{
        color: {TEXT} !important;
        -webkit-text-fill-color: {TEXT} !important;
        font-weight: 700;
    }}


    /* ========================================================
       PAGE 2 DATA DISCLOSURE BOX
       ======================================================== */
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
        font-size: 0.95rem;
        margin-bottom: 12px;
    }}

    .disclosure-note {{
        color: #888888 !important;
        -webkit-text-fill-color: #888888 !important;
        margin-top: 14px;
    }}


    /* ========================================================
       PAGE 1 FOOTER DISCLOSURE
       ======================================================== */
    .disclaimer {{
        color: {MUTED} !important;
        -webkit-text-fill-color: {MUTED} !important;
        font-size: 0.8rem;
        line-height: 1.5;
        margin-top: 32px;
        border-top: 1px solid #333333;
        padding-top: 15px;
    }}

    .disclaimer b {{
        color: {TEXT} !important;
        -webkit-text-fill-color: {TEXT} !important;
    }}

    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# COMMON PLOTLY STYLE
# ============================================================
def style_chart(fig, height=380):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=PANEL,
        plot_bgcolor=PANEL,
        height=height,
        margin=dict(
            l=30,
            r=65,
            t=65,
            b=40,
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
                size=14,
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
# SIDEBAR
# ============================================================
st.sidebar.title("Dashboard Filters")

tier_order = [
    "Bronze",
    "Silver",
    "Gold",
    "Premium",
]

available_tiers = [
    tier
    for tier in tier_order
    if tier in members["membership_tier"].unique()
]

selected_tiers = st.sidebar.multiselect(
    "Membership Tier",
    available_tiers,
    default=available_tiers,
)

if not selected_tiers:
    st.sidebar.warning(
        "Select at least one membership tier."
    )
    st.stop()

filtered = members[
    members["membership_tier"].isin(selected_tiers)
].copy()

st.sidebar.markdown("---")

st.sidebar.caption(
    "Filters update member-level KPIs and retention/value analysis. "
    "Revenue category totals represent the full simulated transaction dataset."
)


# ============================================================
# HEADER
# ============================================================
st.title("AFL Member Intelligence")

st.markdown(
    """
    <div class="dashboard-subtitle">
        Member engagement, retention and commercial performance
        • 2025 portfolio case study
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# KPI CARDS
# ============================================================
total_members = filtered["member_id"].nunique()

renewal_rate = (
    filtered["renewed_numeric"].mean()
)

avg_spend = (
    filtered["total_spend"].mean()
)

avg_matches = (
    filtered["matches_attended"].mean()
)

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "TOTAL MEMBERS",
    f"{total_members:,}",
)

k2.metric(
    "RENEWAL RATE",
    f"{renewal_rate:.1%}",
)

k3.metric(
    "AVG SPEND / MEMBER",
    f"${avg_spend:,.2f}",
)

k4.metric(
    "AVG MATCHES ATTENDED",
    f"{avg_matches:.1f}",
)


# ============================================================
# MEMBER ENGAGEMENT & RETENTION
# ============================================================
st.markdown(
    '<div class="section-title">Member Engagement & Retention</div>',
    unsafe_allow_html=True,
)

c1, c2 = st.columns(2)


# ============================================================
# RENEWAL BY TIER
# ============================================================
renewal_tier = (
    filtered
    .groupby(
        "membership_tier",
        as_index=False,
    )["renewed_numeric"]
    .mean()
)

renewal_tier["membership_tier"] = pd.Categorical(
    renewal_tier["membership_tier"],
    categories=tier_order,
    ordered=True,
)

renewal_tier = renewal_tier.sort_values(
    "membership_tier"
)

tier_colors = [
    YELLOW if tier == "Premium" else BAR
    for tier in renewal_tier["membership_tier"]
]

fig_tier = go.Figure()

fig_tier.add_trace(
    go.Bar(
        x=renewal_tier["renewed_numeric"],
        y=renewal_tier["membership_tier"],
        orientation="h",
        marker_color=tier_colors,
        text=[
            f"{x:.1%}"
            for x in renewal_tier["renewed_numeric"]
        ],
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Renewal Rate: %{x:.1%}"
            "<extra></extra>"
        ),
    )
)

fig_tier.update_layout(
    title="Renewal Rate by Membership Tier",
)

fig_tier.update_xaxes(
    title="Renewal Rate",
    tickformat=".0%",
    range=[0, 0.80],
)

fig_tier.update_yaxes(
    title=None,
)

style_chart(fig_tier)

c1.plotly_chart(
    fig_tier,
    use_container_width=True,
)


# ============================================================
# ATTENDANCE VS RENEWAL
# ============================================================
def attendance_group(x):
    if x == 0:
        return "0"
    elif x <= 3:
        return "1–3"
    elif x <= 6:
        return "4–6"
    elif x <= 9:
        return "7–9"
    return "10+"


filtered["attendance_group"] = (
    filtered["matches_attended"].apply(
        attendance_group
    )
)

attendance_order = [
    "0",
    "1–3",
    "4–6",
    "7–9",
    "10+",
]

attendance_retention = (
    filtered
    .groupby(
        "attendance_group",
        as_index=False,
    )["renewed_numeric"]
    .mean()
)

attendance_retention["attendance_group"] = pd.Categorical(
    attendance_retention["attendance_group"],
    categories=attendance_order,
    ordered=True,
)

attendance_retention = (
    attendance_retention
    .sort_values("attendance_group")
)

attendance_colors = [
    YELLOW if group == "10+" else BAR
    for group in attendance_retention["attendance_group"]
]

fig_attendance = go.Figure()

fig_attendance.add_trace(
    go.Bar(
        x=attendance_retention["attendance_group"],
        y=attendance_retention["renewed_numeric"],
        marker_color=attendance_colors,
        text=[
            f"{x:.1%}"
            for x in attendance_retention["renewed_numeric"]
        ],
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "<b>%{x} matches</b><br>"
            "Renewal Rate: %{y:.1%}"
            "<extra></extra>"
        ),
    )
)

fig_attendance.update_layout(
    title="Attendance & Renewal",
)

fig_attendance.update_xaxes(
    title="Matches Attended",
)

fig_attendance.update_yaxes(
    title="Renewal Rate",
    tickformat=".0%",
    range=[0, 0.80],
)

style_chart(fig_attendance)

c2.plotly_chart(
    fig_attendance,
    use_container_width=True,
)


# ============================================================
# ENGAGEMENT VS RENEWAL
# ============================================================
def engagement_group(row):
    score = 0

    if row["email_open_rate"] >= 0.50:
        score += 1

    if row["app_sessions"] >= filtered["app_sessions"].median():
        score += 1

    if row["matches_attended"] >= 6:
        score += 1

    if score <= 1:
        return "Low"

    elif score == 2:
        return "Medium"

    return "High"


filtered["engagement_level"] = filtered.apply(
    engagement_group,
    axis=1,
)

engagement_order = [
    "Low",
    "Medium",
    "High",
]

engagement_retention = (
    filtered
    .groupby(
        "engagement_level",
        as_index=False,
    )["renewed_numeric"]
    .mean()
)

engagement_retention["engagement_level"] = pd.Categorical(
    engagement_retention["engagement_level"],
    categories=engagement_order,
    ordered=True,
)

engagement_retention = (
    engagement_retention
    .sort_values("engagement_level")
)

engagement_colors = [
    YELLOW if level == "High" else BAR
    for level in engagement_retention["engagement_level"]
]

fig_engagement = go.Figure()

fig_engagement.add_trace(
    go.Bar(
        x=engagement_retention["engagement_level"],
        y=engagement_retention["renewed_numeric"],
        marker_color=engagement_colors,
        text=[
            f"{x:.1%}"
            for x in engagement_retention["renewed_numeric"]
        ],
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "<b>%{x} Engagement</b><br>"
            "Renewal Rate: %{y:.1%}"
            "<extra></extra>"
        ),
    )
)

fig_engagement.update_layout(
    title="Engagement Level & Renewal",
)

fig_engagement.update_xaxes(
    title="Engagement Level",
)

fig_engagement.update_yaxes(
    title="Renewal Rate",
    tickformat=".0%",
    range=[0, 0.80],
)

style_chart(
    fig_engagement,
    height=350,
)

st.plotly_chart(
    fig_engagement,
    use_container_width=True,
)


# ============================================================
# COMMERCIAL PERFORMANCE
# ============================================================
st.markdown(
    '<div class="section-title">Commercial Performance</div>',
    unsafe_allow_html=True,
)

c3, c4 = st.columns(2)


# ============================================================
# MEMBER VALUE
# ============================================================
member_value = (
    filtered
    .groupby(
        "membership_tier",
        as_index=False,
    )["total_spend"]
    .mean()
)

member_value["membership_tier"] = pd.Categorical(
    member_value["membership_tier"],
    categories=tier_order,
    ordered=True,
)

member_value = member_value.sort_values(
    "membership_tier"
)

value_colors = [
    YELLOW if tier == "Premium" else BAR
    for tier in member_value["membership_tier"]
]

fig_value = go.Figure()

fig_value.add_trace(
    go.Bar(
        x=member_value["total_spend"],
        y=member_value["membership_tier"],
        orientation="h",
        marker_color=value_colors,
        text=[
            f"${x:,.0f}"
            for x in member_value["total_spend"]
        ],
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Average Spend: $%{x:,.2f}"
            "<extra></extra>"
        ),
    )
)

max_value = member_value["total_spend"].max()

fig_value.update_layout(
    title="Average Member Value by Tier",
)

fig_value.update_xaxes(
    title="Average Spend per Member",
    tickprefix="$",
    range=[0, max_value * 1.22],
)

fig_value.update_yaxes(
    title=None,
)

style_chart(fig_value)

c3.plotly_chart(
    fig_value,
    use_container_width=True,
)


# ============================================================
# REVENUE BY CATEGORY
# ============================================================
revenue_category = (
    transactions
    .groupby(
        "category",
        as_index=False,
    )["amount"]
    .sum()
    .sort_values(
        "amount",
        ascending=True,
    )
)

max_revenue = (
    revenue_category["amount"].max()
)

revenue_colors = [
    YELLOW if amount == max_revenue else BAR
    for amount in revenue_category["amount"]
]

fig_revenue = go.Figure()

fig_revenue.add_trace(
    go.Bar(
        x=revenue_category["amount"],
        y=revenue_category["category"],
        orientation="h",
        marker_color=revenue_colors,
        text=[
            f"${x / 1000:,.0f}K"
            for x in revenue_category["amount"]
        ],
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Revenue: $%{x:,.0f}"
            "<extra></extra>"
        ),
    )
)

fig_revenue.update_layout(
    title="Revenue by Category",
)

fig_revenue.update_xaxes(
    title="Simulated Revenue",
    tickprefix="$",
    range=[
        0,
        max_revenue * 1.20,
    ],
)

fig_revenue.update_yaxes(
    title=None,
)

style_chart(fig_revenue)

c4.plotly_chart(
    fig_revenue,
    use_container_width=True,
)


# ============================================================
# KEY INSIGHTS
# ============================================================
st.markdown(
    '<div class="section-title">Key Insights</div>',
    unsafe_allow_html=True,
)

i1, i2, i3, i4 = st.columns(4)

with i1:
    st.markdown(
        """
        <div class="insight-card">
            <div class="insight-heading">RETENTION</div>
            <div class="insight-text">
                Premium members show the strongest simulated renewal rate,
                indicating higher retention among upper membership tiers.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with i2:
    st.markdown(
        """
        <div class="insight-card">
            <div class="insight-heading">ATTENDANCE</div>
            <div class="insight-text">
                Members attending 10+ matches show the highest renewal rate,
                suggesting a positive association between attendance and retention.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with i3:
    st.markdown(
        """
        <div class="insight-card">
            <div class="insight-heading">MEMBER VALUE</div>
            <div class="insight-text">
                Premium members generate the highest average spend per member,
                while Bronze contributes value through its larger member base.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with i4:
    st.markdown(
        """
        <div class="insight-card">
            <div class="insight-heading">COMMERCIAL MIX</div>
            <div class="insight-text">
                Merchandise is the largest simulated transaction revenue category,
                substantially exceeding other commercial categories.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# DISCLOSURE
# ============================================================
st.markdown(
    """
    <div class="disclaimer">
        <b>Data disclosure:</b>
        Independent portfolio project using publicly available
        AFL match data from AFL Tables and simulated CRM/member data.
        No proprietary Richmond Football Club data is used.
        Simulated relationships are illustrative and should not
        be interpreted as causal findings.
    </div>
    """,
    unsafe_allow_html=True,
)
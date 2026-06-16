import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# ── Page setup ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Uber Cancellation Analysis",
    page_icon="🚗",
    layout="wide",
)

# ── Color palette ──────────────────────────────────────────────────────────────
GREEN  = "#1DB954"
RED    = "#FF4B4B"
ORANGE = "#F5A623"
PURPLE = "#8B5CF6"
BLUE   = "#3B82F6"

# ── Shared Plotly layout ───────────────────────────────────────────────────────
def base_layout(**kwargs):
    layout = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="sans-serif", color="#8A94A6", size=12),
        showlegend=False,
        margin=dict(l=10, r=40, t=30, b=10),
    )
    layout.update(kwargs)
    return layout


def x_axis(**kwargs):
    ax = dict(showgrid=False, zeroline=False,
              tickfont=dict(color="#C4CDD9", size=12))
    ax.update(kwargs)
    return ax


def y_axis(**kwargs):
    ax = dict(showgrid=True, gridcolor="#1A2230", gridwidth=1,
              zeroline=False, tickfont=dict(color="#C4CDD9", size=12))
    ax.update(kwargs)
    return ax


def chart_config():
    return {"displayModeBar": False, "responsive": True}


# ── Data ───────────────────────────────────────────────────────────────────────
# City cancellation rates — sorted ascending for horizontal bar
city_cancel_sorted = pd.DataFrame({
    "City":          ["Chicago", "Los Angeles", "Houston", "New York", "Miami"],
    "Cancel Rate":   [32.26, 33.33, 33.33, 35.29, 44.00],
    "Color":         [GREEN, BLUE, ORANGE, PURPLE, RED],
})

# City revenue loss — sorted ascending for horizontal bar
city_rev_sorted = pd.DataFrame({
    "City":         ["Chicago", "Houston", "Los Angeles", "Miami", "New York"],
    "Revenue Lost": [215.5, 219.0, 227.5, 262.0, 268.0],
})

eta_buckets = ["0–5 min", "6–10 min", "11–15 min", "16+ min"]
eta_rates   = [12.50, 30.00, 42.86, 60.00]

surge_levels = ["No Surge", "Low Surge", "Medium Surge", "High Surge"]
surge_rates  = [5.88, 22.92, 72.50, 90.91]
surge_colors = [GREEN, BLUE, ORANGE, RED]

reason_labels = ["Long ETA", "High Price", "Other"]
reason_counts = [28, 15, 10]
reason_colors = [RED, ORANGE, BLUE]

risk_matrix = pd.DataFrame({
    "Segment":        [
        "Low ETA + Low Surge",
        "High ETA + Low Surge",
        "Low ETA + High Surge",
        "High ETA + High Surge",
    ],
    "Cancel Rate (%)": [10.77, 20.59, 66.67, 80.56],
    "Risk Level":      ["Low", "Moderate", "High", "Critical"],
})


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — HERO HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.title("🚗 The Cancellation Tipping Point")
st.subheader("When does a rider become likely to cancel an Uber ride?")
st.caption(
    "Uber Operations Intelligence  ·  150 rides across 5 cities  ·  "
    "Analysing the combined effect of wait time and surge pricing on cancellation risk"
)
st.divider()


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — KPI CARDS
# ══════════════════════════════════════════════════════════════════════════════
st.subheader("📊 Executive Overview")
st.caption("The scale of the problem at a glance.")
st.write("")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Rides",       "150",    help="Total rides in the dataset")
col2.metric("Cancellations",     "53",     delta="-53 rides lost",   delta_color="inverse")
col3.metric("Cancellation Rate", "35.33%", delta="1 in 3 abandoned", delta_color="inverse")
col4.metric("Revenue Lost",      "$1,192", delta="Estimated total",  delta_color="inverse")

st.divider()


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — CITY ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
st.subheader("🏙️ City-Level Analysis")
st.caption(
    "Not all cities are equal. Miami leads on cancellation rate, "
    "while New York generates the highest revenue loss."
)
st.write("")

col_left, col_right = st.columns(2)

# ── Chart: Cancellation rate by city ──
with col_left:
    st.markdown("**Cancellation Rate by City**")
    fig_city_rate = go.Figure(go.Bar(
        x=city_cancel_sorted["Cancel Rate"],
        y=city_cancel_sorted["City"],
        orientation="h",
        marker=dict(color=city_cancel_sorted["Color"].tolist(), line=dict(width=0)),
        text=[f"{v:.1f}%" for v in city_cancel_sorted["Cancel Rate"]],
        textposition="outside",
        textfont=dict(color="white", size=13),
        hovertemplate="<b>%{y}</b><br>Cancel Rate: %{x:.1f}%<extra></extra>",
    ))
    fig_city_rate.update_layout(
        **base_layout(height=280),
        xaxis=x_axis(showticklabels=False, range=[0, 58]),
        yaxis=y_axis(showgrid=False),
    )
    st.plotly_chart(fig_city_rate, use_container_width=True, config=chart_config())
    st.info(
        "⚠️ **Miami** has the highest cancellation rate at 44% — "
        "nearly 1 in 2 rides are abandoned. This points to a "
        "localised supply or pricing issue requiring targeted action."
    )

# ── Chart: Revenue loss by city ──
with col_right:
    st.markdown("**Revenue Loss by City**")
    fig_rev = go.Figure(go.Bar(
        x=city_rev_sorted["Revenue Lost"],
        y=city_rev_sorted["City"],
        orientation="h",
        marker=dict(color=PURPLE, opacity=0.85, line=dict(width=0)),
        text=[f"${v}" for v in city_rev_sorted["Revenue Lost"]],
        textposition="outside",
        textfont=dict(color="white", size=13),
        hovertemplate="<b>%{y}</b><br>Revenue Lost: $%{x}<extra></extra>",
    ))
    fig_rev.update_layout(
        **base_layout(height=280),
        xaxis=x_axis(showticklabels=False, range=[0, 340]),
        yaxis=y_axis(showgrid=False),
    )
    st.plotly_chart(fig_rev, use_container_width=True, config=chart_config())
    st.info(
        "💡 **New York** leads on revenue loss at $268 — driven by "
        "higher average fares. Even a modest cancellation reduction "
        "in NY would recover more revenue than any other city."
    )

st.divider()


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — CANCELLATION REASONS
# ══════════════════════════════════════════════════════════════════════════════
st.subheader("❓ Why Are Riders Cancelling?")
st.caption(
    "Over 80% of cancellations trace back to controllable factors — "
    "ETA and pricing. Both can be addressed through operational levers."
)
st.write("")

col_donut, col_bars = st.columns([1, 1.4])

with col_donut:
    fig_donut = go.Figure(go.Pie(
        labels=reason_labels,
        values=reason_counts,
        hole=0.60,
        marker=dict(colors=reason_colors, line=dict(color="#0A0C10", width=3)),
        textinfo="label+percent",
        textfont=dict(color="white", size=12),
        hovertemplate="<b>%{label}</b><br>%{value} rides (%{percent})<extra></extra>",
    ))
    fig_donut.update_layout(
        **base_layout(height=300),
        annotations=[dict(
            text="53<br>total",
            x=0.5, y=0.5, showarrow=False, align="center",
            font=dict(color="white", size=16),
        )],
    )
    st.plotly_chart(fig_donut, use_container_width=True, config=chart_config())

with col_bars:
    st.write("")
    st.write("")
    df_reasons = pd.DataFrame({
        "Reason":  reason_labels,
        "Count":   reason_counts,
        "Share":   ["52.8%", "28.3%", "18.9%"],
    })
    st.dataframe(
        df_reasons,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Reason": st.column_config.TextColumn("Cancellation Reason"),
            "Count":  st.column_config.NumberColumn("Rides Cancelled", format="%d"),
            "Share":  st.column_config.TextColumn("Share of Total"),
        },
    )
    st.warning(
        "⚡ **Key Insight:** Long ETA alone accounts for 52.8% of all "
        "cancellations. Combined with High Price (28.3%), controllable "
        "factors drive more than 4 in 5 cancellation events."
    )

st.divider()


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5 — ETA IMPACT
# ══════════════════════════════════════════════════════════════════════════════
st.subheader("⏱️ How Wait Time Drives Cancellations")
st.caption(
    "Cancellation risk rises sharply after ETA exceeds 10 minutes. "
    "Every additional minute beyond that threshold costs Uber a ride."
)
st.write("")

fig_eta = go.Figure()
fig_eta.add_trace(go.Scatter(
    x=eta_buckets,
    y=eta_rates,
    mode="lines+markers",
    name="Cancel Rate",
    line=dict(color=ORANGE, width=3, shape="spline"),
    marker=dict(size=12, color=ORANGE, line=dict(color="white", width=2)),
    fill="tozeroy",
    fillcolor="rgba(245,166,35,0.10)",
    hovertemplate="<b>%{x}</b><br>Cancellation Rate: %{y:.1f}%<extra></extra>",
))
fig_eta.add_hline(
    y=30, line_dash="dot", line_color=RED, line_width=1.5,
    annotation_text="30% — Risk inflection point",
    annotation_position="top right",
    annotation_font_color=RED,
)
fig_eta.update_layout(
    **base_layout(height=340),
    xaxis=x_axis(title="ETA Bucket"),
    yaxis=y_axis(title="Cancellation Rate (%)", ticksuffix="%", range=[0, 75]),
)
st.plotly_chart(fig_eta, use_container_width=True, config=chart_config())

col_e1, col_e2, col_e3, col_e4 = st.columns(4)
col_e1.metric("0–5 min ETA",   "12.5%",  help="Cancellation rate when wait is under 5 min")
col_e2.metric("6–10 min ETA",  "30.0%",  delta="+17.5pp", delta_color="inverse")
col_e3.metric("11–15 min ETA", "42.9%",  delta="+12.9pp", delta_color="inverse")
col_e4.metric("16+ min ETA",   "60.0%",  delta="+17.1pp", delta_color="inverse")

st.error(
    "📈 **Pattern:** Cancellation rate more than doubles when ETA crosses 10 minutes "
    "(12.5% → 30%). At 16+ minutes, 60% of riders abandon the ride. "
    "Keeping ETA below 10 minutes is the single most impactful operational fix."
)
st.divider()


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 6 — SURGE PRICING IMPACT
# ══════════════════════════════════════════════════════════════════════════════
st.subheader("💸 Surge Pricing: An Even Stronger Signal")
st.caption(
    "Surge pricing has a steeper effect on cancellations than ETA. "
    "Riders are extremely price-sensitive once multipliers climb."
)
st.write("")

fig_surge = go.Figure(go.Bar(
    x=surge_levels,
    y=surge_rates,
    marker=dict(color=surge_colors, opacity=0.9, line=dict(width=0)),
    text=[f"{v:.1f}%" for v in surge_rates],
    textposition="outside",
    textfont=dict(color="white", size=13),
    hovertemplate="<b>%{x}</b><br>Cancel Rate: %{y:.1f}%<extra></extra>",
))
fig_surge.update_layout(
    **base_layout(height=340, bargap=0.35),
    xaxis=x_axis(title="Surge Level"),
    yaxis=y_axis(title="Cancellation Rate (%)", ticksuffix="%", range=[0, 108]),
)
st.plotly_chart(fig_surge, use_container_width=True, config=chart_config())

col_s1, col_s2, col_s3, col_s4 = st.columns(4)
col_s1.metric("No Surge",     "5.9%",  help="Baseline cancellation rate")
col_s2.metric("Low Surge",    "22.9%", delta="+17.0pp", delta_color="inverse")
col_s3.metric("Medium Surge", "72.5%", delta="+49.6pp", delta_color="inverse")
col_s4.metric("High Surge",   "90.9%", delta="+18.4pp", delta_color="inverse")

st.error(
    "🔴 **Critical Finding:** High surge pricing produces a 90.9% cancellation rate — "
    "nearly a certainty. Surge pricing outperforms ETA as a risk driver. "
    "Even medium surge (72.5%) is far more damaging than any ETA bucket."
)
st.divider()


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 7 — RISK MATRIX
# ══════════════════════════════════════════════════════════════════════════════
st.subheader("🔥 Highest-Risk Ride Segments")
st.caption(
    "When ETA and surge pricing combine, cancellation risk compounds dramatically. "
    "High surge is the dominant factor — even fast ETAs can't offset it."
)
st.write("")

col_heat, col_table = st.columns([1.2, 1])

with col_heat:
    fig_heat = go.Figure(go.Heatmap(
        z=[[10.77, 66.67], [20.59, 80.56]],
        x=["Low Surge", "High Surge"],
        y=["Low ETA (0–10 min)", "High ETA (11+ min)"],
        colorscale=[
            [0.0, "#0D3B1A"],
            [0.3, GREEN],
            [0.6, ORANGE],
            [1.0, RED],
        ],
        showscale=True,
        colorbar=dict(
            ticksuffix="%",
            tickfont=dict(color="#8A94A6"),
            outlinewidth=0,
        ),
        text=[["10.77%", "66.67%"], ["20.59%", "80.56%"]],
        texttemplate="<b>%{text}</b>",
        textfont=dict(size=18, color="white"),
        hovertemplate="<b>%{y}  ×  %{x}</b><br>Cancel Rate: %{text}<extra></extra>",
    ))
    fig_heat.update_layout(
        **base_layout(height=280, margin=dict(l=10, r=10, t=50, b=10)),
        xaxis=dict(side="top", tickfont=dict(color="#C4CDD9", size=12)),
        yaxis=dict(tickfont=dict(color="#C4CDD9", size=12)),
    )
    st.plotly_chart(fig_heat, use_container_width=True, config=chart_config())

with col_table:
    st.write("")
    st.dataframe(
        risk_matrix,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Segment":         st.column_config.TextColumn("Ride Condition"),
            "Cancel Rate (%)": st.column_config.NumberColumn(
                "Cancel Rate", format="%.2f%%"
            ),
            "Risk Level":      st.column_config.TextColumn("Risk Level"),
        },
    )
    st.error(
        "🔥 **Worst segment:** High ETA + High Surge = **80.56%** cancellation rate. "
        "Notably, Low ETA + High Surge (66.67%) is far worse than "
        "High ETA + Low Surge (20.59%). Surge pricing is the primary lever."
    )

st.divider()


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 8 — RECOMMENDATIONS
# ══════════════════════════════════════════════════════════════════════════════
st.subheader("✅ Business Recommendations")
st.caption("Data-backed actions ranked by potential impact on cancellation reduction and revenue recovery.")
st.write("")

recs = [
    ("01", "Cap effective ETA at 10 minutes",
     "Cancellations more than double past the 10-minute mark. Use geofenced driver "
     "allocation or surge driver incentives to keep ETA below this threshold in "
     "high-demand zones before a request is accepted."),

    ("02", "Redesign surge communication to reduce sticker shock",
     "The 90.9% cancellation rate at high surge is largely a perception problem. "
     "Introduce progressive fare disclosure, price-lock prompts, or surge caps "
     "to reduce the moment of sticker shock that triggers cancellation."),

    ("03", "Deploy a Miami-specific retention playbook",
     "Miami's 44% cancellation rate — the highest of any city — is driven by both "
     "high_price and long_eta reasons. Investigate driver supply gaps and local "
     "fare competitiveness before any broader rollout."),

    ("04", "Trigger real-time interventions at risk thresholds",
     "When ETA > 10 min AND surge is elevated, proactively offer a price lock, "
     "driver update notification, or revised wait estimate. Interrupting the "
     "cancellation decision at the right moment can save the ride."),

    ("05", "Prioritise New York revenue recovery",
     "New York has the highest revenue loss ($268) despite a mid-range cancellation "
     "rate, because its average fares are higher. A 10% cancellation reduction in "
     "New York recovers more revenue than the same improvement in any other city."),
]

for num, title, desc in recs:
    with st.expander(f"**{num} — {title}**", expanded=True):
        st.write(desc)

st.divider()

# ── Footer ─────────────────────────────────────────────────────────────────────
st.caption(
    "Uber Cancellation Intelligence Dashboard\n"
    "Built with PostgreSQL • Python • Streamlit • Plotly"
)
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go


def create_price_chart(ticker: str, hist_data: pd.DataFrame) -> go.Figure:
    """Create a candlestick chart with MA50 and MA200 overlays."""
    fig = go.Figure()

    fig.add_trace(
        go.Candlestick(
            x=hist_data.index,
            open=hist_data["Open"],
            high=hist_data["High"],
            low=hist_data["Low"],
            close=hist_data["Close"],
            name="Price",
        )
    )

    # MA50
    ma50 = hist_data["Close"].rolling(window=50).mean()
    fig.add_trace(
        go.Scatter(
            x=hist_data.index,
            y=ma50,
            name="MA 50",
            line=dict(color="#06b6d4", width=1.5),
        )
    )

    # MA200
    if len(hist_data) >= 200:
        ma200 = hist_data["Close"].rolling(window=200).mean()
        fig.add_trace(
            go.Scatter(
                x=hist_data.index,
                y=ma200,
                name="MA 200",
                line=dict(color="#f59e0b", width=1.5),
            )
        )

    fig.update_layout(
        title=f"{ticker} Price Chart",
        xaxis_title="Date",
        yaxis_title="Price ($)",
        template="plotly_dark",
        xaxis_rangeslider_visible=False,
        height=500,
    )

    return fig


def create_sentiment_pie(
    num_bullish: int, num_bearish: int, num_neutral: int
) -> go.Figure:
    """Create a pie chart for sentiment distribution."""
    fig = go.Figure(
        data=[
            go.Pie(
                labels=["Bullish", "Bearish", "Neutral"],
                values=[num_bullish, num_bearish, num_neutral],
                marker_colors=["#10b981", "#ef4444", "#6b7280"],
                hole=0.4,
                textinfo="label+percent",
            )
        ]
    )

    fig.update_layout(
        title="Sentiment Distribution",
        template="plotly_dark",
        height=400,
        showlegend=True,
    )

    return fig


def create_divergence_gauge(score: int) -> go.Figure:
    """Create a gauge/speedometer chart for the divergence score."""
    # Determine color based on score
    if score <= 20:
        bar_color = "#10b981"
    elif score <= 40:
        bar_color = "#f59e0b"
    elif score <= 60:
        bar_color = "#f97316"
    elif score <= 80:
        bar_color = "#ef4444"
    else:
        bar_color = "#dc2626"

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            title={"text": "Divergence Score", "font": {"size": 16}},
            number={"font": {"size": 36}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1},
                "bar": {"color": bar_color},
                "steps": [
                    {"range": [0, 20], "color": "#064e3b"},
                    {"range": [20, 40], "color": "#78350f"},
                    {"range": [40, 60], "color": "#7c2d12"},
                    {"range": [60, 80], "color": "#7f1d1d"},
                    {"range": [80, 100], "color": "#450a0a"},
                ],
                "threshold": {
                    "line": {"color": "white", "width": 4},
                    "thickness": 0.75,
                    "value": score,
                },
            },
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
    )

    return fig


def create_score_breakdown_radar(breakdown: dict) -> go.Figure:
    """Create a radar/spider chart of 5 scoring components."""
    categories = [
        "Technical\nDivergence",
        "Sentiment\nUniformity",
        "Insider\nActivity",
        "Fundamental\nRisk",
        "Macro\nHeadwinds",
    ]

    values = [
        breakdown.get("technical_divergence", 0),
        breakdown.get("sentiment_uniformity", 0),
        breakdown.get("insider_activity", 0),
        breakdown.get("fundamental_risk", 0),
        breakdown.get("macro_headwinds", 0),
    ]
    # Close the radar
    values.append(values[0])
    categories.append(categories[0])

    fig = go.Figure(
        data=go.Scatterpolar(
            r=values,
            theta=categories,
            fill="toself",
            fillcolor="rgba(124, 58, 237, 0.3)",
            line_color="#7c3aed",
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100]),
            bgcolor="#1e1e2e",
        ),
        title="Score Breakdown",
        template="plotly_dark",
        showlegend=False,
        height=400,
    )

    return fig

from __future__ import annotations

import streamlit as st

from src.config.settings import settings


def render_sidebar() -> dict:
    """Render the Streamlit sidebar and return user selections."""
    with st.sidebar:
        st.markdown("## 🔮 Oracle Settings")
        st.divider()

        # Ticker input
        ticker = st.text_input(
            "Stock Ticker",
            value="NVDA",
            max_chars=5,
            help="Enter a stock ticker symbol (e.g. AAPL, TSLA, MSFT)",
        ).upper()

        st.markdown("🧠 **Powered by:** Groq (8B + 70B Hybrid)")

        st.divider()
        st.markdown("### ⚖️ Score Weights")

        # Weight sliders
        w_technical = st.slider(
            "Technical Divergence",
            min_value=0,
            max_value=100,
            value=int(settings.weight_technical_divergence * 100),
        )
        w_sentiment = st.slider(
            "Sentiment Uniformity",
            min_value=0,
            max_value=100,
            value=int(settings.weight_sentiment_uniformity * 100),
        )
        w_insider = st.slider(
            "Insider Activity",
            min_value=0,
            max_value=100,
            value=int(settings.weight_insider_activity * 100),
        )
        w_fundamental = st.slider(
            "Fundamental Risk",
            min_value=0,
            max_value=100,
            value=int(settings.weight_fundamental_risk * 100),
        )
        w_macro = st.slider(
            "Macro Headwinds",
            min_value=0,
            max_value=100,
            value=int(settings.weight_macro_headwinds * 100),
        )

        st.divider()

        # Run button
        run_clicked = st.button(
            "🚀 Run Contrarian Analysis",
            type="primary",
            width="stretch",
        )

        st.caption(
            "⚠️ **Disclaimer:** Not financial advice. "
            "For educational and research purposes only."
        )

    return {
        "ticker": ticker,
        "run_clicked": run_clicked,
        "weights": {
            "technical_divergence": w_technical / 100,
            "sentiment_uniformity": w_sentiment / 100,
            "insider_activity": w_insider / 100,
            "fundamental_risk": w_fundamental / 100,
            "macro_headwinds": w_macro / 100,
        },
    }

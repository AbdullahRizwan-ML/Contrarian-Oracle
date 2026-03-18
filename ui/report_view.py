from __future__ import annotations

import streamlit as st

from ui.charts import (
    create_divergence_gauge,
    create_score_breakdown_radar,
    create_sentiment_pie,
)


def render_report(report_data: dict) -> None:
    """Render the final report with tabs."""
    tab_bull, tab_bear, tab_technicals, tab_evidence, tab_verdict = st.tabs(
        ["🐂 Bull Case", "🐻 Bear Case", "📊 Technicals", "🔍 Evidence", "⚖️ Verdict"]
    )

    raw = report_data.get("raw_outputs", {})

    # ── Bull Case tab ──────────────────────────────────────────
    with tab_bull:
        st.markdown("### Mainstream Narrative (Bull Case)")
        bull_text = report_data.get("bull_case_summary", "")
        if bull_text:
            st.markdown(bull_text)

        narrative = report_data.get("narrative", {})
        if narrative:
            st.markdown("### Sentiment Overview")
            score = narrative.get("overall_sentiment_score", 0)
            uniformity = narrative.get("sentiment_uniformity", 0)

            col1, col2, col3 = st.columns(3)
            col1.metric("Sentiment Score", f"{score:+.2f}")
            col2.metric("Uniformity", f"{uniformity:.2f}")
            n_bull = narrative.get("num_bullish", 0)
            n_bear = narrative.get("num_bearish", 0)
            n_neut = narrative.get("num_neutral", 0)
            col3.metric("Headlines", f"{n_bull}🟢 {n_bear}🔴 {n_neut}⚪")

            total = n_bull + n_bear + n_neut
            if total > 0:
                st.plotly_chart(
                    create_sentiment_pie(n_bull, n_bear, n_neut),
                    use_container_width=True,
                )

        if raw.get("sentiment"):
            with st.expander("🔍 Raw Agent Output"):
                st.markdown(raw["sentiment"])

    # ── Bear Case tab ──────────────────────────────────────────
    with tab_bear:
        st.markdown("### Contrarian Narrative (Bear Case)")
        contrarian = report_data.get("contrarian", {})

        bear_text = report_data.get("bear_case_summary", "")
        if bear_text:
            st.markdown(bear_text)
        elif contrarian.get("contrarian_narrative"):
            st.markdown(contrarian["contrarian_narrative"])
        else:
            st.info("No parsed bear case summary. See raw output below.")

        st.markdown("### Key Risks")
        risks = contrarian.get("key_risks", []) or report_data.get(
            "key_risk_factors", []
        )
        if risks:
            for risk in risks:
                st.markdown(f"- ⚠️ {risk}")

        st.markdown("### Evidence")
        for ev in contrarian.get("evidence", []):
            severity = ev.get("severity", "Low").lower()
            st.markdown(
                f'<div class="evidence-item severity-{severity}">'
                f"<strong>[{ev.get('severity', '')}]</strong> "
                f"{ev.get('category', '')}: {ev.get('description', '')}"
                f"<br><em>Source: {ev.get('source', 'N/A')}</em>"
                f"</div>",
                unsafe_allow_html=True,
            )

        if raw.get("contrarian"):
            with st.expander("🔍 Raw Agent Output"):
                st.markdown(raw["contrarian"])

    # ── Technicals tab ─────────────────────────────────────────
    with tab_technicals:
        st.markdown("### Technical Summary")
        tech = report_data.get("technical", {})
        if tech and tech.get("current_price"):
            col1, col2, col3 = st.columns(3)
            col1.metric("Price", f"${tech.get('current_price', 0):.2f}")
            col2.metric("RSI (14)", f"{tech.get('rsi_14', 0):.1f}")
            col3.metric("MACD", f"{tech.get('macd_value', 0):.4f}")

            col4, col5, col6 = st.columns(3)
            col4.metric("MA 50", f"${tech.get('ma_50', 0):.2f}")
            col5.metric(
                "MA 200",
                f"${tech.get('ma_200', 0):.2f}" if tech.get("ma_200") else "N/A",
            )
            col6.metric("MA Crossover", tech.get("ma_crossover", "N/A"))

            col7, col8, col9 = st.columns(3)
            col7.metric("Volume Ratio", f"{tech.get('volume_ratio', 0):.2f}x")
            col8.metric("Insider Buys", tech.get("insider_buys_90d", 0))
            col9.metric("Insider Sells", tech.get("insider_sells_90d", 0))

            st.markdown(
                f"**Overall Technical Bias:** {tech.get('overall_technical_bias', 'N/A')}"
            )
        else:
            st.info("Technical metrics not available. See raw output below.")

        if raw.get("technicals"):
            with st.expander("🔍 Raw Agent Output"):
                st.markdown(raw["technicals"])

    # ── Evidence tab ───────────────────────────────────────────
    with tab_evidence:
        st.markdown("### Full Evidence Ranking")
        contrarian = report_data.get("contrarian", {})
        evidence_list = contrarian.get("evidence", [])

        if evidence_list:
            strength = contrarian.get("evidence_strength_score", 0)
            if strength:
                st.metric("Evidence Strength Score", f"{strength}/100")

            for i, ev in enumerate(evidence_list, 1):
                with st.expander(
                    f"#{i} [{ev.get('severity', '')}] {ev.get('category', '')}"
                ):
                    st.markdown(ev.get("description", ""))
                    st.caption(f"Source: {ev.get('source', 'N/A')}")
        else:
            st.info("No structured evidence parsed. See raw output below.")

        if raw.get("contrarian"):
            with st.expander("🔍 Raw Agent Output"):
                st.markdown(raw["contrarian"])

    # ── Verdict tab ────────────────────────────────────────────
    with tab_verdict:
        st.markdown("### Final Verdict")

        score = report_data.get("divergence_score", 0)
        label = report_data.get("divergence_label", "N/A")

        col1, col2 = st.columns(2)

        with col1:
            st.plotly_chart(
                create_divergence_gauge(score),
                use_container_width=True,
            )

        with col2:
            breakdown = report_data.get("score_breakdown", {})
            if breakdown:
                st.plotly_chart(
                    create_score_breakdown_radar(breakdown),
                    use_container_width=True,
                )
            else:
                st.info("Score breakdown not available.")

        # Display breakdown text if available
        breakdown_text = report_data.get("score_breakdown_text", "")
        if breakdown_text:
            st.markdown("### Score Breakdown")
            st.markdown(breakdown_text)

        # Score card
        if score <= 20:
            css_class = "score-green"
        elif score <= 40:
            css_class = "score-yellow"
        elif score <= 60:
            css_class = "score-orange"
        elif score <= 80:
            css_class = "score-red"
        else:
            css_class = "score-darkred"

        st.markdown(
            f'<div class="score-card {css_class}">'
            f'<div class="score-number">{score}</div>'
            f'<div class="score-label">{label}</div>'
            f"</div>",
            unsafe_allow_html=True,
        )

        st.markdown("### Verdict")
        st.markdown(report_data.get("verdict", "No verdict available."))

        st.markdown(
            f"**Confidence Level:** {report_data.get('confidence_level', 'N/A')}"
        )

        st.markdown("### Key Risk Factors")
        for risk in report_data.get("key_risk_factors", []):
            st.markdown(f"- {risk}")

        if raw.get("final"):
            with st.expander("🔍 Raw Agent Output"):
                st.markdown(raw["final"])

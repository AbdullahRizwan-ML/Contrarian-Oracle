"""The Contrarian Oracle — Streamlit Entry Point."""

import re

import streamlit as st
from loguru import logger

from ui.styles import MAIN_CSS
from ui.sidebar import render_sidebar
from ui.agent_stream import render_agent_progress
from ui.report_view import render_report
from src.crew.oracle_crew import OracleCrew
from src.config.settings import settings

# Page configuration
st.set_page_config(
    page_title="The Contrarian Oracle",
    page_icon="🔮",
    layout="wide",
)

# Inject custom CSS
st.markdown(MAIN_CSS, unsafe_allow_html=True)

# Header
st.markdown(
    '<h1 class="main-header">🔮 The Contrarian Oracle</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="sub-header">'
    "An Autonomous Multi-Agent OSINT System for Financial Narrative Deconstruction"
    "</p>",
    unsafe_allow_html=True,
)

# Sidebar
sidebar_values = render_sidebar()


# ---------------------------------------------------------------------------
# Output parsing helpers
# ---------------------------------------------------------------------------

def _pf(text: str, pattern: str, default: float = 0.0) -> float:
    """Parse a float from text using a regex with one capture group."""
    m = re.search(pattern, text, re.IGNORECASE)
    if m:
        try:
            return float(m.group(1).replace(",", ""))
        except (ValueError, IndexError):
            pass
    return default


def _parse_score(text: str, default: int = 0) -> int:
    """Parse divergence score - ultra-strict to avoid grabbing breakdown numbers."""
    # Use negative lookahead to avoid matching "1" in "1. Technical Divergence"
    m = re.search(r"(?:Divergence Score)[\s\*:]*(\d{1,3})(?!\s*/)", text, re.IGNORECASE)
    if m:
        try:
            return int(m.group(1))
        except (ValueError, IndexError):
            pass
    return default


def _score_to_label(score: int) -> str:
    if score <= 20:
        return "Low Risk"
    if score <= 40:
        return "Moderate Risk"
    if score <= 60:
        return "Elevated Risk"
    if score <= 80:
        return "High Risk"
    return "Extreme Risk"


def parse_crew_output(result, ticker: str) -> dict:
    """Parse CrewOutput into a structured report_data dict."""

    # Collect raw text for each of the 4 tasks
    raw_tasks = ["", "", "", ""]
    if hasattr(result, "tasks_output") and result.tasks_output:
        for i, t in enumerate(result.tasks_output):
            if i < 4:
                raw_tasks[i] = str(t.raw) if hasattr(t, "raw") else str(t)

    tech_text, sent_text, cont_text, final_text = raw_tasks
    if not final_text:
        final_text = str(result)

    # ── Technicals ──────────────────────────────────────────────
    # Try parsing from tech_text, but fallback to final_text if it's mirrored there
    tech_source = tech_text + "\n" + final_text
    
    technical = {}
    if tech_source:
        technical = {
            "current_price": _pf(tech_source, r"(?:Current\s*)?Price[:\s]*\$?([\d,.]+)"),
            "rsi_14": _pf(tech_source, r"RSI.*?[:\s]+([\d.]+)"),
            "macd_value": _pf(tech_source, r"MACD(?:[\sA-Za-z]*)?[:\s]+([-\d.]+)"),
            "ma_50": _pf(tech_source, r"MA\s?50[:\s]*\$?([\d,.]+)"),
            "ma_200": _pf(tech_source, r"MA\s?200[:\s]*\$?([\d,.]+)") or None,
            "ma_crossover": "",
            "volume_ratio": _pf(tech_source, r"Volume Ratio[:\s]*([\d.]+)"),
            "insider_buys_90d": int(_pf(tech_source, r"Insider Buys.*?[:\s]+(\d+)")),
            "insider_sells_90d": int(_pf(tech_source, r"Insider Sells.*?[:\s]+(\d+)")),
            "overall_technical_bias": "",
        }
        m = re.search(r"MA Crossover[:\s]*(.+?)(?:\n|$)", tech_source, re.I)
        if m:
            technical["ma_crossover"] = m.group(1).strip()
        m = re.search(r"Overall Technical Bias[:\s]*(.+?)(?:\n|$)", tech_source, re.I)
        if m:
            technical["overall_technical_bias"] = m.group(1).strip()

    # ── Sentiment ───────────────────────────────────────────────
    sent_source = sent_text + "\n" + final_text
    narrative = {}
    if sent_source:
        narrative = {
            "overall_sentiment_score": _pf(
                sent_source, r"(?:Overall )?Sentiment Score[:\s]*([-+]?[\d.]+)"
            ),
            "sentiment_uniformity": _pf(
                sent_source, r"(?:Sentiment )?Uniformity.*?[:\s]*([\d.]+)"
            ),
            "num_bullish": int(_pf(sent_source, r"Bullish[:\s]*(\d+)")),
            "num_bearish": int(_pf(sent_source, r"Bearish[:\s]*(\d+)")),
            "num_neutral": int(_pf(sent_source, r"Neutral[:\s]*(\d+)")),
            "narrative_confidence": "Medium",
            "headlines": [],
        }

    # ── Contrarian ──────────────────────────────────────────────
    cont_source = cont_text + "\n" + final_text
    contrarian: dict = {}
    if cont_source:
        evidence = []
        for cat, desc, sev, src in re.findall(
            r"Category[:\s]*(.*?),\s*Description[:\s]*(.*?),\s*"
            r"Severity[\s\w]*[:\s]*(Low|Medium|High|Critical),\s*"
            r"Source[:\s]*(.*?)(?:\n|$)",
            cont_source,
            re.I,
        ):
            evidence.append(
                {
                    "category": cat.strip(),
                    "description": desc.strip(),
                    "severity": sev.strip(),
                    "source": src.strip(),
                }
            )

        # Better extraction for Evidence items if the above fails
        if not evidence:
            ev_section = re.search(r"### Evidence[\s\r\n]+(.*?)(?=###|\Z)", cont_source, re.DOTALL | re.I)
            if ev_section:
                for line in ev_section.group(1).splitlines():
                    line = line.strip()
                    if line and re.match(r"^(?:-|\*|\d+\.)", line):
                        # Clean up bullet
                        clean_line = re.sub(r"^(?:-|\*|\d+\.)\s*", "", line)
                        evidence.append({
                            "category": "Finding",
                            "description": clean_line,
                            "severity": "Medium",
                            "source": "AI Synthesis"
                        })

        cn_m = re.search(
            r"Contrarian Narrative[:\s]*(.*?)(?:\n\n|\nEvidence|\nTop|\Z)",
            cont_source,
            re.I | re.DOTALL,
        )
        strength = int(_pf(cont_source, r"Evidence Strength Score[:\s]*(\d+)"))

        cont_risks: list[str] = []
        cr_m = re.search(
            r"(?:Top.*)?Key Risks?[:\s]*\n((?:\s*\d+\..+\n?)+)", cont_source, re.I
        )
        if cr_m:
            cont_risks = [
                r.strip()
                for r in re.findall(r"\d+\.\s+(.+?)(?:\n|$)", cr_m.group(1))
            ]

        contrarian = {
            "contrarian_narrative": cn_m.group(1).strip() if cn_m else "",
            "evidence_strength_score": strength,
            "evidence": evidence,
            "key_risks": cont_risks,
        }

    # ── Final report ────────────────────────────────────────────
    score = _parse_score(final_text)

    lbl_m = re.search(r"Score Label[\*:\s]*([\w\s]+?)(?:\*|\n|\r)", final_text, re.I)
    label = lbl_m.group(1).strip() if lbl_m else _score_to_label(score)

    breakdown: dict = {}
    breakdown_text = ""
    
    # Extract breakdown section for display
    bd_section = re.search(
        r"### Score Breakdown[\s\r\n]+(.*?)(?=### Bull|### Bear|\Z)",
        final_text,
        re.DOTALL | re.I,
    )
    if bd_section:
        breakdown_text = bd_section.group(1).strip()
    
    # Parse individual scores - handle multiple formats
    for comp, key in [
        ("Technical Divergence", "technical_divergence"),
        ("Sentiment Uniformity", "sentiment_uniformity"),
        ("Insider Activity", "insider_activity"),
        ("Fundamental Risk", "fundamental_risk"),
        ("Macro Headwinds", "macro_headwinds"),
    ]:
        # Try percentage format first: "19.25% Technical Divergence"
        m = re.search(
            rf"([\d.]+)%\s+{re.escape(comp)}",
            final_text,
            re.I,
        )
        if m:
            breakdown[key] = round(float(m.group(1)))
        else:
            # Try fraction format: "Technical Divergence: X" or "X/Y"
            m = re.search(
                rf"(?:\*|\d+\.)?\s*\*?\*?{re.escape(comp)}\*?\*?[\s:]*(\d+)(?:/(\d+))?",
                final_text,
                re.I,
            )
            if m:
                score_val = int(m.group(1))
                max_score = int(m.group(2)) if m.group(2) else 100
                if max_score > 0:
                    breakdown[key] = round(score_val / max_score * 100)

    bull_m = re.search(
        r"### Bull Case[\s\r\n]+(.*?)(?=### Bear|### Key|\Z)",
        final_text,
        re.DOTALL | re.I,
    )
    bull_case = bull_m.group(1).strip() if bull_m else ""

    bear_m = re.search(
        r"### Bear Case[\s\r\n]+(.*?)(?=### Key|### Verdict|\Z)",
        final_text,
        re.DOTALL | re.I,
    )
    bear_case = bear_m.group(1).strip() if bear_m else ""

    risks_m = re.search(
        r"### Key Risk Factors[\s\r\n]+(.*?)(?=### Technical|### Evidence|### Verdict|\Z)",
        final_text,
        re.DOTALL | re.I,
    )
    final_risks: list[str] = []
    if risks_m:
        final_risks = [
            r.strip()
            for r in re.findall(r"(?:-|\*|\d+\.)\s+(.+?)(?:\n|$)", risks_m.group(1))
        ]

    verdict_m = re.search(
        r"### Verdict[\s\r\n]+(.*?)(?=###|\Z)",
        final_text,
        re.DOTALL | re.I,
    )
    verdict = verdict_m.group(1).strip() if verdict_m else ""

    conf_m = re.search(r"Confidence Level[\*:\s]*(\d+)%?", final_text)
    confidence = f"{conf_m.group(1)}%" if conf_m else "N/A"

    return {
        "ticker": ticker,
        "divergence_score": score,
        "divergence_label": label,
        "score_breakdown": breakdown,
        "score_breakdown_text": breakdown_text,
        "bull_case_summary": bull_case,
        "bear_case_summary": bear_case or contrarian.get("contrarian_narrative", ""),
        "key_risk_factors": final_risks or contrarian.get("key_risks", []),
        "verdict": verdict or final_text,
        "confidence_level": confidence,
        "technical": technical,
        "narrative": narrative,
        "contrarian": contrarian,
        "raw_outputs": {
            "technicals": tech_text,
            "sentiment": sent_text,
            "contrarian": cont_text,
            "final": final_text,
        },
    }


# ---------------------------------------------------------------------------
# Main content
# ---------------------------------------------------------------------------

if sidebar_values["run_clicked"]:
    ticker = sidebar_values["ticker"]

    if not ticker:
        st.error("Please enter a valid stock ticker.")
    else:
        col_left, col_right = st.columns([2, 1])

        with col_left:
            st.markdown(f"### Analyzing **{ticker}**...")

            agent_names = [
                "🔍 Agent 1: Trend Scraper (Market Data)",
                "📰 Agent 2: Sentiment Synthesizer (Narratives)",
                "🎯 Agent 3: Contrarian Skeptic (Red Team)",
                "⚖️ Agent 4: Final Arbitrator (Verdict)",
            ]

            for name in agent_names:
                render_agent_progress(name, "running", ["Initializing..."])

        with col_right:
            st.markdown("### Divergence Score")
            score_placeholder = st.empty()
            score_placeholder.markdown(
                '<div class="score-card score-green">'
                '<div class="score-number">—</div>'
                '<div class="score-label">Calculating...</div>'
                "</div>",
                unsafe_allow_html=True,
            )

        # Run the crew
        with st.spinner(f"🔮 Oracle is analyzing {ticker}... This may take 2-5 minutes."):
            try:
                crew = OracleCrew(ticker, settings.groq_model)
                crew_result = crew.run()

                # Parse structured data from crew output
                report_data = parse_crew_output(crew_result, ticker)

                # Update the score card
                score = report_data["divergence_score"]
                label = report_data["divergence_label"]

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

                score_placeholder.markdown(
                    f'<div class="score-card {css_class}">'
                    f'<div class="score-number">{score}</div>'
                    f'<div class="score-label">{label}</div>'
                    "</div>",
                    unsafe_allow_html=True,
                )

                st.success(f"✅ Analysis complete for {ticker}!")
                st.markdown("---")
                st.markdown("## 📋 Full Analysis Report")

                render_report(report_data)

            except Exception as e:
                logger.error(f"Error running analysis: {e}")
                st.error(f"Error during analysis: {str(e)}")
                st.info(
                    "Make sure your API keys are configured in the .env file "
                    "and the selected LLM provider is available."
                )

else:
    # Landing state - Premium Dashboard
    st.markdown("---")
    
    # Key Metrics Preview - Larger custom cards
    st.markdown(
        """
        <style>
        .metric-card-large {
            background: linear-gradient(135deg, #1e1e2e, #2d2d3f);
            border-radius: 1rem;
            padding: 1.5rem;
            border: 2px solid #374151;
            text-align: center;
            height: 140px;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        }
        .metric-card-large .metric-value {
            font-size: 2.5rem;
            font-weight: 800;
            color: #06b6d4;
            margin-top: 1rem;
        }
        .metric-card-large .metric-label {
            font-size: 1rem;
            color: #9ca3af;
            font-weight: 600;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    metric_cols = st.columns(4)
    with metric_cols[0]:
        st.markdown(
            """
            <div class="metric-card-large">
                <div class="metric-label">🤖 AI Agents</div>
                <div class="metric-value">4</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with metric_cols[1]:
        st.markdown(
            """
            <div class="metric-card-large">
                <div class="metric-label">📊 Data Sources</div>
                <div class="metric-value">6+</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with metric_cols[2]:
        st.markdown(
            """
            <div class="metric-card-large">
                <div class="metric-label">🎯 Scoring Factors</div>
                <div class="metric-value">5</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with metric_cols[3]:
        st.markdown(
            """
            <div class="metric-card-large">
                <div class="metric-label">⚡ Inference</div>
                <div class="metric-value" style="font-size: 1.5rem;">Groq LPU</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    st.markdown("---")
    
    # Architecture Section
    st.markdown(
        "<h3>⚙️ System Architecture</h3>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "Four specialized AI agents work **sequentially** to audit mainstream financial narratives "
        "against quantitative data and hidden risks."
    )
    
    agent_cols = st.columns(4)
    
    with agent_cols[0]:
        with st.container(border=True, height=240):
            st.markdown("<h4 style='color: #06b6d4;'>🔍 Agent 1</h4>", unsafe_allow_html=True)
            st.markdown("**Trend Scraper**")
            st.caption(
                "Fetches live price data, RSI, MACD, moving averages, "
                "volume analysis, and insider transactions from multiple sources."
            )
    
    with agent_cols[1]:
        with st.container(border=True, height=240):
            st.markdown("<h4 style='color: #06b6d4;'>📰 Agent 2</h4>", unsafe_allow_html=True)
            st.markdown("**Sentiment Synthesizer**")
            st.caption(
                "Scans 48 hours of financial news, classifies sentiment, "
                "and identifies the mainstream consensus narrative."
            )
    
    with agent_cols[2]:
        with st.container(border=True, height=240):
            st.markdown("<h4 style='color: #06b6d4;'>🎯 Agent 3</h4>", unsafe_allow_html=True)
            st.markdown("**Contrarian Skeptic**")
            st.caption(
                "Red-teams the bull case. Finds insider selling, SEC red flags, "
                "hidden transcript risks, and technical divergences."
            )
    
    with agent_cols[3]:
        with st.container(border=True, height=240):
            st.markdown("<h4 style='color: #06b6d4;'>⚖️ Agent 4</h4>", unsafe_allow_html=True)
            st.markdown("**Final Arbitrator**")
            st.caption(
                "Synthesizes all evidence using a weighted scoring model. "
                "Produces a Divergence Score (0-100) with full verdict."
            )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Feature Highlights
    st.markdown(
        "<h3>✨ Key Features</h3>",
        unsafe_allow_html=True,
    )
    feature_cols = st.columns(3)
    
    with feature_cols[0]:
        st.markdown("🧠 **Vector RAG Analysis**")
        st.caption("ChromaDB-powered semantic search through earnings call transcripts")
    
    with feature_cols[1]:
        st.markdown("📈 **Real-Time Market Data**")
        st.caption("Live technical indicators, volume patterns, and insider activity")
    
    with feature_cols[2]:
        st.markdown("🔒 **SEC Filing Scanner**")
        st.caption("Automated analysis of 10-K, 10-Q, and 8-K regulatory filings")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Call to Action
    st.info(
        "👈 **Ready?** Enter a stock ticker in the sidebar and click "
        "'🚀 Run Contrarian Analysis' to begin.",
        icon="🚀",
    )
    
    # Sample Tickers
    st.markdown("**💡 Popular Tickers:** `NVDA` • `TSLA` • `AAPL` • `MSFT` • `META` • `AMZN`")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tech Stack Footer
    st.markdown(
        "<h5>🛠️ Technology Stack</h5>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "`CrewAI Multi-Agent` • `Meta Llama-3.3-70B` • `Groq LPU Inference` • "
        "`ChromaDB Vector Store` • `Streamlit UI` • `Python 3.11`"
    )

# Footer disclaimer
st.markdown("---")
st.caption(
    "⚠️ **Disclaimer:** The Contrarian Oracle is not financial advice. "
    "It is an educational tool for exploring information asymmetries in "
    "financial markets. Always do your own research."
)

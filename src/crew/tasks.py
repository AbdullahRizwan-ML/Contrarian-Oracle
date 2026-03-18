from __future__ import annotations

from crewai import Task

from src.agents.trend_scraper import create_trend_scraper
from src.agents.sentiment_synthesizer import create_sentiment_synthesizer
from src.agents.contrarian_skeptic import create_contrarian_skeptic
from src.agents.final_arbitrator import create_final_arbitrator
from src.config.settings import settings


def create_tasks(ticker: str, llm_model_name: str) -> dict:
    """Create all 4 agents and their tasks for a given ticker."""
    # Use 8B for data collection (fast, efficient)
    # Use 70B for final formatting (better template adherence)
    fast_model = settings.groq_model  # 8B for Agents 1, 2, 3
    smart_model = settings.groq_model_smart  # 70B for Agent 4 only

    # Create agents with appropriate models
    trend_scraper = create_trend_scraper(fast_model)
    sentiment_synth = create_sentiment_synthesizer(fast_model)
    contrarian_skeptic = create_contrarian_skeptic(fast_model)
    arbitrator = create_final_arbitrator(smart_model)  # 70B for formatting

    # Task 1: Technical analysis
    task_technicals = Task(
        description=(
            f"Collect comprehensive market data for {ticker}. "
            f"CRITICAL: Use ONLY the 'stock_data_fetcher' tool - this is your only available tool. "
            f"DO NOT attempt to call 'technical_calculator' or any other tools. "
            f"The 'stock_data_fetcher' tool returns ALL metrics you need in ONE call. "
            f"Call it once with ticker='{ticker}' and report the results. "
            f"If any data is missing from the tool output, report 'N/A' - do not call additional tools. "
            f"Report only facts — never opinions."
        ),
        expected_output=(
            "A detailed technical report containing: current price, "
            "52-week high/low, market cap, sector, PE ratios, MA50, MA200, "
            "MA crossover status, RSI value and signal, MACD value/signal/crossover, "
            "volume metrics, support/resistance, insider buys/sells, "
            "and overall technical bias."
        ),
        agent=trend_scraper,
    )

    # Task 2: Sentiment analysis
    task_sentiment = Task(
        description=(
            f"Search for the latest financial news about {ticker}. "
            f"CRITICAL: Use ONLY the 'financial_news_search' tool - this is your only available tool. "
            f"DO NOT attempt to call 'brave_search', 'google_search', or any other search tools. "
            f"Call the 'financial_news_search' tool with a query about {ticker}. "
            f"Classify each headline as Bullish, Bearish, or Neutral. "
            f"Calculate an overall sentiment score (-1.0 to +1.0). "
            f"Measure sentiment uniformity (how much headlines agree). "
            f"Identify the 'Mainstream Consensus' narrative in 2-3 sentences."
        ),
        expected_output=(
            "A narrative analysis with: headline-by-headline breakdown, "
            "overall sentiment score, sentiment uniformity metric, "
            "mainstream narrative summary, and headline counts per category."
        ),
        agent=sentiment_synth,
    )

    # Task 3: Contrarian analysis
    task_contrarian = Task(
        description=(
            f"DESTROY the bull case for {ticker}. Your job is to find every "
            f"piece of evidence that CONTRADICTS the mainstream narrative. "
            f"Search for: insider selling patterns, technical divergences, "
            f"risks buried in earnings transcripts, competitive threats, "
            f"regulatory risks, and macro headwinds. "
            f"Check SEC filings for red flags. Query earnings transcripts "
            f"for hidden risks. Rate the severity of each piece of evidence "
            f"(Low, Medium, High, Critical). "
            f"If the bull case is genuinely strong, admit it. "
            f"Be concise. Return only the highest-quality, most severe risks. Do not ramble. "
            f"You MUST use the earnings_transcript_search tool to find hidden risks. "
            f"Explicitly quote the transcript in your evidence."
        ),
        expected_output=(
            "A ranked list of contrarian evidence, each with category, "
            "description, severity rating, and source. Include a 2-3 sentence "
            "contrarian narrative (bear case), an evidence strength score (0-100), "
            "and top 3-5 key risks. "
            "You MUST format EACH piece of evidence EXACTLY like this:\n"
            "Category: [Insert Category]\n"
            "Description: [Insert Description]\n"
            "Severity Rating: [Low/Medium/High/Critical]\n"
            "Source: [Insert Source]"
        ),
        agent=contrarian_skeptic,
        context=[task_technicals, task_sentiment],
    )

    # Task 4: Final arbitration
    task_arbitration = Task(
        description=(
            f"Synthesize the bull case and bear case for {ticker}. "
            f"Calculate a Divergence Score (0-100) using this weighted formula: "
            f"25% Technical Divergence + 20% Sentiment Uniformity + "
            f"25% Insider Activity + 15% Fundamental Risk + 15% Macro Headwinds. "
            f"Weigh the QUALITY of evidence, not just quantity. "
            f"A single critical insider-selling pattern can outweigh ten bullish headlines. "
            f"CRITICAL: You MUST use the EXACT output format specified below. "
            f"Copy the section headers EXACTLY with ### prefixes. "
            f"Do not add extra commentary outside the template."
        ),
        expected_output=(
            "CRITICAL: Follow this EXACT format. Do not add extra text before or between sections:\n\n"
            "DIVERGENCE SCORE: <number 0-100>\n"
            "SCORE LABEL: <label>\n\n"
            "### Score Breakdown\n"
            "<percentage>% Technical Divergence\n"
            "<percentage>% Sentiment Uniformity\n"
            "<percentage>% Insider Activity\n"
            "<percentage>% Fundamental Risk\n"
            "<percentage>% Macro Headwinds\n\n"
            "### Bull Case\n"
            "<2-3 sentences summarizing the bullish case>\n\n"
            "### Bear Case\n"
            "<2-3 sentences summarizing the bearish case from Agent 3>\n\n"
            "### Key Risk Factors\n"
            "- <risk 1>\n"
            "- <risk 2>\n"
            "- <risk 3>\n\n"
            "### Technical Summary\n"
            "Current Price: $<price>\n"
            "RSI: <value>\n"
            "MACD: <value>\n"
            "MA 50: $<value>\n"
            "MA 200: $<value>\n"
            "MA Crossover: <status>\n"
            "Overall Technical Bias: <bias>\n\n"
            "### Evidence\n"
            "Category: <category>\n"
            "Description: <description>\n"
            "Severity Rating: <Low/Medium/High/Critical>\n"
            "Source: <source>\n\n"
            "### Verdict\n"
            "<Final verdict paragraph>\n\n"
            "Confidence Level: <percentage>%"
        ),
        agent=arbitrator,
        context=[task_technicals, task_sentiment, task_contrarian],
    )

    return {
        "agents": [trend_scraper, sentiment_synth, contrarian_skeptic, arbitrator],
        "tasks": [task_technicals, task_sentiment, task_contrarian, task_arbitration],
    }

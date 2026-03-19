"""
Backtest Script for The Contrarian Oracle

Runs the OracleCrew on historical dates, records Divergence Scores,
and compares them against actual forward returns to measure predictive power.
"""

import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Tuple

import pandas as pd
import yfinance as yf
from loguru import logger

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.crew.oracle_crew import OracleCrew
from src.config.settings import settings


# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

TICKERS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'META', 'JPM', 'JNJ', 'V']
LOOKBACK_DAYS = 90  # Analyze stocks from 90 days ago


# ─────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def get_target_date() -> str:
    """Calculate the target date (90 days ago) in YYYY-MM-DD format."""
    target = datetime.now() - timedelta(days=LOOKBACK_DAYS)
    return target.strftime("%Y-%m-%d")


def get_close_price(ticker: str, target_date: str, window_days: int = 5) -> Optional[float]:
    """Fetch closing price for a ticker on or near a target date.

    Args:
        ticker: Stock ticker symbol
        target_date: Date in YYYY-MM-DD format
        window_days: Number of days to search forward for valid trading day

    Returns:
        Closing price, or None if not found
    """
    try:
        stock = yf.Ticker(ticker)

        # Parse target date
        target_dt = datetime.strptime(target_date, "%Y-%m-%d")

        # Fetch data from target_date to a few days after (handles weekends/holidays)
        start_date = target_date
        end_date = (target_dt + timedelta(days=window_days)).strftime("%Y-%m-%d")

        hist = stock.history(start=start_date, end=end_date)

        if hist.empty:
            logger.warning(f"No price data found for {ticker} on {target_date}")
            return None

        # Return the first available closing price
        return float(hist['Close'].iloc[0])

    except Exception as e:
        logger.error(f"Error fetching price for {ticker} on {target_date}: {e}")
        return None


def parse_divergence_score(result_text: str) -> Optional[int]:
    """Parse the Divergence Score from crew output using exact regex from app.py.

    Args:
        result_text: Raw crew output text

    Returns:
        Divergence score (0-100), or None if parsing fails
    """
    # Use exact regex from app.py line 59 - ultra-strict to avoid grabbing breakdown numbers
    score_match = re.search(
        r"(?:DIVERGENCE SCORE)[\s\*:]*(\d{1,3})(?!\s*/)",
        result_text,
        re.IGNORECASE
    )

    if score_match:
        try:
            score = int(score_match.group(1))
            if 0 <= score <= 100:
                return score
            else:
                logger.warning(f"Parsed score {score} out of valid range [0, 100]")
                return None
        except (ValueError, IndexError) as e:
            logger.error(f"Error parsing score: {e}")
            return None

    logger.warning("Could not parse Divergence Score from crew output")
    return None


# ─────────────────────────────────────────────────────────────────────────────
# MAIN BACKTEST EXECUTION
# ─────────────────────────────────────────────────────────────────────────────

def run_backtest() -> pd.DataFrame:
    """Execute backtest across all tickers."""
    target_date = get_target_date()
    today = datetime.now().strftime("%Y-%m-%d")

    print("=" * 80)
    print("🔮 THE CONTRARIAN ORACLE - BACKTESTING SYSTEM")
    print("=" * 80)
    print(f"Target Date (Analysis Date): {target_date} ({LOOKBACK_DAYS} days ago)")
    print(f"Evaluation Date (Today): {today}")
    print(f"Tickers: {', '.join(TICKERS)}")
    print(f"Total Tickers: {len(TICKERS)}")
    print("=" * 80)
    print()

    results = []

    for idx, ticker in enumerate(TICKERS, 1):
        print(f"\n{'─' * 80}")
        print(f"[{idx}/{len(TICKERS)}] Analyzing {ticker} as of {target_date}...")
        print(f"{'─' * 80}")

        try:
            # Run OracleCrew with historical target_date
            crew = OracleCrew(
                ticker=ticker,
                llm_model_name=settings.groq_model,
                target_date=target_date
            )
            crew_result = crew.run()

            # Parse Divergence Score from crew output
            result_text = str(crew_result)
            divergence_score = parse_divergence_score(result_text)

            if divergence_score is None:
                logger.warning(f"Failed to parse Divergence Score for {ticker}, skipping...")
                results.append({
                    'Ticker': ticker,
                    'Divergence_Score': None,
                    'Target_Date': target_date,
                    'Target_Price': None,
                    'Current_Price': None,
                    'Actual_Return_Pct': None,
                    'Status': 'PARSE_FAILED'
                })
                continue

            # Get target date price
            target_price = get_close_price(ticker, target_date)
            if target_price is None:
                logger.warning(f"Failed to fetch target price for {ticker}, skipping...")
                results.append({
                    'Ticker': ticker,
                    'Divergence_Score': divergence_score,
                    'Target_Date': target_date,
                    'Target_Price': None,
                    'Current_Price': None,
                    'Actual_Return_Pct': None,
                    'Status': 'PRICE_FETCH_FAILED'
                })
                continue

            # Get current price
            current_price = get_close_price(ticker, today)
            if current_price is None:
                logger.warning(f"Failed to fetch current price for {ticker}, skipping...")
                results.append({
                    'Ticker': ticker,
                    'Divergence_Score': divergence_score,
                    'Target_Date': target_date,
                    'Target_Price': target_price,
                    'Current_Price': None,
                    'Actual_Return_Pct': None,
                    'Status': 'PRICE_FETCH_FAILED'
                })
                continue

            # Calculate forward return
            actual_return_pct = ((current_price - target_price) / target_price) * 100

            print(f"✓ {ticker}: Score={divergence_score}, "
                  f"Price ${target_price:.2f} → ${current_price:.2f}, "
                  f"Return={actual_return_pct:+.2f}%")

            results.append({
                'Ticker': ticker,
                'Divergence_Score': divergence_score,
                'Target_Date': target_date,
                'Target_Price': round(target_price, 2),
                'Current_Price': round(current_price, 2),
                'Actual_Return_Pct': round(actual_return_pct, 2),
                'Status': 'SUCCESS'
            })

        except Exception as e:
            logger.error(f"Error processing {ticker}: {e}")
            results.append({
                'Ticker': ticker,
                'Divergence_Score': None,
                'Target_Date': target_date,
                'Target_Price': None,
                'Current_Price': None,
                'Actual_Return_Pct': None,
                'Status': f'ERROR: {str(e)[:50]}'
            })

    return pd.DataFrame(results)


def analyze_results(df: pd.DataFrame) -> None:
    """Perform statistical analysis and display results."""
    print("\n\n")
    print("=" * 80)
    print("📊 BACKTEST RESULTS")
    print("=" * 80)
    print()

    # Display full results
    print(df.to_string(index=False))
    print()

    # Filter to successful runs only
    df_valid = df[df['Status'] == 'SUCCESS'].copy()

    if len(df_valid) == 0:
        print("❌ No valid results to analyze. All tickers failed.")
        return

    print("=" * 80)
    print("📈 STATISTICAL ANALYSIS")
    print("=" * 80)
    print()
    print(f"Valid Results: {len(df_valid)} / {len(df)}")
    print(f"Success Rate: {len(df_valid) / len(df) * 100:.1f}%")
    print()

    # Summary statistics
    print("Divergence Score Statistics:")
    print(f"  Mean: {df_valid['Divergence_Score'].mean():.2f}")
    print(f"  Median: {df_valid['Divergence_Score'].median():.2f}")
    print(f"  Std Dev: {df_valid['Divergence_Score'].std():.2f}")
    print(f"  Range: [{df_valid['Divergence_Score'].min():.0f}, {df_valid['Divergence_Score'].max():.0f}]")
    print()

    print("Forward Return Statistics:")
    print(f"  Mean: {df_valid['Actual_Return_Pct'].mean():.2f}%")
    print(f"  Median: {df_valid['Actual_Return_Pct'].median():.2f}%")
    print(f"  Std Dev: {df_valid['Actual_Return_Pct'].std():.2f}%")
    print(f"  Range: [{df_valid['Actual_Return_Pct'].min():.2f}%, {df_valid['Actual_Return_Pct'].max():.2f}%]")
    print()

    # Pearson correlation
    if len(df_valid) >= 2:
        correlation = df_valid['Divergence_Score'].corr(df_valid['Actual_Return_Pct'])
        print("=" * 80)
        print("🎯 PEARSON CORRELATION")
        print("=" * 80)
        print(f"Correlation Coefficient: {correlation:.4f}")
        print()

        # Interpretation
        if correlation < -0.5:
            interpretation = "Strong NEGATIVE correlation - High divergence scores predict LOWER returns ✓"
            print(f"Interpretation: {interpretation}")
            print("This validates the Oracle's thesis: divergence indicates risk/overvaluation.")
        elif correlation < -0.3:
            interpretation = "Moderate NEGATIVE correlation - Some predictive signal"
            print(f"Interpretation: {interpretation}")
            print("The Oracle shows promise but may benefit from refinement.")
        elif correlation < -0.1:
            interpretation = "Weak NEGATIVE correlation - Limited predictive power"
            print(f"Interpretation: {interpretation}")
        elif correlation < 0.1:
            interpretation = "No meaningful correlation - System not predictive"
            print(f"Interpretation: {interpretation}")
            print("The Oracle needs significant refinement or reconceptualization.")
        elif correlation < 0.3:
            interpretation = "Weak POSITIVE correlation - Counterintuitive result"
            print(f"Interpretation: {interpretation}")
            print("Surprising: High divergence may indicate opportunity, not risk.")
        elif correlation < 0.5:
            interpretation = "Moderate POSITIVE correlation - High divergence predicts HIGHER returns"
            print(f"Interpretation: {interpretation}")
            print("Counterintuitive: The Oracle may be identifying contrarian opportunities.")
        else:
            interpretation = "Strong POSITIVE correlation - High divergence predicts HIGHER returns"
            print(f"Interpretation: {interpretation}")
            print("The Oracle may be a contrarian opportunity identifier rather than risk detector.")

        print()
    else:
        print("⚠️  Insufficient data for correlation analysis (need at least 2 valid results)")
        print()

    print("=" * 80)


def save_results(df: pd.DataFrame, output_path: str) -> None:
    """Save results to CSV file."""
    df.to_csv(output_path, index=False)
    print(f"💾 Results saved to: {output_path}")
    print("=" * 80)
    print()


# ─────────────────────────────────────────────────────────────────────────────
# MAIN ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

def main():
    """Execute the complete backtest workflow."""
    # Ensure data directory exists
    data_dir = project_root / "data"
    data_dir.mkdir(exist_ok=True)

    # Run backtest
    logger.info("Starting backtest execution...")
    df = run_backtest()

    # Analyze results
    analyze_results(df)

    # Save to CSV
    output_path = data_dir / "backtest_results.csv"
    save_results(df, str(output_path))

    # Final summary
    df_valid = df[df['Status'] == 'SUCCESS']
    if len(df_valid) >= 2:
        correlation = df_valid['Divergence_Score'].corr(df_valid['Actual_Return_Pct'])
        print(f"✅ Backtest complete! Correlation: {correlation:.4f}")
    else:
        print("⚠️  Backtest complete, but insufficient valid results for correlation analysis.")


if __name__ == "__main__":
    main()

# Architecture

## System Overview

The Contrarian Oracle is a multi-agent AI system built with CrewAI that performs adversarial financial analysis.

## Agent Communication Flow

```
Agent 1 (Trend Scraper)
  │ output: Technical analysis text
  ▼
Agent 2 (Sentiment Synth) — runs independently of Agent 1
  │ output: Narrative analysis text
  ▼
Agent 3 (Contrarian Skeptic)
  │ receives: Agent 1 + Agent 2 outputs via `context` parameter
  │ output: Contrarian evidence text
  ▼
Agent 4 (Arbitrator)
  │ receives: Agent 1 + Agent 2 + Agent 3 outputs via `context` parameter
  │ output: Final report with Divergence Score
```

- Tasks 1 and 2 are **independent** (could theoretically run in parallel)
- Task 3 **depends** on tasks 1 and 2
- Task 4 **depends** on tasks 1, 2, and 3
- `process=Process.sequential` in CrewAI ensures they run in order

## Scoring Formula

```
Score = (0.25 × Technical) + (0.20 × Sentiment) + (0.25 × Insider) + (0.15 × Fundamental) + (0.15 × Macro)
```

Each component is scored 0-100, producing a final weighted score.

## Data Flow

1. User enters ticker → Sidebar sends to OracleCrew
2. OracleCrew creates 4 agents with their tools
3. Sequential execution: technicals → sentiment → contrarian → arbitration
4. Results displayed in Streamlit with tabs, charts, and score gauge

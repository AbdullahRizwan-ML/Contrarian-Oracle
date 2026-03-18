"""Custom CSS styles for The Contrarian Oracle Streamlit app."""

MAIN_CSS = """
<style>
    .main-header {
        background: linear-gradient(90deg, #7c3aed, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        padding: 1rem 0 0.25rem 0;
    }

    .sub-header {
        color: #9ca3af;
        font-style: italic;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    .score-card {
        text-align: center;
        padding: 2rem;
        border-radius: 1rem;
        margin: 1rem 0;
    }

    .score-card .score-number {
        font-size: 4rem;
        font-weight: 900;
    }

    .score-card .score-label {
        font-size: 1.2rem;
        margin-top: 0.5rem;
    }

    .score-green {
        background: linear-gradient(135deg, #064e3b, #065f46);
        border: 1px solid #10b981;
    }

    .score-yellow {
        background: linear-gradient(135deg, #78350f, #92400e);
        border: 1px solid #f59e0b;
    }

    .score-orange {
        background: linear-gradient(135deg, #7c2d12, #9a3412);
        border: 1px solid #f97316;
    }

    .score-red {
        background: linear-gradient(135deg, #7f1d1d, #991b1b);
        border: 1px solid #ef4444;
    }

    .score-darkred {
        background: linear-gradient(135deg, #450a0a, #7f1d1d);
        border: 1px solid #dc2626;
    }

    .agent-thought {
        background-color: #1e1e2e;
        border-left: 3px solid #06b6d4;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        font-family: 'JetBrains Mono', 'Fira Code', monospace;
        font-size: 0.85rem;
        border-radius: 0 0.5rem 0.5rem 0;
        color: #e2e8f0;
    }

    .metric-card {
        background: linear-gradient(135deg, #1e1e2e, #2d2d3f);
        border-radius: 0.75rem;
        padding: 1.25rem;
        border: 1px solid #374151;
        margin: 0.5rem 0;
    }

    .metric-card h4 {
        color: #06b6d4;
        margin-bottom: 0.5rem;
    }

    .evidence-item {
        background: #1e1e2e;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #6b7280;
    }

    .evidence-item.severity-low {
        border-left-color: #10b981;
    }

    .evidence-item.severity-medium {
        border-left-color: #f59e0b;
    }

    .evidence-item.severity-high {
        border-left-color: #f97316;
    }

    .evidence-item.severity-critical {
        border-left-color: #ef4444;
    }

    .agent-card {
        background: linear-gradient(135deg, #1e1e2e, #2d2d3f);
        border-radius: 1rem;
        padding: 1.5rem;
        border: 1px solid #374151;
        margin: 0.5rem;
        text-align: center;
    }

    .agent-card h3 {
        color: #7c3aed;
        margin-bottom: 0.5rem;
    }

    .agent-card p {
        color: #9ca3af;
        font-size: 0.9rem;
    }
</style>
"""

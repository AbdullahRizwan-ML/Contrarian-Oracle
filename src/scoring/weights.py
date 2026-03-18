from __future__ import annotations

DEFAULT_WEIGHTS = {
    "technical_divergence": 0.25,
    "sentiment_uniformity": 0.20,
    "insider_activity": 0.25,
    "fundamental_risk": 0.15,
    "macro_headwinds": 0.15,
}

AGGRESSIVE_WEIGHTS = {
    "technical_divergence": 0.30,
    "sentiment_uniformity": 0.15,
    "insider_activity": 0.30,
    "fundamental_risk": 0.10,
    "macro_headwinds": 0.15,
}

CONSERVATIVE_WEIGHTS = {
    "technical_divergence": 0.15,
    "sentiment_uniformity": 0.15,
    "insider_activity": 0.20,
    "fundamental_risk": 0.25,
    "macro_headwinds": 0.25,
}


def get_weights(profile: str = "default") -> dict:
    """Return a weight profile by name."""
    profiles = {
        "default": DEFAULT_WEIGHTS,
        "aggressive": AGGRESSIVE_WEIGHTS,
        "conservative": CONSERVATIVE_WEIGHTS,
    }
    return profiles.get(profile, DEFAULT_WEIGHTS)

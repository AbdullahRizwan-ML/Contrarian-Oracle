from __future__ import annotations

import re
from pathlib import Path

from loguru import logger


def load_text_file(filepath: str) -> str:
    """Load a plain text file and return its contents."""
    try:
        path = Path(filepath)
        text = path.read_text(encoding="utf-8")
        logger.info(f"Loaded text file: {filepath} ({len(text)} chars)")
        return text
    except Exception as e:
        logger.error(f"Error loading file {filepath}: {e}")
        return ""


def load_earnings_transcript(filepath: str) -> dict:
    """Load an earnings call transcript and extract metadata."""
    try:
        text = load_text_file(filepath)
        filename = Path(filepath).stem

        # Attempt to parse metadata from filename (e.g. NVDA_Q3_2024)
        parts = filename.split("_")
        company = parts[0] if len(parts) > 0 else "Unknown"
        quarter = parts[1] if len(parts) > 1 else "Unknown"
        date = parts[2] if len(parts) > 2 else "Unknown"

        return {
            "text": text,
            "date": date,
            "company": company,
            "quarter": quarter,
        }
    except Exception as e:
        logger.error(f"Error loading transcript {filepath}: {e}")
        return {"text": "", "date": "Unknown", "company": "Unknown", "quarter": "Unknown"}


def clean_text(text: str) -> str:
    """Remove extra whitespace and special characters from text."""
    # Remove multiple spaces
    text = re.sub(r"\s+", " ", text)
    # Remove non-printable characters
    text = re.sub(r"[^\x20-\x7E\n]", "", text)
    return text.strip()


def chunk_documents(
    text: str, chunk_size: int, overlap: int
) -> list[str]:
    """Split text into overlapping word-based chunks."""
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start = end - overlap

    return chunks

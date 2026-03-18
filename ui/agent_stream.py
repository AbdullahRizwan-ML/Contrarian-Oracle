from __future__ import annotations

import streamlit as st


def render_agent_progress(
    agent_name: str, status: str, thoughts: list[str]
) -> None:
    """Render real-time agent thought display using st.status."""
    is_complete = status == "complete"

    with st.status(
        f"{'✅' if is_complete else '🔄'} {agent_name}",
        expanded=not is_complete,
        state="complete" if is_complete else "running",
    ):
        for thought in thoughts:
            st.markdown(
                f'<div class="agent-thought">{thought}</div>',
                unsafe_allow_html=True,
            )

        if is_complete:
            st.markdown(f"**{agent_name}** — Analysis complete ✅")
        else:
            st.markdown(f"**{agent_name}** — Working...")

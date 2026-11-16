"""Part 2: ask Claude to explain the stats. Falls back to a simple summary
if there is no API key or the API call fails."""
import os

import anthropic


def fallback_summary(stats: dict, question: str) -> str:
    return (
        f"(Rule-based summary, no AI key set) Total visits: {stats['total_visits']}. "
        f"Top page: {stats['top_page']}. Highest bounce rate: {stats['highest_bounce_page']}. "
        f"Fastest growing: {stats['fastest_growing_page']}."
    )


def ask_ai(stats: dict, question: str) -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")  # read from environment, never hardcode
    if not api_key:
        return fallback_summary(stats, question)

    prompt = (
        "You are a website analytics assistant. Answer ONLY using the data below. "
        "If the data cannot answer the question, say so. Be short and give 2 concrete suggestions.\n\n"
        f"DATA: {stats}\n\nQUESTION: {question}"
    )
    try:
        client = anthropic.Anthropic(api_key=api_key)
        msg = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )
        return msg.content[0].text
    except Exception as e:  # network error, bad key, rate limit...
        return fallback_summary(stats, question) + f" [AI error: {type(e).__name__}]"

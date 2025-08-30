from typing import Literal
Tone = Literal["Neutral", "Suspenseful", "Inspiring"]

EXTRACT_PROMPT = (
    "You are an editor whose job is to extract the essential facts, claims, and "
    "points from the SOURCE text. Return concise bullet points (5-12) that MUST "
    "be preserved by any rewrite.\n\n"
    "<SOURCE>\n{source}\n</SOURCE>\n\n"
    "Return bullets only."
)

REWRITE_PROMPT = (
    "Rewrite the SOURCE text as a polished audiobook narration in a {tone} tone. "
    "Follow these rules:\n"
    "- Preserve the meaning and all facts from the FACTS list.\n"
    "- Maintain technical terms exactly.\n"
    "- Use spoken-friendly pacing, and keep length within +/-10% of original.\n\n"
    "<FACTS>\n{facts}\n</FACTS>\n\n"
    "<SOURCE>\n{source}\n</SOURCE>\n\n"
    "Return only the rewritten narration (no commentary)."
)

VERIFY_PROMPT = (
    "Compare the REWRITE to the FACTS and SOURCE. If the rewrite introduces new claims "
    "or drops any fact, list each problem as a bullet. If it's faithful, reply 'OK'.\n\n"
    "<FACTS>\n{facts}\n</FACTS>\n\n"
    "<SOURCE>\n{source}\n</SOURCE>\n\n"
    "<REWRITE>\n{rewrite}\n</REWRITE>\n"
)

TONE_HINTS = {
    "Neutral": "calm, informative, even pacing",
    "Suspenseful": "measured tension, cinematic pauses, vivid adjectives (but factual)",
    "Inspiring": "uplifting cadence, energetic but clear"
}
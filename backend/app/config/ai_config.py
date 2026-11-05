"""
AI Agent & Model Configuration
"""
from typing import Dict, Any

AI_MODELS = {
    "openai": ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"],
    "gemini": ["gemini-1.5-flash", "gemini-1.5-pro"],
    "mock": ["mailmind-heuristic-agent-v1"]
}

SUPPORTED_TONES = [
    "Professional",
    "Casual",
    "Direct",
    "Empathetic",
    "Formal"
]

DEFAULT_PROMPT_CONFIG: Dict[str, Any] = {
    "max_summary_sentences": 2,
    "max_key_points": 4,
    "max_action_items": 3,
    "confidence_threshold": 0.75,
    "auto_draft_replies": True,
    "sentiment_analysis_enabled": True
}

"""
Simple wrapper for the Ollama chat API.
Uses the llama3 model pulled by the docker‑compose stack.
"""

import os, requests

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")
MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama3")   # change if you prefer mixtral

def run_llm(system_prompt: str, user_input: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_input},
        ],
        "stream": False,
    }

    r = requests.post(f"{OLLAMA_URL}/api/chat", json=payload, timeout=180)
    r.raise_for_status()
    return r.json()["message"]["content"].strip()

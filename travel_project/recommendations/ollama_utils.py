import requests

def call_ollama(prompt: str) -> str:
    url = "http://host.docker.internal:11434/api/generate"
    payload = {
        "model": "gemma3:latest",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload, timeout=1000)
        response.raise_for_status()
        return response.json()["response"]
    except requests.RequestException as e:
        raise Exception(f"Ollama HTTP error: {e}")
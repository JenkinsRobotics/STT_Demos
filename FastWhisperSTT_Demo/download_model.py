import os
import requests
from pathlib import Path

# List of all standard faster-whisper models on Hugging Face
MODELS = {
    "tiny": "Systran/faster-whisper-tiny",
    "tiny.en": "Systran/faster-whisper-tiny.en",
    "base": "Systran/faster-whisper-base",
    "base.en": "Systran/faster-whisper-base.en",
    "small": "Systran/faster-whisper-small",
    "small.en": "Systran/faster-whisper-small.en",
    "medium": "Systran/faster-whisper-medium",
    "medium.en": "Systran/faster-whisper-medium.en",
    "large-v1": "Systran/faster-whisper-large-v1",
    "large-v2": "Systran/faster-whisper-large-v2",
    "large-v3": "Systran/faster-whisper-large-v3",
}

# Required files for each model
FILES = ["config.json", "model.bin", "tokenizer.json", "vocabulary.txt"]

BASE_DIR = Path("models")

def download_file(repo_id, model_dir, file_name):
    url = f"https://huggingface.co/{repo_id}/resolve/main/{file_name}"
    dest = model_dir / file_name
    if dest.exists():
        print(f"  ✔️  {file_name} already exists.")
        return
    print(f"  ⬇️  Downloading {file_name}...")
    response = requests.get(url)
    if response.status_code == 200:
        with open(dest, "wb") as f:
            f.write(response.content)
        print(f"  ✅  Saved: {dest}")
    else:
        print(f"  ❌  Failed to download {file_name} (HTTP {response.status_code})")

def setup_model(model_name, repo_id):
    model_dir = BASE_DIR / model_name
    model_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n📦 Setting up model: {model_name}")
    for file_name in FILES:
        download_file(repo_id, model_dir, file_name)

def main():
    for model_name, repo_id in MODELS.items():
        setup_model(model_name, repo_id)
    print("\n🎉 All models downloaded and ready in the 'models/' directory.")

if __name__ == "__main__":
    main()
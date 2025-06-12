import json
import os

from pathlib import Path

def read_json(path: str, default_response: list | dict = {}) -> dict:
    os.makedirs(str(Path(path).parent), exist_ok=True) 
    try:
        with open(path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        write_json(path, [])
        return default_response

def write_json(path: str, content: dict) -> None:
    print("🔍 DEBUG JSON:", repr(content))
    with open(path, "w") as file:
        json.dump(content, file, ensure_ascii=False)
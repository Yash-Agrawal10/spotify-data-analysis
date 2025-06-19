import json
import os
from dotenv import load_dotenv
from pathlib import Path
from typing import Any, Optional

load_dotenv()
data_path = os.getenv("DATA_PATH")
if not data_path:
    raise RuntimeError("Missing DATA_PATH env var")
data_dir = Path(data_path)

class DataStore:

    def __init__(self, username: str):
        self.directory = data_dir / username
        self.directory.mkdir(exist_ok=True)

    def load(self, key:str) -> Optional[Any]:
        path = (self.directory / key).with_suffix(".json")
        if not path.exists():
            return None
        with open(path, 'r') as file:
            return json.load(file)
        
    def save(self, key: str, obj: Any) -> None:
        path = (self.directory / key).with_suffix(".json")
        tmp = path.with_suffix(".tmp")
        with tmp.open("w") as f:
            json.dump(obj, f, indent=2)
        tmp.replace(path)
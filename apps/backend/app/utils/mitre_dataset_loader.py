import json
from pathlib import Path


class MitreDatasetLoader:

    def __init__(self):
        self.dataset = Path("data/enterprise-attack.json")

    def load(self):

        with open(self.dataset, "r", encoding="utf-8") as f:
            return json.load(f)

    def attack_patterns(self):

        data = self.load()

        return [
            obj
            for obj in data["objects"]
            if obj.get("type") == "attack-pattern"
        ]
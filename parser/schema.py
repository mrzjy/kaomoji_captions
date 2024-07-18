import json

from pydantic import BaseModel


class Caption(BaseModel):
    kaomoji: str
    caption: str
    meta: dict = {}


def save_samples(samples: list[BaseModel], out_path, mode="w", extension="jsonl"):
    print(f"saving {len(samples)} samples into {out_path}")
    with open(out_path, mode, encoding="utf-8") as f:
        if extension == "jsonl":
            for s in samples:
                print(json.dumps(s.dict(), ensure_ascii=False), file=f)
        else:
            samples = [s.dict() for s in samples]
            json.dump(samples, f, ensure_ascii=False, indent=4)
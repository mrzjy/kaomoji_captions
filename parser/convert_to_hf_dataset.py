from datasets import load_dataset

ds = load_dataset("json", data_files={"train": "../data/kaomoji_captions.jsonl"})
ds.save_to_disk("../kaomoji_captions")
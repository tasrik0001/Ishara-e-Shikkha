import json
import re
import pandas as pd
from pathlib import Path
 
UPLOADS = Path("data")
OUT_DIR = Path("data")
OUT_DIR.mkdir(parents=True, exist_ok=True)
 
 
def split_variants(raw_word: str):
    """'বাবা/আব্বা' -> ['বাবা', 'আব্বা']; plain word -> [word]"""
    parts = [p.strip() for p in re.split(r"[/,]", raw_word) if p.strip()]
    return parts if parts else [raw_word.strip()]
 
 
def load_bdslw102(path):
    df = pd.read_csv(path)
    records = []
    for _, row in df.iterrows():
        variants = split_variants(str(row["word"]))
        records.append({
            "primary": variants[0],
            "variants": variants,
            "source": "BdSLW102",
            "source_id": str(row["id"]),
            "category": None,
            "media": [],
        })
    return records
 
 
def load_bdslw401(path):
    df = pd.read_csv(path)
    records = []
    for _, row in df.iterrows():
        variants = split_variants(str(row["Word in Bangla"]))
        records.append({
            "primary": variants[0],
            "variants": variants,
            "source": "BdSLW401",
            "source_id": str(row["Word Number"]),
            "category": None,
            "media": [],
        })
    return records
 
 
def load_ishaara(path):
    """Handles the raw_words_ishaara_ai.json structure shown in the prompt."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    records = []
    for entry in data:
        variants = split_variants(entry["banglaWord"])
        media = [
            {
                "actor": a.get("actorName"),
                "actor_prefix": a.get("actorPrefix"),
                "video": a.get("videoFile"),
                "parquet": a.get("parquetFile"),
                "video_exists": a.get("videoExists"),
                "parquet_exists": a.get("parquetExists"),
            }
            for a in entry.get("actors", [])
        ]
        records.append({
            "primary": variants[0],
            "variants": variants,
            "source": "ishaara",
            "source_id": entry.get("wordId"),
            "category": entry.get("category"),
            "media": media,
        })
    return records
 
 
def merge(all_records):
    """Merge records into unified entries, deduping on variant overlap."""
    # index: variant string -> unified entry index
    variant_index = {}
    unified = []
 
    for rec in all_records:
        match_idx = None
        for v in rec["variants"]:
            if v in variant_index:
                match_idx = variant_index[v]
                break
 
        if match_idx is None:
            entry = {
                "unified_id": len(unified) + 1,
                "word": rec["primary"],
                "variants": list(rec["variants"]),
                "category": rec["category"],
                "sources": {
                    rec["source"]: {
                        "source_id": rec["source_id"],
                        **({"category": rec["category"]} if rec["category"] else {}),
                    }
                },
                "media": list(rec["media"]),
            }
            unified.append(entry)
            idx = len(unified) - 1
            for v in rec["variants"]:
                variant_index[v] = idx
        else:
            entry = unified[match_idx]
            # merge variants
            for v in rec["variants"]:
                if v not in entry["variants"]:
                    entry["variants"].append(v)
                variant_index[v] = match_idx
            # merge source info
            entry["sources"][rec["source"]] = {
                "source_id": rec["source_id"],
                **({"category": rec["category"]} if rec["category"] else {}),
            }
            # fill category if this source has one and entry doesn't yet
            if rec["category"] and not entry["category"]:
                entry["category"] = rec["category"]
            # merge media (avoid dupes by video filename)
            existing_videos = {m["video"] for m in entry["media"] if m.get("video")}
            for m in rec["media"]:
                if m.get("video") not in existing_videos:
                    entry["media"].append(m)
 
    return unified
 
 
def main():
    all_records = []
 
    bdslw102_path = UPLOADS / "BdSLW102.csv"
    bdslw401_path = UPLOADS / "BdSLW401.csv"
    ishaara_path = UPLOADS / "raw_words_ishaara_ai.json"
 
    if bdslw102_path.exists():
        all_records += load_bdslw102(bdslw102_path)
        print(f"Loaded {len(load_bdslw102(bdslw102_path))} words from BdSLW102")
 
    if bdslw401_path.exists():
        all_records += load_bdslw401(bdslw401_path)
        print(f"Loaded {len(load_bdslw401(bdslw401_path))} words from BdSLW401")
 
    if ishaara_path.exists():
        ish = load_ishaara(ishaara_path)
        all_records += ish
        print(f"Loaded {len(ish)} words from Ishaara")
    else:
        print("NOTE: raw_words_ishaara_ai.json not found in uploads — skipped. "
              "Upload it and re-run to include it.")
 
    unified = merge(all_records)
 
    # Save JSON
    out_json = OUT_DIR / "unified_vocabulary.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(unified, f, ensure_ascii=False, indent=2)
 
    # Save flat CSV summary (word, variants, sources present, media count)
    flat_rows = []
    for e in unified:
        flat_rows.append({
            "unified_id": e["unified_id"],
            "word": e["word"],
            "variants": " / ".join(e["variants"]),
            "category": e["category"] or "",
            "sources": ", ".join(e["sources"].keys()),
            "media_count": len(e["media"]),
        })
    out_csv = OUT_DIR / "unified_vocabulary.csv"
    pd.DataFrame(flat_rows).to_csv(out_csv, index=False, encoding="utf-8-sig")
 
    print()
    print(f"Total unique words after merge: {len(unified)}")
    print(f"Saved: {out_json}")
    print(f"Saved: {out_csv}")
 
 
if __name__ == "__main__":
    main()
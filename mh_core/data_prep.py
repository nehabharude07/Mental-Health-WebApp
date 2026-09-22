"""
mh_core.data_prep
-----------------
Deepression.csv ko clean karta hai.

Original file me kaafi problems hain:
  * column names me extra spaces ("Number ")
  * target column me tab characters aur stray digits ("\tMild", "2\tNo depression")
  * 273 rows me target bilkul blank hai
  * scale 1-5 honi chahiye par kuch cells me 6 hai
  * 813 rows me sirf 32 unique symptom combinations hain (bhaari duplication)
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Tuple, Dict, Any

import pandas as pd

from .scoring import ITEMS, STATES

TARGET = "Depression State"
FEATURE_COLUMNS = [i.csv_column for i in ITEMS]

_LABEL_PREFIX = re.compile(r"^[\d\s\t\.\-]+")


def _clean_label(value: object) -> str | float:
    if not isinstance(value, str):
        return float("nan")
    text = _LABEL_PREFIX.sub("", value).strip()
    # normalise casing variants like "no depression"
    for state in STATES:
        if text.lower() == state.lower():
            return state
    return float("nan")


def load_clean(csv_path: str | Path) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Returns (clean_dataframe, report_dict).

    clean_dataframe me sirf 14 feature columns + TARGET rehta hai,
    features 1-5 me clipped, aur target 4 valid states me se ek.
    """
    df = pd.read_csv(csv_path)
    report: Dict[str, Any] = {"rows_loaded": int(len(df))}

    # 1. strip whitespace from headers
    df.columns = [str(c).strip() for c in df.columns]

    missing = [c for c in FEATURE_COLUMNS + [TARGET] if c not in df.columns]
    if missing:
        raise KeyError(f"CSV me ye columns nahi mile: {missing}")

    # 2. clean the target
    df[TARGET] = df[TARGET].map(_clean_label)
    report["rows_dropped_bad_target"] = int(df[TARGET].isna().sum())
    df = df.dropna(subset=[TARGET])

    # 3. coerce features to numeric and clip to the documented 1-5 range
    out_of_range = 0
    for col in FEATURE_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        out_of_range += int(((df[col] < 1) | (df[col] > 5)).sum())
        df[col] = df[col].clip(1, 5)
    report["cells_clipped_out_of_range"] = out_of_range

    before = len(df)
    df = df.dropna(subset=FEATURE_COLUMNS)
    report["rows_dropped_missing_features"] = int(before - len(df))

    df = df[FEATURE_COLUMNS + [TARGET]].reset_index(drop=True)
    for col in FEATURE_COLUMNS:
        df[col] = df[col].astype(int)

    report["rows_clean"] = int(len(df))
    report["class_counts"] = {k: int(v) for k, v in df[TARGET].value_counts().items()}
    report["unique_feature_rows"] = int(df[FEATURE_COLUMNS].drop_duplicates().shape[0])

    # 4. label-noise measurement: identical inputs with different labels
    grouped = df.groupby(FEATURE_COLUMNS)[TARGET]
    sizes = grouped.size()
    purity = grouped.agg(lambda s: s.value_counts().iloc[0] / len(s))
    report["contradictory_combinations"] = int((grouped.nunique() > 1).sum())
    report["total_combinations"] = int(len(sizes))
    report["bayes_accuracy_ceiling"] = round(float((purity * sizes).sum() / sizes.sum()), 4)

    return df, report


if __name__ == "__main__":  # pragma: no cover
    import json

    root = Path(__file__).resolve().parent.parent
    frame, rep = load_clean(root / "Deepression.csv")
    frame.to_csv(root / "Deepression_clean.csv", index=False)
    print(json.dumps(rep, indent=2))
    print(f"\nSaved -> Deepression_clean.csv ({len(frame)} rows)")

"""
train_model.py  (UPGRADED)
==========================

Purana version sirf 8 hardcoded rows par train karta tha - isiliye app har naye
input par lagbhag ek hi jawab de raha tha.

Ab yeh script:
  1. Deepression.csv ko properly clean karta hai (mh_core.data_prep)
  2. 4 alag models compare karta hai stratified 5-fold cross-validation se
  3. Best model ko full data par refit kar ke bundle save karta hai
  4. Honest metrics model/metrics.json me likhta hai
  5. Agar dataset itna noisy hai ki model bharosemand nahi, to bundle me
     `reliable: false` flag lagata hai - app tab rule-based engine ko
     primary rakhta hai.

Run:
    python train_model.py
"""

from __future__ import annotations

import json
from pathlib import Path

from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

import joblib

from mh_core.data_prep import load_clean, FEATURE_COLUMNS, TARGET

ROOT = Path(__file__).resolve().parent
MODEL_DIR = ROOT / "model"
MODEL_DIR.mkdir(exist_ok=True)

RANDOM_STATE = 42
# Agar cross-validated accuracy is threshold se neeche hai to model ko
# app ke headline result me use nahi kiya jayega.
RELIABILITY_THRESHOLD = 0.60


def build_candidates() -> dict:
    return {
        "baseline_majority": Pipeline([
            ("clf", DummyClassifier(strategy="most_frequent")),
        ]),
        "logistic_regression": Pipeline([
            ("scale", StandardScaler()),
            ("clf", LogisticRegression(max_iter=2000, C=1.0,
                                       class_weight="balanced",
                                       random_state=RANDOM_STATE)),
        ]),
        "random_forest": Pipeline([
            ("clf", RandomForestClassifier(n_estimators=400, max_depth=8,
                                           min_samples_leaf=4,
                                           class_weight="balanced",
                                           random_state=RANDOM_STATE,
                                           n_jobs=-1)),
        ]),
        "hist_gradient_boosting": Pipeline([
            ("clf", HistGradientBoostingClassifier(max_iter=300,
                                                   learning_rate=0.08,
                                                   max_depth=6,
                                                   random_state=RANDOM_STATE)),
        ]),
    }


def main() -> None:
    print("=" * 66)
    print("  Mental Health Prediction System - Model Training")
    print("=" * 66)

    # ---------------- 1. data -------------------------------------------
    df, report = load_clean(ROOT / "Deepression.csv")
    df.to_csv(ROOT / "Deepression_clean.csv", index=False)

    print("\n[1] Dataset cleaning")
    print(f"    rows loaded ............... {report['rows_loaded']}")
    print(f"    dropped (bad/empty label) . {report['rows_dropped_bad_target']}")
    print(f"    out-of-range cells clipped  {report['cells_clipped_out_of_range']}")
    print(f"    usable rows ............... {report['rows_clean']}")
    print(f"    class counts .............. {report['class_counts']}")

    print("\n[2] Data quality audit")
    print(f"    unique symptom profiles ... {report['unique_feature_rows']} "
          f"(out of {report['rows_clean']} rows)")
    print(f"    contradictory profiles .... {report['contradictory_combinations']}"
          f"/{report['total_combinations']}")
    print(f"    accuracy ceiling .......... {report['bayes_accuracy_ceiling']:.1%}")
    if report["bayes_accuracy_ceiling"] < 0.7:
        print("    !  WARNING: same symptoms carry different labels in this CSV.")
        print("       Koi bhi model is ceiling se upar nahi ja sakta.")

    X = df[FEATURE_COLUMNS].to_numpy()
    y = df[TARGET].to_numpy()

    # ---------------- 2. compare models ---------------------------------
    print("\n[3] Cross-validated model comparison (stratified 5-fold)")
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    results: dict = {}

    for name, pipe in build_candidates().items():
        scores = cross_val_score(pipe, X, y, cv=cv, scoring="accuracy", n_jobs=-1)
        results[name] = {"mean": float(scores.mean()), "std": float(scores.std())}
        print(f"    {name:<24} {scores.mean():.3f} +/- {scores.std():.3f}")

    contenders = {k: v for k, v in results.items() if k != "baseline_majority"}
    best_name = max(contenders, key=lambda k: contenders[k]["mean"])
    best_cv = contenders[best_name]["mean"]
    baseline = results["baseline_majority"]["mean"]
    print(f"\n    best model -> {best_name} ({best_cv:.3f})")
    print(f"    majority-class baseline    {baseline:.3f}")

    # ---------------- 3. held-out check ---------------------------------
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=RANDOM_STATE
    )
    best_pipe = build_candidates()[best_name]
    best_pipe.fit(X_tr, y_tr)
    y_pred = best_pipe.predict(X_te)
    holdout_acc = float(accuracy_score(y_te, y_pred))

    print(f"\n[4] Held-out test accuracy ... {holdout_acc:.3f} (n={len(y_te)})")
    print("\n" + classification_report(y_te, y_pred, zero_division=0))

    labels_sorted = sorted(set(y.tolist()))
    cm = confusion_matrix(y_te, y_pred, labels=labels_sorted)

    # ---------------- 4. refit on everything ----------------------------
    final_pipe = build_candidates()[best_name]
    final_pipe.fit(X, y)

    reliable = bool(best_cv >= RELIABILITY_THRESHOLD and best_cv > baseline + 0.05)

    bundle = {
        "pipeline": final_pipe,
        "feature_columns": FEATURE_COLUMNS,
        "classes": list(final_pipe.classes_),
        "model_name": best_name,
        "cv_accuracy": best_cv,
        "cv_std": contenders[best_name]["std"],
        "holdout_accuracy": holdout_acc,
        "baseline_accuracy": baseline,
        "accuracy_ceiling": report["bayes_accuracy_ceiling"],
        "reliable": reliable,
        "n_training_rows": int(len(df)),
        "sklearn_version": __import__("sklearn").__version__,
    }
    joblib.dump(bundle, MODEL_DIR / "model_bundle.joblib")

    metrics = {
        "dataset_report": report,
        "cv_results": results,
        "selected_model": best_name,
        "cv_accuracy": best_cv,
        "holdout_accuracy": holdout_acc,
        "baseline_accuracy": baseline,
        "reliable": reliable,
        "reliability_threshold": RELIABILITY_THRESHOLD,
        "confusion_matrix": {"labels": labels_sorted, "matrix": cm.tolist()},
    }
    (MODEL_DIR / "metrics.json").write_text(json.dumps(metrics, indent=2))

    print("\n[5] Saved")
    print("    model/model_bundle.joblib")
    print("    model/metrics.json")
    print("    Deepression_clean.csv")

    print("\n[6] Verdict")
    if reliable:
        print("    OK - Model reliable hai, app ise result me use karega.")
    else:
        print("    !  Model is dataset par bharosemand nahi hai.")
        print("       App rule-based clinical scoring engine ko PRIMARY rakhega,")
        print("       aur ML output ko sirf secondary reference ke taur par dikhayega.")
        print("       Behtar model ke liye better-labelled data chahiye.")
    print("=" * 66)


if __name__ == "__main__":
    main()

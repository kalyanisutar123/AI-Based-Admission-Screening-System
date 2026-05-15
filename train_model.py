import os
import json
import pickle

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from typing import Tuple, Any


# ---------------------------------------------------------------------------
# PATHS
# ---------------------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "model")
os.makedirs(MODEL_DIR, exist_ok=True)

DATASET_PATH = os.path.join(MODEL_DIR, "college_admission_dataset.csv")


# ---------------------------------------------------------------------------
# GENERATE DATASET
# ---------------------------------------------------------------------------

def generate_dataset(path: str, n: int = 500) -> pd.DataFrame:
    """Create a synthetic admission dataset and save it as CSV."""
    np.random.seed(42)

    genders = ["Male", "Female", "Other"]
    courses = [
        "Computer Science",
        "Electronics",
        "Mechanical",
        "Civil",
        "IT",
        "Biotechnology",
        "MBA",
        "General",
        "Artificial Intelligence and Machine Learning",
    ]

    data = {
        "name":            [f"Student_{i}" for i in range(1, n + 1)],
        "age":             np.random.randint(17, 22, n),
        "gender":          np.random.choice(genders, n),
        "marks_10":        np.round(np.random.uniform(50, 100, n), 2),
        "marks_12":        np.round(np.random.uniform(50, 100, n), 2),
        "entrance_score":  np.round(np.random.uniform(40, 100, n), 2),
        "preferred_course": np.random.choice(courses, n),
    }

    df = pd.DataFrame(data)

    composite = (
        df["marks_10"] * 0.25
        + df["marks_12"] * 0.40
        + df["entrance_score"] * 0.35
    )
    df["Eligible"] = np.where(composite >= 60, "Yes", "No")

    df.to_csv(path, index=False)
    print(f" Dataset generated → {path} ({n} rows)")
    return df


if not os.path.exists(DATASET_PATH):
    print(f"Dataset not found at {DATASET_PATH} — generating now …")
    df = generate_dataset(DATASET_PATH)
else:
    df = pd.read_csv(DATASET_PATH)
    print(f"Dataset loaded from {DATASET_PATH}")

print(f"\nShape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")

required_columns = [
    "age", "marks_10", "marks_12", "entrance_score",
    "gender", "preferred_course", "Eligible",
]
for col in required_columns:
    if col not in df.columns:
        raise ValueError(
            f"Missing required column: '{col}'. "
            "Please check your dataset or delete it so it gets regenerated."
        )

le_gender = LabelEncoder()
le_course  = LabelEncoder()

df["gender_enc"] = le_gender.fit_transform(df["gender"].astype(str))
df["course_enc"] = le_course.fit_transform(df["preferred_course"].astype(str))

print("\nGender classes :", list(le_gender.classes_))
print("Course  classes :", list(le_course.classes_))

FEATURE_COLS = ["age", "marks_10", "marks_12", "entrance_score", "gender_enc", "course_enc"]
X = df[FEATURE_COLS].values

eligible_col = df["Eligible"].astype(str).str.strip().str.lower()
y = (eligible_col == "yes").astype(int).values

print(f"\nClass distribution — Eligible: {y.sum()}, Not Eligible: {(1 - y).sum()}")

# ---------------------------------------------------------------------------
# SCALE
# ---------------------------------------------------------------------------

scaler = StandardScaler()
X_scaled: np.ndarray[Tuple[int, int], np.dtype[np.float64]] = scaler.fit_transform(X)

# ---------------------------------------------------------------------------
# TRAIN / TEST SPLIT
# ---------------------------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

# ---------------------------------------------------------------------------
# TRAIN RANDOM FOREST
# ---------------------------------------------------------------------------

model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

from sklearn.metrics import accuracy_score, classification_report

print("=== Random Forest Results ===")

accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy : {accuracy*100:.2f}%")

print(classification_report(y_test, y_pred, target_names=["Not Eligible", "Eligible"], zero_division=0))

# ---------------------------------------------------------------------------
# SAVE MODEL ARTEFACTS
# ---------------------------------------------------------------------------

def save_pkl(obj, filename: str) -> None:
    path = os.path.join(MODEL_DIR, filename)
    with open(path, "wb") as f:
        pickle.dump(obj, f)
    print(f" {filename} saved → {path}")

save_pkl(model,     "model.pkl")
save_pkl(scaler,    "scaler.pkl")
save_pkl(le_gender, "le_gender.pkl")
save_pkl(le_course, "le_course.pkl")

# ---------------------------------------------------------------------------
# COLLEGE CUTOFFS
# ---------------------------------------------------------------------------

college_cutoffs = [
    {"name": "IIT Bombay",                  "courses": ["Artificial Intelligence and Machine Learning","Computer Science"], "cutoff": 98},
    {"name": "COEP Pune",                   "courses": ["Computer Science","Artificial Intelligence and Machine Learning","Mechanical"],  "cutoff": 96 },
    {"name": "PICT Pune",                 "courses": ["Computer Science","Artificial Intelligence and Machine Learning","IT"], "cutoff": 91 },
    {"name": "Shivaji University Kolhapur",          "courses": ["Computer Science","IT"], "cutoff": 88 },
    {"name": "Walchand College of Engineering, Sangli",                 "courses": ["Computer Science","IT","Electronics"],"cutoff": 86 },
    {"name": "Rajarambapu Institute of Technology",                  "courses":["Computer Science","Artificial Intelligence and Machine Learning","Electronics"], "cutoff": 86 },
    {"name": "KIT College of Engineering, Kolhapur",                  "courses": ["Computer Science","IT"],          "cutoff": 84},
    {"name": "D Y Patil College of Engineering and Technology",                    "courses": ["Computer Science","Electronics"], "cutoff": 82},
    {"name": "D.K.T.E. Society's Textile and Engineering Institute",               "courses": ["Computer Science","Mechanical"],  "cutoff": 81},
    {"name": "AITRC, Vita",                "courses": ["Computer Science","Artificial Intelligence and Machine Learning"], "cutoff": 79},
    {"name": "Bharati Vidyapeeth's College of Engineering",            "courses": ["Computer Science","Mechanical"],  "cutoff": 78},
    {"name": "Ashokrao Mane Group of Institutions",               "courses": ["Computer Science","Artificial Intelligence and Machine Learning"],       "cutoff": 75},
    {"name": "PVPIT, Tasgaon",  "courses": ["Artificial Intelligence and Machine Learning","Civil"],             "cutoff": 74},
    {"name": "Annasaheb Dange College of Engineering and Technology",          "courses": ["Computer Science","Electronics"],"cutoff": 73},
    {"name": "Arvind Gavali College of Engineering", "courses":["Computer Science","General"],"cutoff": 72},
    {"name": "Yashoda Technical Campus",  "courses":["Computer Science","General"],"cutoff": 69},
    {"name": "Other",                       "courses": ["General"],                                   "cutoff": 66},
]

cutoffs_path = os.path.join(MODEL_DIR, "college_cutoffs.json")
with open(cutoffs_path, "w") as f:
    json.dump(college_cutoffs, f, indent=2)
print(f"college_cutoffs.json saved → {cutoffs_path}")

print("\n All model files saved successfully!")
print(f" Location: {MODEL_DIR}") 
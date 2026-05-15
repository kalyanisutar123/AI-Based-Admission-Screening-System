"""
app.py  —  AdmitIQ Flask Backend
Run:  python app.py
"""

import hashlib
import json
import os
import pickle
import secrets
import sqlite3

import numpy as np
from flask import Flask, jsonify, request, send_from_directory, session

# ---------------------------------------------------------------------------
# FLASK APP
# ---------------------------------------------------------------------------

app = Flask(__name__, static_folder="frontend", static_url_path="")
app.secret_key = secrets.token_hex(16)

# ---------------------------------------------------------------------------
# PATHS
# ---------------------------------------------------------------------------

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "model")
DB_DIR    = os.path.join(BASE_DIR, "database")

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(DB_DIR, exist_ok=True)

DB_PATH = os.path.join(DB_DIR, "admission.db")

# ---------------------------------------------------------------------------
# LOAD MODEL FILES
# ---------------------------------------------------------------------------

def _load(filename: str):
    path = os.path.join(MODEL_DIR, filename)

    with open(path, "rb") as f:
        return pickle.load(f)


try:
    model      = _load("model.pkl")
    scaler     = _load("scaler.pkl")
    le_gender  = _load("le_gender.pkl")
    le_course  = _load("le_course.pkl")

    with open(os.path.join(MODEL_DIR, "college_cutoffs.json"), "r") as f:
        college_cutoffs = json.load(f)

    print(" Model files loaded successfully!")

except FileNotFoundError as exc:
    print(f" Missing model file: {exc}")
    raise SystemExit(1)

except Exception as exc:
    print(f" Error loading model files: {exc}")
    raise SystemExit(1)

# ---------------------------------------------------------------------------
# DATABASE
# ---------------------------------------------------------------------------

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _hash_pw(pw: str):
    return hashlib.sha256(pw.encode()).hexdigest()


def init_db():

    conn = get_db()

    # STUDENTS TABLE
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT,
            age INTEGER,
            gender TEXT,

            marks_10 REAL,
            marks_12 REAL,
            entrance_score REAL,

            preferred_course TEXT,

            composite_score REAL,

            prediction TEXT,

            recommended_college TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # USERS TABLE
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    """)

    # DEFAULT ADMIN
    admin = conn.execute(
        "SELECT * FROM users WHERE username='admin'"
    ).fetchone()

    if not admin:

        conn.execute("""
            INSERT INTO users (username, password, role)
            VALUES (?, ?, ?)
        """, (
            "admin",
            _hash_pw("admin123"),
            "admin"
        ))

    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# LOGIN HELPERS
# ---------------------------------------------------------------------------

def _current_user():
    return session.get("user")


def _require_login():

    if not _current_user():

        return jsonify({
            "success": False,
            "message": "Unauthorized"
        }), 401

    return None


# ---------------------------------------------------------------------------
# COLLEGE RECOMMENDATION
# ---------------------------------------------------------------------------

def recommend_colleges(composite_score):

    recommendations = []

    for c in college_cutoffs:

        if composite_score >= c["cutoff"]:

            recommendations.append({
                "college": c["name"],
                "cutoff": c["cutoff"]
            })

    return recommendations[:5]


# ---------------------------------------------------------------------------
# FRONTEND ROUTES
# ---------------------------------------------------------------------------

@app.route("/")
def home():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(app.static_folder, path)


# ---------------------------------------------------------------------------
# AUTH ROUTES
# ---------------------------------------------------------------------------

@app.route("/api/login", methods=["POST"])
def login():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    conn = get_db()

    user = conn.execute("""
        SELECT * FROM users
        WHERE username = ?
        AND password = ?
    """, (
        username,
        _hash_pw(password)
    )).fetchone()

    conn.close()

    if user:

        session["user"] = username
        session["role"] = user["role"]

        return jsonify({
            "success": True,
            "role": user["role"]
        })

    return jsonify({
        "success": False,
        "message": "Invalid credentials"
    })


@app.route("/api/logout", methods=["POST"])
def logout():

    session.clear()

    return jsonify({
        "success": True
    })


# ---------------------------------------------------------------------------
# PREDICTION ROUTE
# ---------------------------------------------------------------------------

@app.route("/api/predict", methods=["POST"])
def predict():

    data = request.get_json()

    try:

        name             = data["name"]
        age              = int(data["age"])
        gender           = data["gender"]

        marks_10         = float(data["marks_10"])
        marks_12         = float(data["marks_12"])

        entrance_score   = float(data["entrance_score"])

        preferred_course = data["preferred_course"]

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        })

    # ENCODING
    gender_encoded = int(le_gender.transform([gender])[0])

    if preferred_course in le_course.classes_:
        course_encoded = int(le_course.transform([preferred_course])[0])
    else:
        course_encoded = 0

    # FEATURE VECTOR
    features = np.array([[
        age,
        marks_10,
        marks_12,
        entrance_score,
        gender_encoded,
        course_encoded
    ]])

    scaled = scaler.transform(features)

    # MODEL PREDICTION
    prediction = int(model.predict(scaled)[0])

    probabilities = model.predict_proba(scaled)[0]

    confidence = round(float(max(probabilities)) * 100, 2)

    prediction_text = "Eligible" if prediction == 1 else "Not Eligible"

    # COMPOSITE SCORE
    composite_score = round(
        (marks_10 * 0.25) +
        (marks_12 * 0.40) +
        (entrance_score * 0.35),
        2
    )

    recommendations = recommend_colleges(composite_score)

    recommended_college = (
        recommendations[0]["college"]
        if recommendations else "N/A"
    )

    # SAVE TO DATABASE
    conn = get_db()

    conn.execute("""
        INSERT INTO students (

            name,
            age,
            gender,

            marks_10,
            marks_12,
            entrance_score,

            preferred_course,

            composite_score,

            prediction,

            recommended_college

        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        name,
        age,
        gender,

        marks_10,
        marks_12,
        entrance_score,

        preferred_course,

        composite_score,

        prediction_text,

        recommended_college
    ))

    conn.commit()
    conn.close()

    return jsonify({

        "success": True,

        "prediction": prediction_text,

        "confidence": confidence,

        "composite_score": composite_score,

        "recommendations": recommendations
    })


# ---------------------------------------------------------------------------
# ADMIN STATS
# ---------------------------------------------------------------------------

@app.route("/api/admin/stats")
def admin_stats():

    conn = get_db()

    total = conn.execute(
        "SELECT COUNT(*) FROM students"
    ).fetchone()[0]

    eligible = conn.execute("""
        SELECT COUNT(*)
        FROM students
        WHERE prediction='Eligible'
    """).fetchone()[0]

    avg_comp = conn.execute("""
        SELECT AVG(composite_score)
        FROM students
    """).fetchone()[0]

    conn.close()

    return jsonify({

        "total": total,

        "Eligible": eligible,

        "Not_Eligible": total - eligible,

        "admission_rate":
            round((eligible / total) * 100, 2)
            if total else 0,

        "avg_composite":
            round(avg_comp or 0, 2)
    })


# ---------------------------------------------------------------------------
# ADMIN STUDENTS
# ---------------------------------------------------------------------------

@app.route("/api/admin/students")
def admin_students():

    conn = get_db()

    rows = conn.execute("""
        SELECT *
        FROM students
        ORDER BY created_at DESC
    """).fetchall()

    conn.close()

    return jsonify([
        dict(r) for r in rows
    ])


# ---------------------------------------------------------------------------
# DELETE STUDENT
# ---------------------------------------------------------------------------

@app.route("/api/admin/delete_student/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):

    conn = get_db()

    conn.execute("""
        DELETE FROM students
        WHERE id = ?
    """, (student_id,))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Student deleted successfully"
    })


# ---------------------------------------------------------------------------
# UPDATE STUDENT
# ---------------------------------------------------------------------------

@app.route("/api/admin/update_student/<int:student_id>", methods=["PUT"])
def update_student(student_id):

    data = request.get_json()

    conn = get_db()

    conn.execute("""

        UPDATE students

        SET

            name = ?,
            age = ?,
            gender = ?,

            marks_10 = ?,
            marks_12 = ?,
            entrance_score = ?,

            preferred_course = ?

        WHERE id = ?

    """, (

        data["name"],
        data["age"],
        data["gender"],

        data["marks_10"],
        data["marks_12"],
        data["entrance_score"],

        data["preferred_course"],

        student_id
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Student updated successfully"
    })


# ---------------------------------------------------------------------------
# COLLEGES
# ---------------------------------------------------------------------------

@app.route("/api/colleges")
def colleges():
    return jsonify(college_cutoffs)


# ---------------------------------------------------------------------------
# RUN APP
# ---------------------------------------------------------------------------

if __name__ == "__main__":

    init_db()

    print("\n AdmitIQ Server Starting...")
    print(" http://127.0.0.1:5000\n")

    app.run(debug=True, use_reloader=False)
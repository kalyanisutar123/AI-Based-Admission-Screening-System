# AdmitIQ — AI-Based College Admission Screening System

## Project Overview
AdmitIQ is an AI-powered web application that predicts college admission eligibility for students applying to Maharashtra universities. It uses a **Random Forest ML model** trained on academic data (10th marks, 12th marks, entrance score) to produce instant admission predictions with college recommendations.

**Technologies:** Python · Flask · scikit-learn · SQLite · HTML/CSS/JavaScript · Chart.js

---

## Project Structure
```
project/
├── app.py                    ← Flask backend (all API routes)
├── requirements.txt          ← Python dependencies
├── frontend/
│   ├── index.html            ← Home page
│   ├── login.html            ← Login & Register page
│   ├── form.html             ← Admission application form
│   ├── result.html           ← Prediction result page
│   ├── colleges.html         ← Maharashtra colleges list
│   ├── admin.html            ← Admin dashboard with charts
│   ├── style.css             ← Shared CSS (dark/light theme)
│   └── app.js                ← Shared JS utilities
├── model/
│   ├── generate_dataset.py   ← Creates dataset.csv (200 rows)
│   ├── train_model.py        ← Trains and saves ML model
│   ├── dataset.csv           ← Generated training data
│   ├── model.pkl             ← Trained Random Forest model
│   ├── scaler.pkl            ← StandardScaler
│   ├── le_gender.pkl         ← Gender LabelEncoder
│   ├── le_course.pkl         ← Course LabelEncoder
│   └── college_cutoffs.json  ← College cutoff data
└── database/
    ├── init_db.py            ← Creates SQLite tables & default users
    └── admission.db          ← SQLite database (auto-created)
```

---

### Step 1 — Clone / Download and open in VS Code
```bash
cd project
code .
```

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Generate dataset and train the model
```bash
python model/generate_dataset.py
python model/train_model.py
```

### Step 4 — Initialize the database
```bash
python database/init_db.py
```

### Step 5 — Run the Flask server
```bash
python app.py
```

### Step 6 — Open in browser
Navigate to: **http://127.0.0.1:5000**

---

## Default Login Credentials

| Role    | Username  | Password    |
|---------|-----------|-------------|
| Admin   | `admin`   | `admin123`  |
| Student | `student` | `student123`|

---

## Pages

| URL                              | Description              |
|----------------------------------|--------------------------|
| http://127.0.0.1:5000/           | Home page                |
| http://127.0.0.1:5000/login.html | Login / Register         |
| http://127.0.0.1:5000/form.html  | Admission form           |
| http://127.0.0.1:5000/result.html| Prediction result        |
| http://127.0.0.1:5000/colleges.html | College list & cutoffs |
| http://127.0.0.1:5000/admin.html | Admin dashboard          |

---

## 🔌 API Endpoints

| Method | Endpoint              | Description                    |
|--------|-----------------------|--------------------------------|
| POST   | /api/login            | Login with username + password |
| POST   | /api/register         | Register new student account   |
| POST   | /api/logout           | Logout                         |
| POST   | /api/predict          | Run ML prediction              |
| GET    | /api/colleges         | List all colleges + cutoffs    |
| GET    | /api/admin/students   | All student records            |
| GET    | /api/admin/stats      | Dashboard statistics           |

---

## ML Model Details

- **Algorithm:** Random Forest Classifier (100 trees)
- **Accuracy:** ~92.5%
- **Features:** age, 10th%, 12th%, entrance score, gender, preferred course
- **Composite Score Formula:** `(10th × 0.25) + (12th × 0.40) + (entrance × 0.35)`

### College Cutoff Tiers
| Score Range | Tier Example |
|-------------|-------------|
| 90+         | IIT Bombay |
| 80-90       | COEP, VJTI, SPIT |
| 70-80       | MIT Pune, Symbiosis |
| 60-70       | Walchand, DY Patil |
| 50-60       | Other Colleges |

---

## Features
- Dark / Light mode toggle
- Login & Registration with hashed passwords
- Show/hide password toggle
- Student admission form with live score preview
- AI prediction with confidence score
- Top 5 college recommendations
- Admin dashboard with 4 charts (Chart.js)
- Student table with search, filter, CSV export
- 30+ Maharashtra colleges with cutoffs
- Responsive design (mobile-friendly)
- SQLite database for persistence

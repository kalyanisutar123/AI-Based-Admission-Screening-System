import pandas as pd
import numpy as np
import random

random.seed(42)
np.random.seed(42)

colleges = [
    {"name": "IIT Bombay", "course": "Artificial Intelligence and Machine Learning", "cutoff": 98},
    {"name": "IIT Bombay", "course": "Computer Engineering", "cutoff": 97},
    {"name": "COEP Pune", "course": "Artificial Intelligence and Machine Learning", "cutoff":96 },
    {"name": "COEP Pune", "course": "Computer Engineering", "cutoff": 95},
    {"name": "COEP Pune", "course": "Mechanical", "cutoff": 93},
    {"name": "PICT Pune", "course": "Artificial Intelligence and Machine Learning", "cutoff": 91},
    {"name": "PICT Pune", "course": "Computer Science", "cutoff": 90},
    {"name": "PICT Pune", "course": "IT", "cutoff": 89},
    {"name": "Shivaji University Kolhapur", "course": "Computer Science", "cutoff": 88},
    {"name": "Shivaji University Kolhapur", "course": "IT", "cutoff": 87},
    {"name": "Walchand Sangli", "course": "Computer Science", "cutoff": 86},
    {"name": "Walchand Sangli", "course": "IT", "cutoff": 85},
    {"name": "Walchand Sangli", "course": "Electronics", "cutoff": 78},
    {"name": "Rajarambapu Institute of Technology", "course": "Computer Science", "cutoff": 86},
    {"name": "Rajarambapu Institute of Technology", "course": "Artificial Intelligence and Machine Learning", "cutoff": 85},
    {"name": "Rajarambapu Institute of Technology", "course": "Electronics", "cutoff": 80},
    {"name": "KIT College of Engineering, Kolhapur", "course": "Computer Science", "cutoff": 86},
    {"name": "KIT College of Engineering, Kolhapur", "course": "Computer Science", "cutoff": 85},
    {"name": "D Y Patil College of Engineering and Technology", "course": "Computer Science", "cutoff": 82},
    {"name": "D Y Patil College of Engineering and Technology", "course": "Electronics", "cutoff": 81},
    {"name": "D.K.T.E. Society's Textile and Engineering Institute", "course": "Computer Science", "cutoff": 81},
    {"name": "D.K.T.E. Society's Textile and Engineering Institute", "course": "Mechanical", "cutoff": 80},
    {"name": "AITRC, Vita", "course": "Artificial Intelligence and Machine Learning", "cutoff": 79},
    {"name": "AITRC, Vita", "course": "Computer Science", "cutoff": 78},
    {"name": "Bharati Vidyapeeth's College of Engineering", "course": "Computer Science", "cutoff": 78},
    {"name": "Bharati Vidyapeeth's College of Engineering", "course": "Mechanical", "cutoff": 77},
    {"name": "Ashokrao Mane Group of Institutions", "course": "Computer Science", "cutoff": 75},
    {"name": "Ashokrao Mane Group of Institutions", "course": "Artificial Intelligence and Machine Learning", "cutoff": 74},
    {"name": "PVPIT, Tasgaon", "course": "Artificial Intelligence and Machine Learning", "cutoff": 74},
    {"name": "PVPIT, Tasgaon", "course": "Civil", "cutoff": 73},
    {"name": "Annasaheb Dange College of Engineering and Technology", "course": "Computer Science", "cutoff": 73},
    {"name": "Annasaheb Dange College of Engineering and Technology", "course": "Electronics", "cutoff": 72},
    {"name": "Arvind Gavali College of Engineering", "course": "Computer Science", "cutoff": 72},
    {"name": "Arvind Gavali College of Engineering", "course": "Electronics", "cutoff": 71},
    {"name": "Yashoda Technical Campus", "course": "Computer Science", "cutoff": 69},
    {"name": "Yashoda Technical Campus", "course": "General", "cutoff": 64},
    {"name": "Dadasaheb Mokashi College of Food Technology", "course": "Mechanical", "cutoff": 68},
    {"name": "Dadasaheb Mokashi College of Food Technology", "course": "Civil", "cutoff": 67},
    {"name": "Other", "course": "General", "cutoff": 66},
    ];

names_m = ["Aarav","Rohan","Arjun","Vivek","Siddharth","Karan","Rahul","Nikhil","Amit","Suraj",
           "Pranav","Yash","Akash","Dev","Raj","Mohit","Tejas","Ankit","Vishal","Gaurav"]
names_f = ["Kalyani","Sanjana","Pranali","Rajani","Vaibhavi","Priya","Sneha","Pooja","Ananya","Riya","Kavya","Sakshi","Neha","Ishita","Divya",
           "Swati","Nisha","Aisha","Meera","Tanvi","Shruti","Aditi","Komal","Sonal","Pallavi"]

courses = ["Artificial Intelligence and Machine Learning","Computer Science","Electronics","Mechanical","Civil","IT","Biotechnology","MBA","General"]
genders = ["Male","Female","Other"]


data = []
for i in range(200):
    gender = random.choices(["Male","Female","Other"], weights=[55,43,2])[0]
    name = random.choice(names_m if gender == "Male" else names_f) + " " + random.choice(
        ["Sharma","Patil","Desai","Joshi","Kulkarni","Rao","Nair","Mehta","Shah","Gupta",
         "Pawar","Shinde","Deshpande","Jadhav","Gaikwad","More","Salunke","Bhosale","Naik","Wagh"])
    age = random.randint(17, 22)
    marks_10 = round(random.uniform(45, 99), 2)
    marks_12 = round(random.uniform(40, 99), 2)
    entrance_score = round(random.uniform(20, 100), 2)
    preferred_course = random.choice(courses)

    # Composite score for admission logic
    composite = (marks_10 * 0.25) + (marks_12 * 0.40) + (entrance_score * 0.35)

    # Assign college based on composite score
    Eligible = "No"
    assigned_college = "Not Eligible"
    assigned_cutoff = 0

    if composite >= 90:
        college_entry = random.choice([c for c in colleges if c["cutoff"] >= 90])
        Eligible = "Yes"
    elif composite >= 80:
        college_entry = random.choice([c for c in colleges if 80 <= c["cutoff"] < 90])
        Eligible = "Yes"
    elif composite >= 70:
        college_entry = random.choice([c for c in colleges if 70 <= c["cutoff"] < 80])
        Eligible = "Yes"
    elif composite >= 60:
        college_entry = random.choice([c for c in colleges if 60 <= c["cutoff"] < 70])
        Eligible = "Yes"
    elif composite >= 50:
        college_entry = colleges[-1]  # Other
        Eligible = "Yes"
    else:
        Eligible = "No"
        college_entry = {"name": "Not Eligible", "course": preferred_course, "cutoff": 0}

    data.append({
        "id": i + 1,
        "name": name,
        "age": age,
        "gender": gender,
        "marks_10": marks_10,
        "marks_12": marks_12,
        "entrance_score": entrance_score,
        "preferred_course": preferred_course,
        "composite_score": round(composite, 2),
        "Eligible": Eligible,
        "assigned_college": college_entry["name"],
        "assigned_course": college_entry["course"],
        "college_cutoff": college_entry["cutoff"]
    })

df = pd.DataFrame(data)
df.to_csv("C:/AdmitIQ/model/college_admission_dataset.csv", index=False)
print(f"Dataset generated: {len(df)} rows")
print(df["Eligible"].value_counts())
print(df.head(5).to_string())
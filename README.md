# Student Academic Performance Analysis Dashboard

A beginner-friendly B.Tech mini-project built with Python, NumPy, Pandas, Matplotlib, and Streamlit.

## Features
- Load the included sample CSV or upload a CSV file.
- Validate required columns and marks from 0–100.
- Calculate total marks, average marks, grades, pass/fail status, and rank.
- View subject averages, grade distribution, marks distribution, and class comparisons.
- Search and filter student records.
- Download filtered analyzed results as CSV.

## Requirements
- Python 3.10 or newer recommended
- pip
- A web browser

## Run on Ubuntu/Linux
Open a terminal in this project folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Streamlit normally opens the app in your browser. If it does not, open the local URL printed in the terminal (usually `http://localhost:8501`).

## Run on Windows
```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

## CSV format
Required columns:
`Student_ID, Student_Name, Class, Department, Semester, Math, Science, English, Computer`

Subject marks must be numeric values from 0 to 100, and Student_ID should be unique.

## Demonstration grading rules
- Pass: average is at least 40 and every subject mark is at least 35.
- A: average >= 80
- B: average >= 70
- C: average >= 60
- D: average >= 50
- E: average >= 40
- F: average < 40

These rules are for demonstration only. Replace them with your institution's official grading and passing rules before analyzing real academic results.

## Project structure
```text
app.py
data/student_data.csv
modules/data_loader.py
modules/analysis.py
modules/visualization.py
docs/
assets/
requirements.txt
README.md
```

## Important
The included data is fictional and created for demonstration. Do not upload identifiable student records without authorization. Verify the calculations before using the output for any official decision.

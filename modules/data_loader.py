from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = [
    "Student_ID", "Student_Name", "Class", "Department", "Semester",
    "Math", "Science", "English", "Computer"
]
SUBJECT_COLUMNS = ["Math", "Science", "English", "Computer"]

def load_student_data(uploaded_file=None):
    """Load the uploaded CSV, or use the included sample data."""
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        data_path = Path(__file__).resolve().parents[1] / "data" / "student_data.csv"
        df = pd.read_csv(data_path)
    return df

def validate_student_data(df):
    """Return a list of readable validation errors; empty means valid."""
    errors = []
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        errors.append("Missing required column(s): " + ", ".join(missing))
        return errors
    if df.empty:
        errors.append("The dataset contains no student records.")
        return errors
    for col in SUBJECT_COLUMNS:
        numeric = pd.to_numeric(df[col], errors="coerce")
        if numeric.isna().any():
            errors.append(f"Column '{col}' contains missing or non-numeric marks.")
        elif ((numeric < 0) | (numeric > 100)).any():
            errors.append(f"Column '{col}' must contain marks from 0 to 100.")
    if df["Student_ID"].astype(str).duplicated().any():
        errors.append("Student_ID values should be unique.")
    return errors

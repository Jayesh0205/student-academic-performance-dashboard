import numpy as np
import pandas as pd
from modules.data_loader import SUBJECT_COLUMNS

def add_derived_columns(df):
    """Return a copy with total, average, grade, result, and rank columns."""
    result = df.copy()
    for subject in SUBJECT_COLUMNS:
        result[subject] = pd.to_numeric(result[subject], errors="coerce")
    result["Total_Marks"] = result[SUBJECT_COLUMNS].sum(axis=1)
    result["Average_Marks"] = result[SUBJECT_COLUMNS].mean(axis=1)
    result["Grade"] = result["Average_Marks"].apply(assign_grade)
    subject_pass = (result[SUBJECT_COLUMNS] >= 35).all(axis=1)
    result["Result"] = np.where((result["Average_Marks"] >= 40) & subject_pass, "Pass", "Fail")
    result["Rank"] = result["Average_Marks"].rank(method="min", ascending=False).astype(int)
    return result

def assign_grade(average):
    if average >= 80:
        return "A"
    if average >= 70:
        return "B"
    if average >= 60:
        return "C"
    if average >= 50:
        return "D"
    if average >= 40:
        return "E"
    return "F"

def summary_metrics(df):
    if df.empty:
        return {"total_students": 0, "average_marks": 0.0, "pass_percentage": 0.0, "highest_average": 0.0}
    pass_percentage = (df["Result"].eq("Pass").mean() * 100)
    return {
        "total_students": int(len(df)),
        "average_marks": float(np.mean(df["Average_Marks"])),
        "pass_percentage": float(pass_percentage),
        "highest_average": float(df["Average_Marks"].max())
    }

def subject_summary(df):
    rows = []
    for subject in SUBJECT_COLUMNS:
        rows.append({
            "Subject": subject,
            "Average": df[subject].mean(),
            "Highest": df[subject].max(),
            "Lowest": df[subject].min(),
            "Students >= 40": int((df[subject] >= 40).sum())
        })
    return pd.DataFrame(rows)

def grade_summary(df):
    order = ["A", "B", "C", "D", "E", "F"]
    return df["Grade"].value_counts().reindex(order, fill_value=0)

def student_rankings(df):
    cols = ["Rank", "Student_ID", "Student_Name", "Class", "Department", "Average_Marks", "Grade", "Result"]
    return df[cols].sort_values(["Rank", "Student_Name"])

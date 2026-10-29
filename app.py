import streamlit as st
import pandas as pd
from modules.data_loader import load_student_data, validate_student_data
from modules.analysis import add_derived_columns, summary_metrics, subject_summary, grade_summary, student_rankings
from modules.visualization import subject_bar_chart, grade_pie_chart, marks_histogram, class_comparison_chart

st.set_page_config(page_title="Student Academic Performance Dashboard", page_icon="🎓", layout="wide")
st.title("🎓 Student Academic Performance Analysis Dashboard")
st.caption("Analyze student marks, grades, and class performance using Python, Pandas, NumPy, Matplotlib, and Streamlit.")

with st.sidebar:
    st.header("Dataset")
    uploaded_file = st.file_uploader("Upload a CSV file (optional)", type=["csv"])
    st.info("Expected columns: Student_ID, Student_Name, Class, Department, Semester, Math, Science, English, Computer")
    st.markdown("---")
    st.caption("Tip: Start with the included sample dataset.")

try:
    raw_df = load_student_data(uploaded_file)
    errors = validate_student_data(raw_df)
    if errors:
        st.error("The dataset needs a few corrections:")
        for error in errors:
            st.write(f"• {error}")
        st.stop()
    df = add_derived_columns(raw_df)
except Exception as exc:
    st.error(f"Could not load the dataset: {exc}")
    st.stop()

with st.sidebar:
    st.subheader("Filters")
    classes = sorted(df["Class"].dropna().astype(str).unique().tolist())
    departments = sorted(df["Department"].dropna().astype(str).unique().tolist())
    selected_classes = st.multiselect("Class", classes, default=classes)
    selected_departments = st.multiselect("Department", departments, default=departments)

filtered = df[
    df["Class"].astype(str).isin(selected_classes) &
    df["Department"].astype(str).isin(selected_departments)
].copy()

if filtered.empty:
    st.warning("No records match these filters. Select at least one class and department.")
    st.stop()

metrics = summary_metrics(filtered)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Students", f"{metrics['total_students']:,}")
c2.metric("Average Marks", f"{metrics['average_marks']:.1f}%")
c3.metric("Pass Percentage", f"{metrics['pass_percentage']:.1f}%")
c4.metric("Highest Average", f"{metrics['highest_average']:.1f}%")

st.markdown("---")
tab1, tab2, tab3 = st.tabs(["📊 Overview", "👩‍🎓 Student Records", "📈 Detailed Analysis"])

with tab1:
    left, right = st.columns(2)
    with left:
        st.subheader("Average Marks by Subject")
        st.pyplot(subject_bar_chart(filtered), clear_figure=True)
    with right:
        st.subheader("Grade Distribution")
        st.pyplot(grade_pie_chart(filtered), clear_figure=True)
    left2, right2 = st.columns(2)
    with left2:
        st.subheader("Distribution of Student Averages")
        st.pyplot(marks_histogram(filtered), clear_figure=True)
    with right2:
        st.subheader("Average Performance by Class")
        st.pyplot(class_comparison_chart(filtered), clear_figure=True)

with tab2:
    st.subheader("Search and inspect student records")
    search = st.text_input("Search by student name or ID")
    display_df = filtered.copy()
    if search.strip():
        query = search.strip().lower()
        display_df = display_df[
            display_df["Student_Name"].astype(str).str.lower().str.contains(query, na=False) |
            display_df["Student_ID"].astype(str).str.lower().str.contains(query, na=False)
        ]
    columns = ["Student_ID", "Student_Name", "Class", "Department", "Semester",
               "Math", "Science", "English", "Computer", "Total_Marks",
               "Average_Marks", "Grade", "Result", "Rank"]
    st.dataframe(display_df[columns].sort_values("Rank"), use_container_width=True, hide_index=True)
    csv_bytes = display_df[columns].to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download filtered results (CSV)", data=csv_bytes,
                       file_name="analyzed_student_results.csv", mime="text/csv")

with tab3:
    st.subheader("Subject summary")
    st.dataframe(subject_summary(filtered).round(2), use_container_width=True)
    st.subheader("Top 10 students")
    st.dataframe(student_rankings(filtered).head(10), use_container_width=True, hide_index=True)
    st.subheader("How results are calculated")
    st.markdown("""
    - **Total marks:** sum of the four subject marks.
    - **Average marks:** total marks divided by the number of subjects.
    - **Pass rule:** a student passes when their average is at least 40 **and** each subject mark is at least 35.
    - **Grades:** A (80+), B (70–79.99), C (60–69.99), D (50–59.99), E (40–49.99), F (below 40).
    - **Pass percentage:** passing students divided by all students in the filtered dataset, multiplied by 100.

    These are demonstration rules. Change them to match your college's official rules before using real results.
    """)

with st.expander("View the loaded raw dataset"):
    st.dataframe(raw_df, use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("Student Academic Performance Analysis Dashboard • Educational demonstration project")

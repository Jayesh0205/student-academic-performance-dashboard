import matplotlib.pyplot as plt
from modules.data_loader import SUBJECT_COLUMNS
from modules.analysis import grade_summary

def subject_bar_chart(df):
    fig, ax = plt.subplots(figsize=(7, 4))
    averages = df[SUBJECT_COLUMNS].mean()
    ax.bar(averages.index, averages.values)
    ax.set_ylabel("Average marks (out of 100)")
    ax.set_ylim(0, 100)
    ax.set_title("Subject-wise Average")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    return fig

def grade_pie_chart(df):
    fig, ax = plt.subplots(figsize=(7, 4))
    counts = grade_summary(df)
    counts = counts[counts > 0]
    if counts.empty:
        ax.text(0.5, 0.5, "No grade data", ha="center", va="center")
    else:
        ax.pie(counts.values, labels=counts.index, autopct="%1.1f%%", startangle=90)
    ax.set_title("Grade Distribution")
    fig.tight_layout()
    return fig

def marks_histogram(df):
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(df["Average_Marks"], bins=10, edgecolor="black")
    ax.set_xlabel("Average marks")
    ax.set_ylabel("Number of students")
    ax.set_title("Student Average Marks Distribution")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    return fig

def class_comparison_chart(df):
    fig, ax = plt.subplots(figsize=(7, 4))
    averages = df.groupby("Class")["Average_Marks"].mean().sort_index()
    ax.bar(averages.index.astype(str), averages.values)
    ax.set_ylabel("Average marks")
    ax.set_ylim(0, 100)
    ax.set_title("Average Performance by Class")
    ax.tick_params(axis="x", rotation=20)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    return fig

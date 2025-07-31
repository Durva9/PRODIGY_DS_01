import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ----- PAGE SETUP -----
st.set_page_config(layout="wide", page_title="Population Distribution Dashboard")

st.markdown(
    "<h1 style='text-align: center; color: white;'>Population Distribution Dashboard by Age and Gender</h1>"
    "<h4 style='text-align: center; color: lightgray; font-style: italic;'>Based on World Bank Data (1960–2024)</h4>",
    unsafe_allow_html=True,
)

# ----- MOCK DATA GENERATION -----
@st.cache_data
def generate_data():
    np.random.seed(42)
    n = 17000
    data = {
        "ID": range(1, n + 1),
        "Age": np.random.randint(0, 90, size=n),
        "Gender": np.random.choice(["Male", "Female"], size=n),
        "Year": np.random.choice([str(year) for year in range(1960, 2025)], size=n)
    }
    return pd.DataFrame(data)

df = generate_data()

# ----- AGE GROUP CATEGORIZATION -----
def categorize_age(age):
    if age <= 14:
        return "0-14"
    elif 15 <= age <= 29:
        return "15-29"
    elif 30 <= age <= 59:
        return "30-59"
    else:
        return "60+"

df["Age Group"] = df["Age"].apply(categorize_age)

# ----- SIDEBAR YEAR FILTER -----
st.sidebar.header("🔎 Filter")
year_filter = st.sidebar.selectbox("Year", options=["All"] + sorted(df["Year"].unique().tolist(), key=int))
if year_filter != "All":
    df = df[df["Year"] == year_filter]

# ----- METRICS -----
total_population = len(df)
male_population = len(df[df["Gender"] == "Male"])
female_population = len(df[df["Gender"] == "Female"])
child_population = len(df[df["Age"] <= 14])
senior_population = len(df[df["Age"] >= 60])

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Population", f"{total_population / 1000:.2f}K")
col2.metric("Male Population", f"{male_population / 1000:.2f}K")
col3.metric("Female Population", f"{female_population / 1000:.2f}K")
col4.metric("Child Population (0-14)", f"{child_population / 1000:.2f}K")
col5.metric("Senior Population (60+)", f"{senior_population / 1000:.2f}K")

# ----- GENDER vs AGE GROUP BAR -----
st.markdown("### 👥 Population by Gender and Age Group")
grouped_gender_age = df.groupby(["Gender", "Age Group"]).size().reset_index(name="Count")

fig_gender = px.bar(
    grouped_gender_age,
    x="Count",
    y="Gender",
    color="Age Group",
    orientation="h",
    barmode="stack",
    labels={"Count": "Population"},
    color_discrete_sequence=px.colors.qualitative.Set2
)
st.plotly_chart(fig_gender, use_container_width=True)

# ----- AGE GROUP HISTOGRAM-STYLE BAR -----
st.markdown("### 📊 Population by Age Group")
age_group_count = df["Age Group"].value_counts().reset_index()
age_group_count.columns = ["Age Group", "Population"]

fig_age = px.bar(
    age_group_count,
    x="Age Group",
    y="Population",
    color="Age Group",
    color_discrete_sequence=px.colors.qualitative.Set2
)
st.plotly_chart(fig_age, use_container_width=True)

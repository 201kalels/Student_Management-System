import requests
import pandas as pd
import streamlit as st

API = "http://127.0.0.1:8000"
st.title("Student Management System")

with st.form("student_form"):
    sid = st.number_input("ID", min_value=1, step=1)
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=5, max_value=100, step=1)
    email = st.text_input("Email")
    marks = st.number_input("Marks", min_value=0.0, max_value=100.0)
    submitted = st.form_submit_button("Add Student")

if submitted:
    payload = {"id": int(sid), "name": name, "age": int(age),
               "email": email, "marks": float(marks)}
    try:
        response = requests.post(f"{API}/students", json=payload, timeout=5)
        if response.status_code == 201:
            st.success("Student added successfully")
        else:
            st.error(response.text)
    except requests.RequestException:
        st.error("Could not connect. Start FastAPI first.")

st.subheader("All students")
try:
    response = requests.get(f"{API}/students", timeout=5)
    response.raise_for_status()
    students = response.json()
    if students:
        df = pd.DataFrame(students)
        st.dataframe(df, use_container_width=True)
        st.metric("Average marks", f"{df['marks'].mean():.2f}")
    else:
        st.info("No students added yet")
        st.metric("Average marks", "N/A")
except requests.RequestException:
    st.warning("FastAPI server is not running.")

import streamlit as st
import requests

st.title("Team Task Manager")

API_URL = "http://127.0.0.1:8000"

menu = ["Signup", "Login", "Tasks"]
choice = st.sidebar.selectbox("Menu", menu)

# Signup
if choice == "Signup":
    st.subheader("Create Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["admin", "member"])

    if st.button("Signup"):
        res = requests.post(f"{API_URL}/signup",
                            json={"email": email, "password": password, "role": role})
        st.success(res.json())

# Login
elif choice == "Login":
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        res = requests.post(f"{API_URL}/login",
                            json={"email": email, "password": password, "role": ""})
        st.write(res.json())

# Tasks
elif choice == "Tasks":
    st.subheader("Create Task")

    title = st.text_input("Task Title")
    assigned = st.text_input("Assign To (email)")
    status = st.selectbox("Status", ["Pending", "In Progress", "Done"])

    if st.button("Create Task"):
        res = requests.post(f"{API_URL}/create-task",
                            json={"title": title, "status": status, "assigned_to": assigned})
        st.success(res.json())

    if st.button("Show Tasks"):
        res = requests.get(f"{API_URL}/tasks")
        st.write(res.json())

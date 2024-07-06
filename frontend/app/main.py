# frontend/app/main.py
import streamlit as st
import requests

API_URL = "http://backend:8000"

def main():
    st.title("Todo App")

    if "token" in st.session_state:
        menu = ["Todo List", "Logout"]
    else:
        menu = ["Login", "Register"]

    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        login()
    elif choice == "Register":
        register()
    elif choice == "Todo List":
        todo_list()
    elif choice == "Logout":
        logout()

def login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        response = requests.post(f"{API_URL}/token", data={"username": username, "password": password})
        if response.status_code == 200:
            token = response.json().get("access_token")
            st.session_state["token"] = token
            st.success("Login successful")
            st.experimental_rerun()
        else:
            st.error("Login failed")

def register():
    st.subheader("Register")
    username = st.text_input("New Username")
    password = st.text_input("New Password", type="password")
    if st.button("Register"):
        register_data = {"username": username, "password": password}
        response = requests.post(f"{API_URL}/register/", json=register_data)
        if response.status_code == 200:
            st.success("User registered successfully")
            # Automatically login after registration
            login_response = requests.post(f"{API_URL}/token", data={"username": username, "password": password})
            if login_response.status_code == 200:
                token = login_response.json().get("access_token")
                st.session_state["token"] = token
                st.success("Login successful")
                st.experimental_rerun()
            else:
                st.error("Login failed")
        else:
            st.error("Failed to register user")

def todo_list():
    st.subheader("Todo List")
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}

    # Fetching tasks
    response = requests.get(f"{API_URL}/todos/", headers=headers)
    if response.status_code == 200:
        todos = response.json()
        for todo in todos:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"{todo['title']} - {todo['description']}")
            with col2:
                if st.button("Delete", key=todo['id']):
                    delete_task(todo['id'], headers)
    else:
        st.error("Failed to fetch tasks")

    # Adding new task
    st.subheader("Add a new task")
    title = st.text_input("Title", key="task_title")
    description = st.text_input("Description", key="task_description")
    if st.button("Add Task"):
        todo_data = {"title": title, "description": description}
        response = requests.post(f"{API_URL}/todos/", json=todo_data, headers=headers)
        if response.status_code == 200:
            st.success("Task added successfully")
            st.experimental_rerun()  # Refresh the list
        else:
            st.error("Failed to add task")

def delete_task(todo_id, headers):
    response = requests.delete(f"{API_URL}/todos/{todo_id}", headers=headers)
    if response.status_code == 200:
        st.success("Task deleted successfully")
        st.experimental_rerun()  # Refresh the list
    else:
        st.error("Failed to delete task")

def logout():
    st.session_state.pop("token", None)
    st.success("Logged out successfully")
    st.experimental_rerun()

if __name__ == "__main__":
    main()

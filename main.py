import streamlit as st
import requests

# Define API base URL
API_URL = "http://localhost:8080/api/tasks"

# Streamlit UI
st.title("Task Manager")

# Add Task Section
st.header("Add Task")
description = st.text_input("Description", placeholder="Enter task description")
status_options = ["Started", "Pending", "Completed"]
status = st.selectbox("Status", status_options)
if st.button("Add Task", use_container_width=True):
    if description.strip():  # Check if description is not empty or only whitespace
        data = {"description": description, "status": status}
        response = requests.post(API_URL, json=data)
        if response.status_code == 200:
            st.success("Task added successfully!")
        else:
            st.error("Failed to add task!")
    else:
        st.error("Task description cannot be empty")

# View Tasks Section
st.header("Tasks")
response = requests.get(API_URL)
tasks = response.json() if response.status_code == 200 else []
if tasks:
    for task in tasks:
        task_id = task['ID']
        with st.container():
            st.markdown(f"**Task {task_id}**")
            cols = st.columns(3)
            with cols[0]:
                task_description = st.text_input(f"Description_{task_id}", value=task['Description'])
            with cols[1]:
                task_status = st.selectbox(f"Status_{task_id}", status_options, index=status_options.index(task['Status']))
            with cols[2]:
                update_button = st.button(f"Update_{task_id}", key=f"update_{task_id}", use_container_width=True)
                delete_button = st.button(f"Delete_{task_id}", key=f"delete_{task_id}", use_container_width=True)

            if update_button:
                data = {"id": task_id, "description": task_description, "status": task_status}
                response = requests.put(API_URL + f"/{task_id}", json=data)
                if response.status_code == 200:
                    st.success(f"Task {task_id} updated successfully!")
                else:
                    st.error(f"Failed to update task {task_id}!")
            if delete_button:
                response = requests.delete(API_URL + f"/{task_id}")
                if response.status_code == 200:
                    st.success(f"Task {task_id} deleted successfully!")
                else:
                    st.error(f"Failed to delete task {task_id}!")
else:
    st.warning("No tasks available.")

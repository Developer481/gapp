import streamlit as st
import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect('project_management.db')
cursor = conn.cursor()

# Create tasks table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT,
        assignee TEXT,
        status TEXT
    )
''')
conn.commit()

def add_task(task, assignee, status):
    # Store the task in the SQLite database
    cursor.execute('''
        INSERT INTO tasks (task, assignee, status)
        VALUES (?, ?, ?)
    ''', (task, assignee, status))
    conn.commit()

def get_all_tasks():
    # Fetch all tasks from the SQLite database
    cursor.execute('SELECT * FROM tasks')
    task_list = cursor.fetchall()
    return task_list

def main():
    # Add a title to the app
    st.title("Project Management App")

    # Add input fields for task details
    task = st.text_input("Task")
    assignee = st.text_input("Assignee")
    status = st.selectbox("Status", ['Not Started', 'In Progress', 'Completed'])

    # Add a button to add the task
    if st.button("Add Task"):
        add_task(task, assignee, status)
        st.success("Task added successfully!")

    # Fetch all tasks from the SQLite database
    task_list = get_all_tasks()

    if len(task_list) > 0:
        # Convert the task list to a DataFrame
        columns = ['ID', 'Task', 'Assignee', 'Status']
        tasks_df = pd.DataFrame(task_list, columns=columns)

        # Display the current tasks
        st.subheader("Task List")
        st.dataframe(tasks_df)
    else:
        st.info("No tasks available.")

if __name__ == '__main__':
    main()

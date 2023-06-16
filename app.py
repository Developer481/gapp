import streamlit as st
import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect('project_tracker.db')
cursor = conn.cursor()

# Create tasks table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT,
        assignee TEXT,
        status TEXT,
        date   TEXT,
        client TEXT,
        comments  TEXT,
        feedback TEXT
    )
''')
conn.commit()

def add_task(task, assignee, status, date, client, comments, feedback):
    # Store the task in the SQLite database
    cursor.execute('''
        INSERT INTO tasks (task, assignee, status, date, client, comments, feedback)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (task, assignee, status, date, client, comments, feedback))
    conn.commit()

def update_task(task_id, status=None, task=None, assignee=None, client=None, date=None, comments=None, feedback=None):
    # Fetch the existing task from the SQLite database
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    existing_task = cursor.fetchone()

    # Update the fields with the new values or keep the existing values if not provided
    updated_status = status if status is not None else existing_task[3]
    updated_task = task if task is not None else existing_task[1]
    updated_assignee = assignee if assignee is not None else existing_task[2]
    updated_client = client if client is not None else existing_task[5]
    updated_date = date if date is not None else existing_task[4]
    updated_comments = comments if comments is not None else existing_task[6]
    updated_feedback = feedback if feedback is not None else existing_task[7]

    # Update the task in the SQLite database
    cursor.execute('''
        UPDATE tasks SET status = ?, task = ?, assignee = ?, client = ?, date = ?, comments = ?, feedback = ?
        WHERE id = ?
    ''', (updated_status, updated_task, updated_assignee, updated_client, updated_date, updated_comments, updated_feedback, task_id))
    conn.commit()

def delete_task(task_id):
    # Delete the task from the SQLite database
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()

def get_all_tasks():
    # Fetch all tasks from the SQLite database
    cursor.execute('SELECT * FROM tasks')
    task_list = cursor.fetchall()
    return task_list

def main():
    st.markdown(
    """
    <style>
    .css-1y4p8pa.e1g8pov64 {
        border: 5px solid skyblue;
        border-radius: 20px;
        padding: 55px;
    }
    .appview-container{
        margin-top:55px;
    }

    .button {
        background-color: skyblue;
        color: white;
        .title-text {
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 30px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
    )
    
    # Add a title to the app
    st.title("Project Management App")

    # Set page layout width and centered content
    st.markdown(
        """
        <style>
        .centered {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }
        .full-width {
            width: 100%;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Apply centered layout to the app
    st.markdown('<div class="centered">', unsafe_allow_html=True)

    # Custom CSS styling
    st.markdown(
        """
        <style>
        .header-text {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .success-message {
            color: green;
            margin-top: 10px;
        }
        .info-message {
            color: #777777;
            margin-top: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<h2 class="header-text">Task Management</h2>', unsafe_allow_html=True)

    operation = st.radio("Select Operation", ("Add Task", "Update Task", "Delete Task"))

    if operation == "Add Task":
        st.markdown('<h3 class="header-text">Add Task</h3>', unsafe_allow_html=True)
        task = st.text_input("Task")
        assignee = st.text_input("Assignee")
        status = st.selectbox("Status", ['Working', 'Critical', 'Sent for Review', 'Done', 'Pending for Review', 'To be discussed', 'To be started'])
        client = st.text_input("Client")
        date = st.text_input("Date")
        comments = st.text_input("comments")
        feedback = st.text_input("feedback")

        if st.button("Submit"):
            add_task(task, assignee, status, date, client, comments, feedback)
            st.success("Task added successfully!")

    elif operation == "Update Task":
        st.markdown('<h3 class="header-text">Update Task</h3>', unsafe_allow_html=True)
        task_id = st.number_input("Task ID")

        # Fetch the existing task based on the provided task ID
        cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        existing_task = cursor.fetchone()

        if existing_task is not None:
            # Get the existing values from the database
            existing_task_id = existing_task[0]
            existing_task_name = existing_task[1]
            existing_assignee = existing_task[2]
            existing_status = existing_task[3]
            existing_date = existing_task[4]
            existing_client = existing_task[5]
            existing_comments = existing_task[6]
            existing_feedback = existing_task[7]

            status_options = ['Working', 'Critical', 'Sent for Review', 'Done', 'Pending for Review', 'To be discussed', 'To be started']
            status_index = status_options.index(existing_status) if existing_status in status_options else 0

            # Pre-fill the form fields with existing values
            task = st.text_input("Task", value=existing_task_name)
            assignee = st.text_input("Assignee", value=existing_assignee)
            status = st.selectbox("Status", status_options, index=status_index)
            client = st.text_input("Client", value=existing_client)
            date = st.text_input("Date", value=existing_date)
            comments = st.text_input("Comments", value=existing_comments)
            feedback = st.text_input("Feedback", value=existing_feedback)

            if st.button("Submit"):
                update_task(task_id, status, task, assignee, client, date, comments, feedback)
                st.success("Task updated successfully!")
        else:
            st.warning("No task found for the provided ID.")

    elif operation == "Delete Task":
        st.markdown('<h3 class="header-text">Delete Task</h3>', unsafe_allow_html=True)
        task_id = st.number_input("Task ID")

        if st.button("Delete"):
            delete_task(task_id)
            st.success("Task deleted successfully!")

    # Display all tasks
    task_list = get_all_tasks()
    if task_list:
        st.markdown('<h2 class="header-text">All Tasks</h2>', unsafe_allow_html=True)
        df = pd.DataFrame(task_list, columns=['ID', 'Task', 'Assignee', 'Status', 'Date', 'Client', 'Comments', 'Feedback'])
        st.dataframe(df)
    else:
        st.info("No tasks found.")

    # Close the database connection
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()

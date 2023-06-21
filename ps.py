import streamlit as st
import sqlite3
import pandas as pd

# Custom CSS styling for the submit button
# Custom CSS styling for the submit button
st.markdown(
    """
    <style>
    .skyblue-button {
        background-color: skyblue;
        color: white;
        padding: 0.375rem 0.75rem;
        border-radius: 0.25rem;
        border: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Connect to SQLite database
conn = sqlite3.connect('project_tracker.db')
cursor = conn.cursor()

# Create user table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
''')
conn.commit()


# Create user table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
''')
conn.commit()

# Create superuser table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS superuser (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
''')
conn.commit()

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

def add_admin(username, password):
    # Store the admin in the SQLite database
    cursor.execute('''
        INSERT INTO admin (username, password)
        VALUES (?, ?)
    ''', (username, password))
    conn.commit()

def get_admin(username):
    # Fetch the admin from the SQLite database
    cursor.execute('SELECT * FROM admin WHERE username = ?', (username,))
    admin = cursor.fetchone()
    return admin

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


def add_user(username, password):
    # Store the user in the SQLite database
    cursor.execute('''
        INSERT INTO user (username, password)
        VALUES (?, ?)
    ''', (username, password))
    conn.commit()

def get_all_user():
    # Fetch all tasks from the SQLite database
    cursor.execute('SELECT * FROM user')
    user_list = cursor.fetchall()
    return user_list


def add_superuser(username, password):
    # Store the superuser in the SQLite database
    cursor.execute('''
        INSERT INTO superuser (username, password)
        VALUES (?, ?)
    ''', (username, password))
    conn.commit()

def get_all_superuser():
    # Fetch all tasks from the SQLite database
    cursor.execute('SELECT * FROM superuser')
    superuser_list = cursor.fetchall()
    return superuser_list

def get_superuser(username):
    # Fetch the superuser from the SQLite database
    cursor.execute('SELECT * FROM superuser WHERE username = ?', (username,))
    superuser = cursor.fetchone()
    return superuser




def get_user(username):
    # Fetch the user from the SQLite database
    cursor.execute('SELECT * FROM user WHERE username = ?', (username,))
    user = cursor.fetchone()
    return user
def app():
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
        st.write("Performing task work...")
        # Add your code for task work here

def app1():
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
        st.write("Performing task work...")
        # Add your code for task work here

def get_tasks_by_user(assignee):
    # Fetch tasks assigned to the user from the SQLite database
    cursor.execute('SELECT * FROM tasks WHERE assignee = ?', (assignee,))
    tasks = cursor.fetchall()
    return tasks

def app2(user):
    user = user[1]
    userdata = get_user(user)
    if userdata:
        st.markdown('<h2 class="header-text">User Tasks</h2>', unsafe_allow_html=True)
        tasks = get_tasks_by_user(user)
        if tasks:
            df = pd.DataFrame(tasks, columns=['ID', 'Task', 'Assignee', 'Status', 'Date', 'Client', 'Comments', 'Feedback'])
            st.dataframe(df)
        else:
            st.info("No tasks found for the user.")
    else:
        st.warning("User not found.")

    st.write("Performing task work...")




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
    


    # Apply centered layout to the app
   

    
    # Create a radio button for login options
    option = st.radio("Select Operation", ("Admin login","Admin create","Super user login", "User login"), key="login-option")

    # Add a submit button with sky blue color
    if option == "Admin login":
        st.write("Performing admin login...")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            admin = get_admin(username)
            if admin is not None:
                if password == admin[2]:
                    option1 = st.radio("Select Admin Operation", ("Create user", "Create superuser", "Task work"), key="admin-operation")
                    if option1 == "Create user":
                        st.write("Creating user...")
                        username = st.text_input("Username", key="username_input")
                        password = st.text_input("Password", key="password_input", type="password")
 

                        if st.button("Submit"):
                            add_user(username, password)
                            st.success("User added successfully!")
                        # Display all user
                        task_list1 = get_all_user()
                        if task_list1:
                            st.markdown('<h2 class="header-text">All User</h2>', unsafe_allow_html=True)
                            df = pd.DataFrame(task_list1, columns=['ID', 'user','password'])
                            st.dataframe(df)
                        else:
                            st.info("No tasks found.")
                            st.write("Performing task work...")
                            # Add your code for task work here

                    elif option1 == "Create superuser":
                        st.write("Creating superuser...")
                        username = st.text_input("Username")
                        password = st.text_input("Password", type="password")

                        if st.button("Submit"):
                            add_superuser(username, password)
                            st.success("Superuser added successfully!")
                        # Display all superuser
                        task_list2 = get_all_superuser()
                        if task_list2:
                            st.markdown('<h2 class="header-text">All Superuser</h2>', unsafe_allow_html=True)
                            df = pd.DataFrame(task_list2, columns=['ID', 'user','password'])
                            st.dataframe(df)
                        else:
                            st.info("No tasks found.")
                            st.write("Performing task work...")
                            # Add your code for task work here


                    elif option1 == "Task work":
                        app()
    elif option == "Admin create":
        st.write("Creating admin...")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Create"):
            add_admin(username, password)
            st.success("Admin created successfully!")


                
    elif option == "Super user login":
        st.write("Performing super user login...")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            superuser = get_superuser(username)
            if superuser is not None:
                if password == superuser[2]:
                    app1()
                    st.success("Super user login successful!")
                    # Add your code for super user login here
                    
                else:
                    st.error("Invalid password for the provided username.")
            else:
                st.error("Super user not found for the provided username.")

        st.write("Performing super user login...")
        # Add your code for super user login here

    elif option == "User login":
        st.write("Performing user login...")
        # Add your code for user login here
        st.write("Performing user login...")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = get_user(username)
            if user is not None:
                if password == user[2]:
                    app2(user)
                    st.success("User login successful!")
                    # Add your code for user login here
                else:
                    st.error("Invalid password for the provided username.")
            else:
                st.error("User not found for the provided username.")

if __name__ == "__main__":
    main()

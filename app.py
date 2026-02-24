import streamlit as st
from datetime import datetime
from streamlit_calendar import calendar

st.set_page_config(page_title="Productivity Dashboard", layout="wide")


if "todos" not in st.session_state:
    st.session_state.todos = []

if "schedule" not in st.session_state:
    st.session_state.schedule = []

if "notes" not in st.session_state:
    st.session_state.notes = []


st.sidebar.title("📌 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["To-Do List", "Scheduler", "Notes", "Overview"]
)


if page == "To-Do List":
    st.title("✅ To-Do List")

    new_task = st.text_input("Add a new task")

    col_add, col_clear = st.columns([2, 1])

    if col_add.button("Add Task"):
        if new_task.strip():
            st.session_state.todos.append({
                "task": new_task,
                "done": False
            })
            st.success("Task added!")
            st.rerun()

    if col_clear.button("🗑️ Delete All Tasks"):
        st.session_state.todos.clear()
        st.rerun()

    st.markdown("### Your Tasks")

    for i, task in enumerate(st.session_state.todos):
        col1, col2 = st.columns([4, 1])

        task["done"] = col1.checkbox(
            task["task"],
            value=task["done"],
            key=f"check_{i}"
        )

        if col2.button("❌", key=f"delete_todo_{i}"):
            st.session_state.todos.pop(i)
            st.rerun()



elif page == "Scheduler":
    st.title("📅 Scheduler")

    event_name = st.text_input("Event name")
    event_date = st.date_input("Select date")
    event_time = st.time_input("Select time")

    col_add, col_clear = st.columns([2, 1])

    if col_add.button("Add Event"):
        if event_name.strip():
            event_datetime = datetime.combine(event_date, event_time)
            st.session_state.schedule.append(
                {
                    "title": event_name,
                    "start": event_datetime.isoformat(),
                }
            )
            st.success("Event scheduled!")
            st.rerun()

    if col_clear.button("🗑️ Delete All Events"):
        st.session_state.schedule.clear()
        st.rerun()

    st.markdown("### 📆 Calendar View")

    calendar_options = {
        "initialView": "dayGridMonth",
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek,timeGridDay"
        },
        "editable": False,
        "selectable": True,
    }

    calendar(
        events=st.session_state.schedule,
        options=calendar_options,
        key="calendar"
    )

    st.markdown("### Upcoming Events")

    for i, event in enumerate(st.session_state.schedule):
        col1, col2 = st.columns([4, 1])
        col1.write(
            f"{event['title']} - {event['start'][:16].replace('T', ' ')}"
        )
        if col2.button("❌", key=f"delete_sched_{i}"):
            st.session_state.schedule.pop(i)
            st.rerun()



elif page == "Notes":
    st.title("📝 Notes")

    new_note = st.text_area("Write a note")

    col_add, col_clear = st.columns([2, 1])

    if col_add.button("Save Note"):
        if new_note.strip():
            st.session_state.notes.append(new_note)
            st.success("Note saved!")
            st.rerun()

    if col_clear.button("🗑️ Delete All Notes"):
        st.session_state.notes.clear()
        st.rerun()

    st.markdown("### Saved Notes")

    for i, note in enumerate(st.session_state.notes):
        col1, col2 = st.columns([4, 1])
        col1.write(note)
        if col2.button("❌", key=f"delete_note_{i}"):
            st.session_state.notes.pop(i)
            st.rerun()



elif page == "Overview":
    st.title("📊 Overview")

    total_tasks = len(st.session_state.todos)
    completed_tasks = len(
        [t for t in st.session_state.todos if t["done"]]
    )
    total_events = len(st.session_state.schedule)
    total_notes = len(st.session_state.notes)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Tasks", total_tasks)
    col2.metric("Completed Tasks", completed_tasks)
    col3.metric("Events", total_events)
    col4.metric("Notes", total_notes)

    if total_tasks > 0:
        progress = completed_tasks / total_tasks
        st.progress(progress)

    st.markdown("### Pending Tasks")
    for task in st.session_state.todos:
        if not task["done"]:
            st.write(f"- {task['task']}")

    st.markdown("### Upcoming Events")
    for event in st.session_state.schedule:
        st.write(
            f"{event['title']} - {event['start'][:16].replace('T', ' ')}"
        )

    st.markdown("### Notes")
    for note in st.session_state.notes:
        st.write(f"- {note}")
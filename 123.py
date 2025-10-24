import streamlit as st
import pandas as pd
import sqlite3
import datetime

# ----------------------------------------------------------
# 🎓 STREAMLIT SCHOOL MANAGEMENT SYSTEM
# ----------------------------------------------------------

# Page setup
st.set_page_config(page_title="🎓 School Management System", page_icon="🏫", layout="wide")

st.title("🎓 School Management System")
# st.caption("A web-based CRUD app built using Streamlit and SQLite.")

# ----------------------------------------------------------
# 📦 DATABASE SETUP
# ----------------------------------------------------------
conn = sqlite3.connect("SchoolManagement.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS SCHOOL_MANAGEMENT (
    STUDENT_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    NAME TEXT,
    EMAIL TEXT,
    PHONE_NO TEXT,
    GENDER TEXT,
    DOB TEXT,
    STREAM TEXT

)
""")
conn.commit()

# ----------------------------------------------------------
# 🔧 Helper functions
# ----------------------------------------------------------
def add_record(name, email, phone, gender, dob, stream):
    cursor.execute(
        "INSERT INTO SCHOOL_MANAGEMENT (NAME, EMAIL, PHONE_NO, GENDER, DOB, STREAM) VALUES (?, ?, ?, ?, ?, ?)",
        (name, email, phone, gender, dob, stream)
    )
    conn.commit()

def delete_record(student_id):
    cursor.execute("DELETE FROM SCHOOL_MANAGEMENT WHERE STUDENT_ID = ?", (student_id,))
    conn.commit()

def view_all_records():
    cursor.execute("SELECT * FROM SCHOOL_MANAGEMENT")
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=["Student ID", "Name", "Email", "Phone No", "Gender", "DOB", "Stream"])
    return df

def reset_database():
    cursor.execute("DELETE FROM SCHOOL_MANAGEMENT")
    conn.commit()

# ----------------------------------------------------------
# 🧠 MAIN APP INTERFACE
# ----------------------------------------------------------

# Sidebar for Navigation
menu = ["Add Record", "View Records", "Delete Record", "Reset Database"]
choice = st.sidebar.radio("📋 Menu", menu)

# ----------------------------------------------------------
# 🧾 ADD RECORD SECTION
# ----------------------------------------------------------
if choice == "Add Record":
    st.subheader("➕ Add a New Student Record")

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Contact Number")
    with col2:
        gender = st.selectbox("Gender", ["Select", "Male", "Female"])
        dob = st.date_input("Date of Birth", datetime.date(2005, 1, 1))
        stream = st.text_input("Stream")

    if st.button("💾 Add Record"):
        if not name or not email or not phone or gender == "Select" or not stream:
            st.error("⚠️ Please fill all fields before submitting.")
        else:
            try:
                add_record(name, email, phone, gender, dob.strftime("%Y-%m-%d"), stream)
                st.success(f"✅ Record added for {name}")
            except Exception as e:
                st.error(f"Error: {e}")

# ----------------------------------------------------------
# 📋 VIEW RECORDS SECTION
# ----------------------------------------------------------
elif choice == "View Records":
    st.subheader("📊 All Student Records")

    df = view_all_records()
    if df.empty:
        st.info("No records found. Add some students first.")
    else:
        st.dataframe(df, use_container_width=True)

        # Search feature
        search_term = st.text_input("🔍 Search by Name or Stream")
        if search_term:
            filtered = df[df["Name"].str.contains(search_term, case=False) | df["Stream"].str.contains(search_term, case=False)]
            st.dataframe(filtered, use_container_width=True)
        else:
            st.dataframe(df, use_container_width=True)

        # Summary stats
        st.write("### 📈 Summary")
        st.write(f"Total Students: **{len(df)}**")
        st.bar_chart(df["Stream"].value_counts())

# ----------------------------------------------------------
# 🗑️ DELETE RECORD SECTION
# ----------------------------------------------------------
elif choice == "Delete Record":
    st.subheader("🗑️ Delete a Student Record")

    df = view_all_records()
    if df.empty:
        st.warning("No records available to delete.")
    else:
        st.dataframe(df, use_container_width=True)
        student_id = st.number_input("Enter Student ID to Delete", min_value=1, step=1)

        if st.button("🗑️ Delete"):
            try:
                delete_record(student_id)
                st.success(f"Record with ID {student_id} deleted successfully.")
            except Exception as e:
                st.error(f"Error: {e}")

# ----------------------------------------------------------
# ♻️ RESET DATABASE SECTION
# ----------------------------------------------------------
elif choice == "Reset Database":
    st.subheader("⚠️ Reset the Entire Database")

    st.warning("This will permanently delete all student records!")
    if st.button("🚨 Confirm Delete All"):
        reset_database()
        st.success("✅ All records have been deleted successfully!")

# ----------------------------------------------------------
# Footer
# ----------------------------------------------------------
# st.write("---")
# st.caption("📘 Developed using Python, SQLite, and Streamlit | © 2025")


from langchain_core.tools import tool
from db_connection import get_connection
import os
import json
import sqlite3

@tool
def AddTwoNumbers(a:int, b:int)->str:
    '''sum of two numbers'''
    return f'Sum of the given numbers is {(a+b)}'

@tool
def MultiplyTwoNumbers(a:int, b:int)->str:
    '''multiplication of two numbers'''
    return f'Multiplication of the given numbers is {(a*b)}'

@tool
def SaveToFile(content:str)->str:
    """
    Create a new xlog.txt file and save the provided content into it.

    Use this tool ONLY when the user wants to create/save NEW data or replace the entire existing file content.

    Do NOT use this tool when the user wants to modify, edit, add or change specific existing data in xlog.txt. For those requests use UpdateToFile instead.
    """
    with open("./xlog.txt", "w") as file:
        file.write(content)
    return "File saved successfully!"

@tool
def ReadFromFile()->str:
    """
    Read and return the current content of xlog.txt

    Use this tool when the user wants to view, read, check or retrieve information from the file.
    """
    with open("./xlog.txt", "r") as file:
        return file.read()

@tool
def DeleteFile(filename:str)->str:
    """
    Delete the specified file.

    Use this tool ONLY when the user explicitly wants to delete a file. Do not use it for modifying or clearing file content.
    """
    if os.path.exists(filename):
        os.remove(filename)
        return f"{filename} deleted successfully"
    else:
        return f"{filename} does not exist"

@tool
def UpdateToFile(content:str)->str:
    """
    Add new content to the existing xlog.txt file.

    Use this tool ONLY when the user wants to add, append, insert or save NEW information to the existing file.
    """
    with open("xlog.txt", "a") as file:
        file.write("\n"+ content)
    return f"Content added to log file successfully"

@tool
def add_student(name:str, email:str)->str:
    """
    Add a new student to the database.
    """
    try:
        with get_connection() as con:
            cursor = con.cursor()
            cursor.execute("INSERT INTO students (student_name,student_email) VALUES (?,?)",(name, email))

            if cursor.rowcount == 1:
                return "Student information successfully inserted into database!"
            else:
                return "Unable to insert student information"

    except sqlite3.Error as e:
        return f"Database error: {e}"

@tool
def show_all_students():
    """
    Show all students information from the database
    """
    try:
        with get_connection() as con:
            cursor = con.cursor()
            cursor.execute("SELECT student_id, student_name,student_email FROM students")
            data = cursor.fetchall()

        students = []

        for row in data:
            students.append({
                "Roll": row[0],
                "Name": row[1],
                "Email": row[2]
            })

        return json.dumps(students, indent=1)

    except sqlite3.Error as e:
        return f"Database error: {e}"

@tool
def update_student(id:int, name:str, email:str)->str:
    """
    Update a student's name and email using the student ID
    """
    try:
        with get_connection() as con:
            cursor = con.cursor()
            cursor.execute("UPDATE students SET student_name = ?,student_email = ? WHERE student_id = ?",(name,email,id))

            if cursor.rowcount == 1:
                return "Student information updated successfully!"
            else:
                return f"No student found with ID {id}"

    except sqlite3.Error as e:
        return f"Database error: {e}"

@tool
def delete_student(id:int)->str:
    """
    Delete a student using the student ID
    """
    try:
        with get_connection() as con:
            cursor = con.cursor()
            cursor.execute("DELETE FROM students WHERE student_id = ?",(id,))

            if cursor.rowcount == 1:
                return "Student information deleted successfully!"
            else:
                return f"No student found with ID {id}"

    except sqlite3.Error as e:
        return f"Database error: {e}"

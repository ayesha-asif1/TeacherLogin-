import sqlite3
from flask import Flask, render_template, redirect, request, session, jsonify, url_for

app = Flask(__name__)
app.secret_key = 'uvas_secret_key'

# --- DATABASE INITIALIZATION ---
def init_db():
    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()
    
    # 1. Create the Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            full_name TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # 2. Create the Classes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_email TEXT NOT NULL,
            day TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            subject TEXT NOT NULL,
            room TEXT NOT NULL
        )
    ''')
    
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    
    if count == 0:
        # Add the first teacher
        cursor.execute("INSERT INTO users (email, full_name, password) VALUES (?, ?, ?)", 
                       ('teacher@uvas.edu.pk', 'Dr. Ahmad', 'ahmad'))
        print("Dr. Smith added.")

    # Re-check count to add the second teacher if he doesn't exist yet
    cursor.execute("SELECT COUNT(*) FROM users WHERE email = ?", ('dr.ali@uvas.edu.pk',))
    if cursor.fetchone()[0] == 0:
        # Add the second teacher
        cursor.execute("INSERT INTO users (email, full_name, password) VALUES (?, ?, ?)", 
                       ('dr.ali@uvas.edu.pk', 'Dr. Ali', 'pass456'))
        print("Second teacher (Dr. Ali) added to database.")
    # ---------------------------

    conn.commit()
    conn.close()

# Make sure this is called so the changes happen!
init_db()
# Run the setup every time the app starts
init_db()

# --- ROUTES ---

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email_input = request.form.get("username").strip().lower()
        pass_input = request.form.get("password").strip()
        
        conn = sqlite3.connect('timetable.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # This will no longer crash because we just created the table!
        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email_input, pass_input))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session["user_email"] = user["email"]
            session["user_name"] = user["full_name"]
            return redirect(url_for("dashboard"))
        
        return render_template("login.html", error="Invalid Email or Password")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user_email" not in session:
        return redirect(url_for("login"))
    
    conn = sqlite3.connect('timetable.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM classes WHERE teacher_email = ?", (session["user_email"],))
    
    # Fix the 'Row is not JSON serializable' error from earlier
    rows = cursor.fetchall()
    timetable_list = [dict(row) for row in rows] 
    conn.close()
    
    return render_template("dashboard.html", user_name=session["user_name"], timetable=timetable_list)

@app.route("/api/timetable", methods=["POST"])
def manage_timetable():
    if "user_email" not in session:
        return jsonify({"success": False}), 401

    data = request.json
    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()

    if data.get("action") == "add":
        cursor.execute('''
            INSERT INTO classes (teacher_email, day, start_time, end_time, subject, room)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (session["user_email"], data["day"], data["start_time"], data["end_time"], data["subject"], data["room"]))
    
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/student_info")
def student_info():
    return render_template("student_info.html")

if __name__ == "__main__":
    app.run(debug=True)
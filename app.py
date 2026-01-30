from flask import Flask, render_template, redirect, request, session, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///timetable.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False) # 'teacher', 'admin', 'student'
    name = db.Column(db.String(100))
    department = db.Column(db.String(50))

class Timetable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    day = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.String(20), nullable=False) # e.g., "09:00"
    end_time = db.Column(db.String(20), nullable=False)   # e.g., "10:00"
    subject = db.Column(db.String(100), nullable=False)
    room = db.Column(db.String(50), nullable=False)

# Create tables and seed admin/teacher if not exists
with app.app_context():
    db.create_all()
    # Seed a test teacher if not exists
    if not User.query.filter_by(email='teacher@uvas.edu.pk').first():
        hashed_pw = generate_password_hash('password123')
        teacher = User(email='teacher@uvas.edu.pk', password=hashed_pw, role='teacher', name='Dr. Smith', department='CS')
        db.session.add(teacher)
        db.session.commit()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        session['role'] = user.role
        session['name'] = user.name
        if user.role == 'teacher':
            return redirect(url_for('dashboard'))
        else:
            return "Role not supported yet", 403
            
    return render_template("index.html", error="Invalid credentials")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session or session.get('role') != 'teacher':
        return redirect(url_for('index'))
    
    # Fetch timetable for this teacher
    timetable_entries = Timetable.query.filter_by(teacher_id=session['user_id']).all()
    return render_template("dashboard.html", user_name=session['name'], timetable=timetable_entries)

@app.route("/api/timetable", methods=["POST"])
def update_timetable():
    if 'user_id' not in session or session.get('role') != 'teacher':
        return jsonify({"error": "Unauthorized"}), 401
        
    data = request.json
    action = data.get('action')
    
    if action == 'add':
        new_entry = Timetable(
            teacher_id=session['user_id'],
            day=data.get('day'),
            start_time=data.get('start_time'),
            end_time=data.get('end_time'),
            subject=data.get('subject'),
            room=data.get('room')
        )
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({"success": True, "id": new_entry.id})

    elif action == 'update':
        entry_id = data.get('id')
        entry = Timetable.query.get(entry_id)
        if entry and entry.teacher_id == session['user_id']:
            entry.day = data.get('day')
            entry.start_time = data.get('start_time')
            entry.end_time = data.get('end_time')
            entry.subject = data.get('subject')
            entry.room = data.get('room')
            db.session.commit()
            return jsonify({"success": True})
        
    elif action == 'delete':
        entry_id = data.get('id')
        entry = Timetable.query.get(entry_id)
        if entry and entry.teacher_id == session['user_id']:
            db.session.delete(entry)
            db.session.commit()
            return jsonify({"success": True})
            
    return jsonify({"error": "Invalid action"}), 400

if __name__ == "__main__":
    app.run(debug=True)

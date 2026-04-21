from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from config import *
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = SECRET_KEY

def load_users():
    try:
        with open(USERS_DB, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(USERS_DB, 'w') as f:
        json.dump(users, f, indent=2)

def load_data():
    try:
        students = pd.read_csv(f'{LOCAL_DATA_PATH}/students.csv')
        grades = pd.read_csv(f'{LOCAL_DATA_PATH}/grades.csv')
        return students, grades
    except:
        students = pd.DataFrame({
            'student_id': range(1,101),
            'name': [f'Student_{i}' for i in range(1,101)],
            'age': np.random.randint(18,25,100),
            'gender': np.random.choice(['M','F'],100)
        })
        grades = pd.DataFrame({
            'student_id': np.random.choice(range(1,101),1000),
            'course_id': np.random.randint(1,20,1000),
            'grade': np.random.normal(75,15,1000).clip(0,100),
            'attendance': np.random.uniform(70,100,1000)
        })
        return students, grades

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        users = load_users()
        
        if username in users and check_password_hash(users[username]['password'], password):
            session['user'] = username
            session['role'] = users[username]['role']
            session['name'] = users[username]['name']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials!', 'error')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        role = request.form.get('role', 'teacher')
        
        users = load_users()
        
        if username in users:
            flash('Username already exists!', 'error')
        elif len(password) < 6:
            flash('Password must be at least 6 characters!', 'error')
        else:
            # Hash password
            hashed_pw = generate_password_hash(password)
            users[username] = {
                'name': name,
                'email': email,
                'role': role,
                'password': hashed_pw,
                'created': datetime.now().strftime('%Y-%m-%d %H:%M')
            }
            save_users(users)
            flash(f'Welcome {name}! Account created successfully!', 'success')
            return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    role = session.get('role')
    students, grades = load_data()
    
    if role == 'admin':
        return admin_dashboard(students, grades)
    elif role == 'teacher':
        return teacher_dashboard(students, grades)
    elif role == 'student':
        return student_dashboard(students, grades)
    elif role == 'analyst':
        return analyst_dashboard(students, grades)

# Role dashboards (same as before - admin_dashboard, teacher_dashboard, etc.)
def admin_dashboard(students, grades):
    users = load_users()
    predictions = [{'id':i, 'risk':'HIGH' if np.random.random()>0.6 else 'LOW'} for i in range(1,21)]
    
    fig1 = px.histogram(grades, x='grade', title='All Grades Distribution')
    fig2 = px.pie(students, names='gender', title='Student Demographics')
    
    alerts = ['🚨 15 High Risk Students', f'👥 {len(users)} Active Users']
    
    return render_template('dashboard.html',
                         role='admin',
                         title='Admin Control Panel',
                         predictions=predictions,
                         charts={'grades': fig1.to_html(full_html=False, include_plotlyjs='cdn'),
                                'demo': fig2.to_html(full_html=False, include_plotlyjs='cdn')},
                         alerts=alerts,
                         stats={'Total Students': len(students), 'Total Users': len(users), 'Avg Grade': f"{grades['grade'].mean():.1f}"})

def teacher_dashboard(students, grades):
    class_students = students.head(30)
    class_grades = grades[grades['student_id'].isin(class_students['student_id'])]
    
    fig1 = px.scatter(class_grades, x='attendance', y='grade', title='Attendance vs Grade')
    fig2 = px.bar(class_students.head(10), x='name', y='student_id', title='Top Students')
    
    return render_template('dashboard.html',
                         role='teacher',
                         title='Teacher Classroom Dashboard',
                         predictions=[{'id':i, 'risk':'LOW'} for i in range(1,11)],
                         charts={'performance': fig1.to_html(full_html=False, include_plotlyjs='cdn'),
                                'class': fig2.to_html(full_html=False, include_plotlyjs='cdn')},
                         alerts=['📚 Check attendance reports'],
                         stats={'Class Size': len(class_students), 'Avg Grade': f"{class_grades['grade'].mean():.1f}"})

def student_dashboard(students, grades):
    my_id = 1
    my_grades = grades[grades['student_id'] == my_id].head(10)
    
    fig1 = px.line(my_grades, x='course_id', y='grade', title='My Course Grades')
    
    return render_template('dashboard.html',
                         role='student',
                         title='My Student Dashboard',
                         predictions=[{'id': my_id, 'risk': 'LOW'}],
                         charts={'my_grades': fig1.to_html(full_html=False, include_plotlyjs='cdn')},
                         alerts=['✅ Good performance!'],
                         stats={'My Avg': f"{my_grades['grade'].mean():.1f}", 'Courses': len(my_grades)})

def analyst_dashboard(students, grades):
    avg_grades = grades.groupby('course_id')['grade'].mean().reset_index()
    
    fig1 = px.bar(avg_grades, x='course_id', y='grade', title='Course Analytics')
    fig2 = px.box(grades, x='course_id', y='grade', title='Grade Distribution')
    
    return render_template('dashboard.html',
                         role='analyst',
                         title='Data Analyst Dashboard',
                         predictions=[],
                         charts={'analytics': fig1.to_html(full_html=False, include_plotlyjs='cdn'),
                                'distribution': fig2.to_html(full_html=False, include_plotlyjs='cdn')},
                         alerts=['📊 New trends detected'],
                         stats={'Courses': len(avg_grades), 'Records': len(grades)})

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    print("🚀 EduPredict - Full Auth System")
    print("📝 http://localhost:5000 (Login)")
    print("➕ http://localhost:5000/signup (New User)")
    app.run(host='localhost', port=5000, debug=True)